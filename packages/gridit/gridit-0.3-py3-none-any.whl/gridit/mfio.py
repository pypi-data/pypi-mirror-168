"""Provide support for MODFLOW files."""
from io import StringIO
from pathlib import Path

import numpy as np

from .logger import get_logger

comment_chars = ["!", "#", "//"]


def line_is_comment(line):
    """Return True if line is a comment."""
    line = line.strip()
    for char in comment_chars:
        if line.startswith(char):
            return True
    return False


class Block:
    """Generic block data.

    BEGIN <name> [extra]
    ...
    END <name>
    """

    def __init__(self, name, extra=[]):
        self.name = name
        self.extra = extra

    @classmethod
    def from_file(cls, fname):
        """Not implemented."""
        raise NotImplementedError(
            f"{cls.__class__.__name__} does not have from_file() (yet?)")

    def __repr__(self):
        if self.__class__.__name__ == "Block":
            ret = f"<{self.__class__.__name__} ({self.name})"
            if self.extra:
                ret += " " + ", ".join(self.extra)
            return ret + ">"
        else:
            return f"<{self.__class__.__name__}>"


class _StructuredBlock(Block):
    _lower = []

    def __init__(self, ndarray):
        self.ndarray = ndarray
        # one row: must make it iterable/countable, prevent IndexError on 0-d
        if not ndarray.shape:
            self.ndarray = ndarray.reshape((1,))
        for col in self.ndarray.dtype.names:
            setattr(self, col, self.ndarray[col])
        setattr(self, "_dtype", self.ndarray.dtype)

    def __len__(self):
        return len(self.ndarray)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} ({len(self)}): " +
            ", ".join(self._dtype.names) + ">")

    @classmethod
    def from_file(cls, fp):
        lines = fp.readlines()
        if lines:
            dtype = np.dtype(cls._dtype)
            nparts = len(dtype)
            try:
                dat = np.loadtxt(
                    lines, dtype=dtype, comments=comment_chars)
            except ValueError:
                dat = None
            if dat is None:
                dat = np.empty(len(lines), dtype=dtype)
                empty_row = list(np.empty(1, np.dtype(dtype))[0])
                iter_lines = []
                for line in lines:
                    if line_is_comment(line):
                        continue
                    parts = line.split()
                    npartdiff = len(parts) - nparts
                    if npartdiff < 0:
                        parts.extend(empty_row[npartdiff:])
                    elif npartdiff > 0:
                        parts = parts[:nparts]
                    iter_lines.append(tuple(parts))
                dat = np.fromiter(iter_lines, dtype=dtype)
            for name in cls._lower:
                dat[name] = np.char.lower(dat[name])
            return cls(dat)

    def to_frame(self):
        import pandas as pd

        return pd.DataFrame(self.ndarray)


class _KeyBlock(Block):
    _type = {}
    _lower = []

    def __init__(self, data={}):
        self._keys = []
        for key, value in data.items():
            setattr(self, key, value)
            self._keys.append(key)

    def __len__(self):
        return len(self._keys)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.to_dict()}>"

    def to_dict(self):
        return {key: getattr(self, key) for key in self._keys}

    @classmethod
    def from_file(cls, fp):
        data = {}
        for inline in fp.readlines():
            line = inline.strip()
            if not line:
                continue
            parts = line.split()
            key = parts[0].lower()
            lower_value = key in cls._lower
            if len(parts) == 1:
                data[key] = True
            elif len(parts) == 2:
                value = parts[1]
                if lower_value:
                    value = value.lower()
                if isinstance(cls._type, dict):
                    if key in cls._type:
                        value = cls._type[key](value)
                elif cls._type is not None:
                    value = cls._type(value)
                data[key] = value
            else:
                if lower_value:
                    parts = line.lower().split()
                data[key] = parts[1:]
        return cls(data)


class Options(_KeyBlock):
    _lower = ["length_units"]
    _type = {
        "xorigin": float,
        "yorigin": float,
        "angrot": float,
    }


class File:
    def __init__(self, fname, parent, blocks, logger=None):
        if logger is None:
            self.logger = get_logger(self.__class__.__name__)
        else:
            self.logger = logger
        self.fname = fname
        self.parent = parent
        self.blocks = blocks
        for name, block in blocks.items():
            setattr(self, name, block)

    @staticmethod
    def resolve_fname(fname, parent=None):
        fpath = Path(fname)
        if fpath.is_file():
            return fpath
        if parent is not None and parent.fname is not None:
            parent_fpath = Path(parent.fname).parent / fname
            if parent_fpath.is_file():
                return parent_fpath
        resolve_fpath = Path(fname).resolve()
        if resolve_fpath.is_file():
            return resolve_fpath
        # self.logger.error("cannot resolve fname '%s'", fname)
        return fpath

    @classmethod
    def from_file(cls, fname, parent=None):
        """Read MF6 file."""
        logger = get_logger(cls.__class__.__name__)
        fname_is_file_pointer = hasattr(fname, "readline")
        if fname_is_file_pointer:
            fname = None
            logger.info("reading file pointer: %s", fname)
            fp = fname
        else:
            fname = cls.resolve_fname(fname, parent)
            if not fname.is_file():
                raise ValueError(f"cannot find {fname}")
            logger.info("reading ASCII file: %s", fname)
            fp = open(fname, "r")  # close this in "finally"
        lineno = 0
        blocks = {}
        block_cls = None
        content = None
        try:
            # Index blocks into pieces that are read by their class
            while True:
                lineno += 1
                inline = fp.readline()
                line = inline.lower().strip()
                if not inline:
                    break  # done reading file
                if block_cls is None:
                    if line.startswith("begin "):
                        parts = line.split()
                        block_name = parts[1]
                        block_extra = parts[2:]
                        logger.debug(
                            "%d: start of %r block", lineno, block_name)
                        if block_name in block_classes:
                            block_cls = block_classes[block_name]
                            content = StringIO()
                        else:
                            block_cls = False
                    elif len(line) == 0 or line_is_comment(line):
                        # skip lines outside a block without any data
                        continue
                    else:
                        logger.debug("%s: non-block line", lineno)
                else:  # block_cls is not None
                    if line.startswith(f"end {block_name}"):
                        logger.debug("%d: end of %r", lineno, block_name)
                        if block_cls is False:
                            block = Block(block_name, block_extra)
                        else:
                            content.seek(0)
                            try:
                                block = block_cls.from_file(content)
                            except NotImplementedError:
                                block = Block(block_name, block_extra)
                        blocks[block_name] = block
                        block_cls = None
                    elif block_cls is not False:
                        content.write(inline)
        finally:
            content = None
            if not fname_is_file_pointer:
                logger.debug("closing %r", fname)
                fp.close()
        return cls(fname, parent, blocks, logger)


class NameFile(File):
    def __init__(self, fname, parent, blocks, logger=None):
        super().__init__(fname, parent, blocks, logger)
        self.packages_list = []
        for pak in self.packages.ndarray:
            package = File.from_file(pak["fname"], self)
            package.name = pak["pname"]
            self.packages_list.append(package)
            if not hasattr(self, pak["ftype"]):
                setattr(self, pak["ftype"], package)
            else:
                self.logger.warning("more than one %r found", pak["ftype"])


class Packages(_StructuredBlock):
    _dtype = [("ftype", "|U9"), ("fname", "|U255"), ("pname", "|U16")]
    _lower = ["ftype"]


class Mf6Sim(File):
    def __init__(self, fname, parent, blocks, logger=None):
        super().__init__(fname, parent, blocks, logger)
        self.models_list = []
        for mod in self.models.ndarray:
            model = NameFile.from_file(mod["mfname"], self)
            model.name = mod["mname"]
            self.models_list.append(model)
            if not hasattr(self, mod["mtype"]):
                setattr(self, mod["mtype"], model)
            else:
                self.logger.warning("more than one %r found", mod["mtype"])


class Timing(_KeyBlock):
    pass


class Models(_StructuredBlock):
    _dtype = [("mtype", "|U9"), ("mfname", "|U255"), ("mname", "|U16")]
    _lower = ["mtype"]


class Dimensions(_KeyBlock):
    _type = int

def get_subclasses(cls):
    yield cls
    for subclass in cls.__subclasses__():
        yield from get_subclasses(subclass)
        yield subclass

# filter out the abstract clases (starting with '_')
block_classes = {
    cls.__name__.lower(): cls
    for cls in get_subclasses(Block)
    if not cls.__name__.startswith("_")
}
