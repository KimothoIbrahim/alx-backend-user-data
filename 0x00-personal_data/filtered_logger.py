#!/usr/bin/env python3
import re
import logging
from typing import List

def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    for data in fields:
        pattern = rf"{data}=[^;]*"
        message = re.sub(pattern, f'{data}={redaction}', message)
    return message
