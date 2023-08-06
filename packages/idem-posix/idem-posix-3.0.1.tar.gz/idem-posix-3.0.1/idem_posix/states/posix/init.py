import os


def __sub_virtual__(hub):
    return os.name == "posix", "idem-posix only runs on posix systems"
