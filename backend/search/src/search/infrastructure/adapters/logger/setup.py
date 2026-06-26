import json
import logging
import sys
from collections.abc import Callable, Mapping, MutableMapping
from functools import partial
from typing import Any

import structlog
from structlog.contextvars import merge_contextvars

type ProcessorType = Callable[
    [Any, str, MutableMapping[str, Any]],
    Mapping[str, Any] | str | bytes | bytearray | tuple[Any, ...],
]


def setup_logging(debug: bool) -> None:
    shared_processors: list[ProcessorType] = [
        merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(
            serializer=partial(
                json.dumps, ensure_ascii=False, indent=2 if debug else None
            )
        ),
    ]
    structlog.configure(
        processors=shared_processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
