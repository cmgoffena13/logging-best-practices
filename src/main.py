import logging
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed

from opentelemetry import trace

from src.logging_conf import setup_logging
from src.pipeline.runner import PipelineRunner
from src.settings import config
from src.sources.registry import MASTER_REGISTRY

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

CPU_COUNT = multiprocessing.cpu_count() or 1
logger.info(f"Using {CPU_COUNT} CPU cores")


def run_pipeline(source_config):
    with tracer.start_as_current_span(f"pipeline.{source_config.name}") as span:
        pipeline_runner = PipelineRunner(source_config)
        result = pipeline_runner.run()
        if result and result[0]:
            span.set_status(trace.Status(trace.StatusCode.OK))
        else:
            span.set_status(trace.Status(trace.StatusCode.ERROR, "Pipeline failed"))
        return result


def main():
    setup_logging()
    logger.info(f"Starting application with log level: {config.LOG_LEVEL}")

    source_configs = MASTER_REGISTRY.get_source_configs()
    if not source_configs:
        logger.warning("No source configs found in registry")
        return

    with ThreadPoolExecutor(max_workers=CPU_COUNT) as executor:
        futures = {
            executor.submit(run_pipeline, source_config): source_config
            for source_config in source_configs
        }
        results = [future.result() for future in as_completed(futures)]

    for result in results:
        if result[0]:
            logger.info(f"Pipeline {result[1]} completed successfully")
        else:
            logger.error(f"Pipeline {result[1]} failed")

    logger.info("All pipelines completed")


if __name__ == "__main__":
    main()
