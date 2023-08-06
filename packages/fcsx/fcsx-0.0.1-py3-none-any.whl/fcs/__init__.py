# -*- coding: utf-8 -*-

__version__ = '0.0.1'

from .fcs import (
    PathLike,
    FileLike,
    FileHandlingError,
    FileParsingError,
    ParsingOffsetsError,
    ParsingNotSupportedError,
    file_handler,
    read_header,
    read_text,
    read_data,
    read_analysis,
    read,
    FCS,
)

__all__ = (
    'PathLike',
    'FileLike',
    'FileHandlingError',
    'FileParsingError',
    'ParsingOffsetsError',
    'ParsingNotSupportedError',
    'file_handler',
    'read_header',
    'read_text',
    'read_data',
    'read_analysis',
    'read',
    'FCS',
)
