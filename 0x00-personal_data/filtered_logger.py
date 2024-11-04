#!/usr/bin/env python3
import re
import logging
from typing import list


def filter_datum(fields: list[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for data in fields:
        message = re.sub(rf"{data}=[^;]*", f'{data}={redaction}', message)
    return message
