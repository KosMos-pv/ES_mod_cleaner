
init python:

    from re import compile as re_compile
    from shutil import copy as filecopy
    from __builtin__ import (
        filter as filter_fix,
        map as fix_map
    )
    from os import remove
    from os.path import (
        abspath,
        isfile,
        join as os_join
    )

    class CleanerInitializer(object):

        def __init__(self):

            _l = lambda x: abspath(renpy.loader.transfn(x))
            _m = lambda x: abspath(os_join(renpy.config.basedir, "renpy", x))

            self.version_re = re_compile(r"__version__.+=.+")

            self.bootstrap = _l("bootstrap.py_")
            self.cleaner_file = _l("clean_workshop.py_")

            self.original_bootstrap = _m("bootstrap.py")
            self.original_bootstrap_backup = _m("bootstrap.py_backup")
            self.actual_cleaner = _m("clean_workshop.py")

            self.pyo_files = fix_map(
                _m,
                ("bootstrap.pyo", "clean_workshop.pyo")
            )

        def del_pyo(self):
            for f in self.pyo_files:
                if isfile(f):
                    remove(f)

        def start_copy(self):

            if self.is_need_copy():
                self.backup()
                self.del_pyo()
                filecopy(self.bootstrap, self.original_bootstrap)
                filecopy(self.cleaner_file, self.actual_cleaner)
                return True
            return False

        def backup(self):
            if not isfile(self.original_bootstrap_backup):
                filecopy(
                    self.original_bootstrap,
                    self.original_bootstrap_backup
                )

        def is_need_copy(self, force_update=False):

            if force_update:
                return True

            if not isfile(self.actual_cleaner):
                return True

            from renpy.clean_workshop import __version__ as ver
            if self.parse_version() > ver:
                return True

            return False

        def parse_version(self):

            with open(self.cleaner_file, "rb") as fl:
                for line in fl:
                    line = line.decode("utf-8", "ignore").strip()
                    if not line:
                        continue
                    ver_search = self.version_re.search(line)
                    if ver_search:
                        ver = filter_fix(
                            bool,
                            fix_map(
                                (lambda x: x.strip()),
                                ver_search.group().split("=")
                            )
                        )[-1]
                        break
                else:
                    ver = u"+inf"
            return float(ver)

    CleanerInitializer().start_copy()
