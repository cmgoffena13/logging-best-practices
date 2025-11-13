# Modern Python Project Example

Example Python Project showcasing best practices in configuration, logging, testing, and continuous integration.

## Main Packages
 - Ruff
 - Pydantic-Settings
 - Pytest
 - Pre-Commit
 - Logger
   - OpenTelemetry Packages

## Logger

### Logger Components
 - Logger
    - Creates the log messages, normally one per file
 - Handler
    - Handlers determine the destination of the logs
 - Formatter
    - Specifies the format of the log message itself
 - Filter
    - Dynamically enriches logs with additional context
    - Provides a way to include/exclude log entries dynamically

### Logger Levels
 - DEBUG
   - Show detailed information
   - Example: Show record values that are inserted for every insert
- INFO
   - Normal operation events
   - Example: Show that a batch of records was inserted
- WARNING
   - When something undesirable happens, but does not impact runtime
   - Example: Show that there were no records available to insert, we expect records
- ERROR
   - When an exception occurs
   - Example: Show that the batch insert failed with an exception
   - NOTE: Use `logger.exception` as best practice to include the traceback when its unexpected
- CRITICAL
   - Application cannot continue
   - Example: Show that the database connection could not be created, unable to insert records
