"""Directory class.
"""
#Copyright (c) LiveAction, Inc. 2022. All rights reserved.
#Copyright (c) Savvius, Inc. 2013-2019. All rights reserved.
#Copyright (c) WildPackets, Inc. 2013-2014. All rights reserved.

from pathlib import PurePath


class Directory(object):
    """A file system Directory object.
    """

    parent = None
    """The parent :class:`Directory <omniscript.directory.Directory>`
    object of this object. The root directory does not
    have a parent.
    """

    name = ''
    """The name of this Directory"""

    directory_list = []
    """The list of
    :class:`Directory <omniscript.directory.Directory>` objects
    in this Directory."""

    file_list = []
    """The list of File Names in this Directory."""

    _engine = None
    """The OmniEngine this Directory belongs to."""

    def __init__(self, engine, props=None, path=None):
        self.parent = Directory.parent
        self.name = Directory.name
        self.directory = Directory.directory_list
        self.file = Directory.file_list
        self._engine = engine
        self._load(props, path)

    def _load(self, props, path):
        """Load the Directory from a dictionary."""
        if isinstance(props, dict):
            p = PurePath(props['dir'])
            self.name = p.name
            if p.parent != p.parent.parent:
                self.parent = Directory(self._engine, path=p.parent)
            self.directory_list = props['dirs']
            self.file_list = props.get('files')
        elif isinstance(path, PurePath):
            self.name = path.name
            if path.parent != path.parent.parent:
                self.parent = Directory(self._engine, path=path.parent)

    def __str__(self):
        return f'Directory: {self.name}'


# def _create_file_system(engine, props):
#     lst = []
#     if isinstance(props, dict):
#         lst.append(Directory(engine, '', props))
#     return lst
