# -*- coding: utf-8 -*-
"""Read a Flow Cytometry Standard (FCS) data file into FCS object.

FCS 2.0, 3.0, and 3.1 versions are supported.

Reference:
    [1] Dean PN, Bagwell CB, Lindmo T, Murphy RF, Salzman GC. Data file
    standard for flow cytometry. Cytometry 1990;11:323–332.
    [2] Seamer LC, Bagwell CB, Barden L, Redelman D, Salzman GC, Wood JC,
    Murphy RF. Proposed new data file standard for flow cytometry, version
    FCS 3.0. Cytometry 1997;28:118–122.
    [3] Spidlen J, Moore W, Parks D, Goldberg M, Bray C, Bierre P, Gorombey P,
    Hyun B,Hubbard M, Lange S, et al. Data file standard for flow Cytometry,
    version FCS 3.1. Cytometry Part A 2010;77A(1):97–100.

"""

import os
import io
import functools
import contextlib
import pathlib

from typing import Any, Optional, Sequence, Tuple, Union

PathLike = os.PathLike

FileLike = io.BufferedReader


class _BytesDecodeError(Exception):
    pass


class FileHandlingError(Exception):
    pass


class FileParsingError(Exception):
    pass


class ParsingOffsetsError(FileParsingError):
    pass


class ParsingNotSupportedError(FileParsingError):
    pass


def _typecode(
    datatype: str,
    typesize: int,
    signed: bool = False,
) -> str:
    """Return the data type code in a single character given its type hint
    and type size."""
    if datatype not in ('I', 'F', 'D'):
        raise ValueError('invalid data type')
    if datatype == 'I':
        if typesize not in (1, 2, 4, 8):
            raise ValueError('invalid data type size in bytes')
        if typesize == 1:
            return 'b' if signed else 'B'
        if typesize == 2:
            return 'h' if signed else 'H'
        if typesize == 4:
            return 'i' if signed else 'I'
        if typesize == 8:
            return 'l' if signed else 'L'
    if datatype == 'F':
        if typesize != 4:
            raise ValueError('invalid data type size in bytes')
        return 'f'
    if datatype == 'D':
        if typesize != 8:
            raise ValueError('invalid data type size in bytes')
        return 'd'


def _byteordercode(byteorder: str) -> str:
    """Return the byte order code in a single character given its endianness
    hints."""
    if byteorder not in (
            'big',
            'big-endian',
            '2,1',
            '4,3,2,1',
            'little',
            'little-endian',
            '1,2',
            '1,2,3,4',
    ):
        raise ValueError('invalid byte order')
    if byteorder in ('big', 'big-endian', '2,1', '4,3,2,1'):
        return '>'
    if byteorder in ('little', 'little-endian', '1,2', '1,2,3,4'):
        return '<'


def _typesize(typecode: str) -> int:
    """Return the data type size in bytes given its type code."""
    if typecode not in ('b', 'B', 'h', 'H', 'i', 'I', 'l', 'L', 'f', 'd'):
        raise ValueError('invalid data type code in a single character')
    if typecode in ('b', 'B'):
        return 1
    if typecode in ('h', 'H'):
        return 2
    if typecode in ('i', 'I'):
        return 4
    if typecode in ('l', 'L'):
        return 8
    if typecode == 'f':
        return 4
    if typecode == 'd':
        return 8


def _bytesize(bitsize: Union[int, str]) -> int:
    """Return the number of bytes given a number of bits."""
    bitsize = int(bitsize)
    if bitsize < 0 or bitsize % 8 != 0:
        raise ValueError('invalid number of bits')
    return bitsize // 8


def _itemsize(begin: int, end: int, typesize: Optional[int] = None) -> int:
    """Return the item size from the `begin` file position to the `end` file
    position."""
    bytesize = end - begin + 1
    if typesize is None:
        return bytesize
    if typesize not in (1, 2, 4, 8) or bytesize % typesize != 0:
        raise ValueError('invalid data type size in bytes')
    return bytesize // typesize


def _read_bytesize(f: FileLike) -> int:
    """Read a file-like object (in binary mode).

    Args:
        f: The file-like object opened in binary mode.

    Returns:
        The total number of bytes of the file-like object.

    """
    f.seek(0, os.SEEK_END)
    return f.tell()


def _read_bytes(
    f: FileLike,
    begin: int,
    end: int,
    offset: int = 0,
    whence: int = 0,
    use_array: bool = False,
) -> bytes:
    """Read a file-like object (in binary mode) from the `begin` file
    position to the `end` file position.

    Args:
        f: The file-like object opened in binary mode.
        begin: The byte offset to the beginning position to be read.
        end: The byte offset to the end position to be read.
        offset: The byte offset to the postion to go to before reading.
        whence: The byte offset to the reference postion. A whence value of 0
            measures from the beginning of the file, 1 uses the current file
            position, and 2 uses the end of the file as the reference point.
        use_array: Use `array.array` to read or not.

    Returns:
        The binary data.

    """
    offset += begin
    f.seek(offset, whence)
    size = _itemsize(begin, end)
    if use_array:
        import array
        a = array.array('b')
        a.fromfile(f, size)
        return a.tobytes()
    return f.read(size)


def _read_array(
    f: FileLike,
    begin: int,
    end: int,
    typecode: Union[str, Sequence[str]],
    byteordercode: str,
    offset: int = 0,
    whence: int = 0,
    use_numpy: bool = False,
    shape: Optional[Tuple[int, int]] = None,
) -> Any:
    """Read a file-like object (in binary mode) from the `begin` file
    position to the `end` file position.

    Args:
        f: The file-like object opened in binary mode.
        begin: The byte offset to the beginning position to be read.
        end: The byte offset to the end position to be read.
        offset: The byte offset to the postion to go to before reading.
        whence: The byte offset to the reference postion. A whence value of 0
            measures from the beginning of the file, 1 uses the current file
            position, and 2 uses the end of the file as the reference point.
        typecode: The data type code of the array-like data columns.
        byteordercode: The byte order code of the array-like data.
        use_numpy: Use `numpy.memmap` to read or not.
        shape: The desired shape of the array-like data.

    Returns:
        The array-like data.

    """
    offset += begin
    f.seek(offset, whence)
    if isinstance(typecode, str):
        if use_numpy:
            try:
                import numpy
            except ImportError:
                raise ImportError(
                    "NumPy is not installed, run `pip install fcsx[numpy]` to install"
                )
            data = numpy.memmap(
                f,
                dtype=numpy.dtype(typecode),
                mode='r',
                offset=offset,
                shape=shape,
                order='C',
            )
            return numpy.array(data)
        import array
        size = _itemsize(begin, end, typesize=_typesize(typecode))
        a = array.array(typecode)
        a.fromfile(f, size)
        if byteordercode == '>':
            a.byteswap()
        return list(a)
    if isinstance(list(typecode), list):
        import struct
        size = _itemsize(begin, end)
        iterator = struct.iter_unpack(
            '{}{}'.format(byteordercode, ''.join(typecode)),
            f.read(size),
        )
        return [list(i) for i in iterator]


def _int(data: bytes) -> int:
    """Decode bytes to integer."""
    try:
        return int(data)
    except ValueError:
        return 0
    except TypeError:
        raise _BytesDecodeError(
            'failed to decode bytes to integer (deprecated, to be removed)')


def _str(data: bytes, strip: bool = False) -> str:
    """Decode bytes to string."""
    try:
        data = data.decode(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            data = data.decode(encoding='ISO-8859-1')
        except UnicodeDecodeError:
            raise _BytesDecodeError(
                'failed to decode bytes to string (deprecated, to be removed)')
    if strip:
        data = data.strip()
    return data


def _dict(data: str) -> dict:
    """Decode delimited string to key-value pairs."""
    delimiter = data[0]
    data = data[1:-1]
    if len(data) == 0:
        return {}
    kv_pairs = data.split(delimiter)
    if len(kv_pairs) % 2 != 0:
        raise _BytesDecodeError(
            'failed to decode delimited string to key-value pairs (deprecated, to be removed)'
        )
    return dict(zip(kv_pairs[0::2], kv_pairs[1::2]))


@contextlib.contextmanager
def file_handler(
        filepath_or_buffer: Union[str, PathLike, FileLike]) -> FileLike:
    """Return a file-like object (in binary mode) given any valid string path,
    or path-like, file-like object.

    Args:
        filepath_or_buffer: The given valid string path, or path-like,
            file-like object.

    Returns:
        A file-like object opened in binary mode.

    """
    try:
        if isinstance(filepath_or_buffer, FileLike):
            if 'b' not in filepath_or_buffer.mode:
                raise FileHandlingError(
                    'only file-like object in binary mode is supported')
            f = filepath_or_buffer
        else:
            f = pathlib.Path(filepath_or_buffer).open(mode='rb')
        yield f
    finally:
        f.close()


def read_header(f: FileLike) -> dict:
    """Read the HEADER segment of an FCS file.

    Args:
        f: The file-like object opened in binary mode.

    Returns:
        The HEADER segment of the FCS file.

    """
    header = {}
    header['$VERSION'] = _str(_read_bytes(f, 3, 9), strip=True)
    header['$BEGINTEXT'] = _int(_read_bytes(f, 10, 17))
    header['$ENDTEXT'] = _int(_read_bytes(f, 18, 25))
    header['$BEGINDATA'] = _int(_read_bytes(f, 26, 33))
    header['$ENDDATA'] = _int(_read_bytes(f, 34, 41))
    header['$BEGINANALYSIS'] = _int(_read_bytes(f, 42, 49))
    header['$ENDANALYSIS'] = _int(_read_bytes(f, 50, 57))
    return header


def read_text(f: FileLike, begin: int, end: int) -> dict:
    """Read the (supplemental) TEXT segment of an FCS file.

    Args:
        f: The file-like object opened in binary mode.
        begin: The byte offset to the beginning position of the TEXT segment.
        end: The byte offset to the end position of the TEXT segment.

    Returns:
        The (supplemental) TEXT segment of the FCS file.

    """
    return _dict(_str(_read_bytes(f, begin, end, use_array=True)))


def read_data(
    f: FileLike,
    begin: int,
    end: int,
    dtype: Union[str, Sequence[str]],
    byteorder: str,
    use_numpy: bool = False,
    shape: Optional[Tuple[int, int]] = None,
) -> Any:
    """Read the DATA segment of an FCS file.

    Args:
        f: The file-like object opened in binary mode.
        begin: The byte offset to the beginning position of the DATA segment.
        end: The byte offset to the end position of the DATA segment.
        dtype: The data type code of the DATA segment channels.
        byteorder: The byte order code of the DATA segment.
        use_numpy: Use `numpy.memmap` to read the DATA segment or not.
        shape: The desired shape of the array-like data.

    Returns:
        The DATA segment of the FCS file.

    """
    return _read_array(
        f,
        begin,
        end,
        dtype,
        byteorder,
        use_numpy=use_numpy,
        shape=shape,
    )


def read_analysis(f: FileLike, begin: int, end: int) -> Optional[dict]:
    """Read the optional ANALYSIS segment of an FCS file.

    Args:
        f: The file-like object opened in binary mode.
        begin: The byte offset to the beginning position of the ANALYSIS
            segment.
        end: The byte offset to the end position of the ANALYSIS segment.

    Returns:
        The optional ANALYSIS segment of the FCS file.

    """
    if begin == end:
        return None
    return _dict(_str(_read_bytes(f, begin, end, use_array=True)))


class FCS(object):
    """Object representing a Flow Cytometry Standard (FCS) data file.

    A binary FCS data file consists of a minimum of four segments by order:
        1. HEADER segment
        2. TEXT segment
        3. DATA segment
        4. Optional ANALYSIS segment

    Attributes:
        name: The name of the FCS file.
        header: The HEADER segment.
        text: The TEXT segment.
        data: The DATA segment.
        analysis: The ANALYSIS segment.

    """

    def __init__(
        self,
        filepath_or_buffer: Union[str, PathLike, FileLike],
        use_numpy: bool = False,
    ) -> None:
        """FCS object contructor.

        Args:
            filepath_or_buffer: The given valid string path, or path-like,
                file-like object.
            use_numpy: Use `numpy.memmap` to read the DATA segment or not.

        """
        with file_handler(filepath_or_buffer) as f:
            self.name = f.name
            self.header = self._parse_header(f)
            self.text = self._parse_text(f)
            self.data = self._parse_data(f, use_numpy=use_numpy)
            self.analysis = self._parse_analysis(f)

    @functools.cached_property
    def version(self) -> str:
        """The FCS version of the data file."""
        return self.header['$VERSION']

    @functools.cached_property
    def num_events(self) -> int:
        """The total number of events in the FCS data file."""
        return int(self.text['$TOT'])

    @functools.cached_property
    def num_channels(self) -> int:
        """The number of channels (a.k.a. parameters) in an event."""
        return int(self.text['$PAR'])

    @functools.cached_property
    def channel_labels(self) -> list[str]:
        """The labels of channels."""
        channels = self._channels('$PnS')
        if channels[0].strip():
            return channels
        return self._channels('$PnN')

    @functools.cached_property
    def dtype(self) -> Union[str, list[str]]:
        """The data type code of channels."""
        datatype = self.text['$DATATYPE']
        bitsize = self._channels('$PnB')
        if len(list(set(bitsize))) == 1:
            bitsize = bitsize[0]
            return _typecode(datatype, _bytesize(bitsize))
        return [_typecode(datatype, _bytesize(b)) for b in bitsize]

    @functools.cached_property
    def byteorder(self) -> list:
        """The byte order code for data acquisition."""
        return _byteordercode(self.text['$BYTEORD'])

    @functools.cached_property
    def channels(self):
        """The primary annotations of channels."""
        return {
            key: self._channels(key)
            for key in ('$PnB', '$PnE', '$PnN', '$PnR', '$PnS')
        }

    def __len__(self) -> int:
        return self.num_events

    def __repr__(self) -> str:
        return '{}({}, {})'.format(
            self.__class__.__name__,
            self.name,
            self.version,
        )

    def _offsets(self, key: str) -> Tuple[int, int]:
        """Query the pairs of byte offsets that designate the positions of the
        TEXT, supplemental TEXT, DATA, and ANALYSIS segments.
        """
        key = key.upper()
        if key not in ('TEXT', 'STEXT', 'DATA', 'ANALYSIS'):
            raise KeyError(
                "'{}', only 'TEXT', 'STEXT', 'DATA', and 'ANALYSIS' are supported"
                .format(key))
        metadata = self.header
        if key == 'STEXT' or (key != 'TEXT' and self.version != '2.0'):
            metadata = self.text
        begin = int(metadata['$BEGIN{}'.format(key)])
        end = int(metadata['$END{}'.format(key)])
        if begin > end:
            raise ParsingOffsetsError('invalid byte offsets')
        return begin, end

    def _channels(self, key: str) -> list:
        """Query the annotations of channels."""
        if key not in ('$PnB', '$PnE', '$PnN', '$PnR', '$PnS'):
            raise KeyError(
                "'{}', only '$PnB', '$PnE', '$PnN', '$PnR', and '$PnS' are supported"
                .format(key))
        return [
            self.text[key.replace('n', '{}').format(i + 1)]
            for i in range(self.num_channels)
        ]

    def _parse_header(self, f: FileLike) -> dict:
        """Parse the HEADER segment of an FCS file."""
        header = read_header(f)
        if header['$VERSION'] not in ('2.0', '3.0', '3.1'):
            raise ParsingNotSupportedError(
                'FCS {}, only FCS 2.0, 3.0, and 3.1 versions are supported'.
                format(header['$VERSION']))
        return header

    def _parse_text(self, f: FileLike) -> dict:
        """Parse the TEXT segment of an FCS file."""
        begin, end = self._offsets('text')
        text = read_text(f, begin, end)
        if text['$MODE'] not in ('L',):
            raise ParsingNotSupportedError(
                "'$MODE': '{}', only list ('L') mode is supported".format(
                    text['$MODE']))
        if text['$BYTEORD'] not in ('1,2,3,4', '1,2', '4,3,2,1', '2,1'):
            raise ParsingNotSupportedError(
                "'$BYTEORD': '{}', only big-endian ('4,3,2,1' or '2,1') and little-endian ('1,2,3,4' or '1,2') systems are supported"
                .format(text['$BYTEORD']))
        if text['$DATATYPE'] not in ('I', 'F', 'D'):
            raise ParsingNotSupportedError(
                "'$DATATYPE': '{}', only integer ('I'), float ('F') and double ('D') datatypes are supported"
                .format(text['$DATATYPE']))
        if int(text['$NEXTDATA']) != 0:
            raise ParsingNotSupportedError(
                "'$NEXTDATA': '{}', ignoring additional data (not supported)".
                format(text['$NEXTDATA']))
        return text

    def _parse_data(self, f: FileLike, use_numpy: bool = False) -> Any:
        """Parse the DATA segment of an FCS file."""
        begin, end = self._offsets('data')
        if use_numpy:
            return read_data(
                f,
                begin,
                end,
                self.dtype,
                self.byteorder,
                use_numpy=use_numpy,
                shape=(self.num_events, self.num_channels),
            )
        return read_data(f, begin, end, self.dtype, self.byteorder)

    def _parse_analysis(self, f: FileLike) -> Optional[dict]:
        """Parse the optional ANALYSIS segment of an FCS file."""
        begin, end = self._offsets('analysis')
        return read_analysis(f, begin, end)


def read(
    filepath_or_buffer: Union[str, PathLike, FileLike],
    use_numpy: bool = False,
) -> FCS:
    """Read an FCS file.

    Args:
        filepath_or_buffer: Any valid string path, or path-like, file-like
            object representing the FCS file.
        use_numpy: Use `numpy.memmap` to read the DATA segment or not.

    Returns:
        An FCS object.

    """
    return FCS(filepath_or_buffer, use_numpy=use_numpy)
