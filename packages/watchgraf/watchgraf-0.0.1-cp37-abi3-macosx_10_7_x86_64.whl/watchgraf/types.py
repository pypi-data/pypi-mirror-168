from enum import IntEnum


class Change(IntEnum):

    added = 1
    modified = 2
    deleted = 3


FileChange = tuple[Change, str]