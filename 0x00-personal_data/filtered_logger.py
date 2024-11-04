#!/usr/bin/env python3
import re
import logging


def filter_datum(fields: list[str],
                 redaction: str,
                 message: str,
                 separator: str = "; ") -> str:
    """
    returns the log message obfuscated
    Args:
        fields str():
    Returns:
        log message
    """
    for data in fields:
        pattern = rf"{data}=[^;]*"
        message = re.sub(pattern, f'{data}={redaction}', message)
    return message
