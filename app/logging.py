"""This module sets up structured JSON logging for the application using the python-json-logger library."""

import logging

from pythonjsonlogger import jsonlogger


def setup_json_logging() -> None:
    """Configure structured JSON logging for the application."""

    # Create a custom formatter that includes extra fields
    class CustomJsonFormatter(jsonlogger.JsonFormatter):
        def add_fields(self, log_record, record, message_dict) -> None:
            """Add custom fields to the log record."""
            super().add_fields(log_record, record, message_dict)

            # Add standard fields to every log entry
            log_record["timestamp"] = record.created
            log_record["level"] = record.levelname
            log_record["logger"] = record.name

            # Add location info for debugging
            log_record["module"] = record.module
            log_record["function"] = record.funcName
            log_record["line"] = record.lineno

    # Configure the formatter with desired fields
    formatter = CustomJsonFormatter("%(timestamp)s %(level)s %(name)s %(message)s")

    # Set up handler with JSON formatter
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Configure root logger
    logging.root.handlers = [handler]
    logging.root.setLevel(logging.INFO)
