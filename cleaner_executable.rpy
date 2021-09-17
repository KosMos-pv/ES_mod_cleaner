
init python:
    import re
    import __builtin__ as bltIn
    from shutil import copy as filecopy
    from os import (
        remove,
        path
    )

    if persistent.cleaner_unsupported_renpy == None:
        persistent.cleaner_unsupported_renpy = False

    if _preferences.language == None:
        cleaner_installed = u"""

                New Life Team Mod Cleaner успешно установлен или обновлён.
                Необходимо перезапустить игру, чтобы мод начал работать.
                """
        cleaner_unsupported = u"""

                Неподдерживаемая версия Ren'py!

                Игра была обновлена до более новой версии движка, и теперь New Life Team Mod Cleaner не работает.
                Данное сообщение не является критической ошибкой и показывается только один раз, поэтому просто перезапустите игру.
                В ближайшее время разработчики Mod Cleaner выпустят обновление для совместимости с новой версией движка игры.
                """
    else:
        cleaner_installed = u"""

                New Life Team Mod Cleaner has been successfully installed or updated.
                You must restart the game for the mod to start working.
                """
        cleaner_unsupported = u"""

                Unsupported version of Ren'py!

                The game has been updated to a newer version of the engine, and now New Life Team Mod Cleaner does not work.
                This message is not a critical error and is shown only once, so just restart the game.
                In the near future, the developers of Mod Cleaner will release an update for compatibility with the new version of the game engine.
                """

    class __CleanerInitializer(object):

        def __init__(self):

            self.__modified_bootstrap = self._find_file(
                ("modified_bootstrap.py_")
            )
            self.__not_changed_bootstrap = self._find_file(
                ("not_changed_bootstrap.py_")
            )
            self.__cleaner_file = self._find_file("clean_workshop.py_")

            self.__original_bootstrap = self._renpy_dir("bootstrap.py")
            self.__original_bootstrap_backup = self.get_backup_filename()
            self.__actual_cleaner = self._renpy_dir("clean_workshop.py")

            self.__pyo_files = tuple(
                bltIn.map(
                    lambda x: "{0}.pyo".format(*path.splitext(x)),
                    (self.__original_bootstrap, self.__actual_cleaner)
                )
            )

        def _renpy_dir(self, filename):
            return path.abspath(
                path.join(renpy.config.basedir, "renpy", filename)
            )

        def _find_file(self, filename):
            try:
                _filepath = renpy.loader.transfn(filename)
            except Exception:
                raise Exception(u"Файл {0!r} не обнаружен.".format(filename))
            return path.abspath(_filepath)

        def get_backup_filename(self):
            name, ext = path.splitext(self.__original_bootstrap)
            return u"{0}{1}".format(name, u"{0}_backup".format(ext))

        def del_pyo(self):
            for f in self.__pyo_files:
                if path.isfile(f):
                    remove(f)

        def start_copy(self):

            if self.is_need_copy():
                self.del_pyo()

                filecopy(
                    self.__not_changed_bootstrap,
                    self.__original_bootstrap_backup
                )
                filecopy(self.__modified_bootstrap, self.__original_bootstrap)
                filecopy(self.__cleaner_file, self.__actual_cleaner)
                raise Exception(cleaner_installed)

        def is_need_copy(self):

            if renpy.version(tuple=False) == "Ren'Py 7.4.8.1895":
                persistent.cleaner_unsupported_renpy = False
            else:
                if persistent.cleaner_unsupported_renpy == False:
                    persistent.cleaner_unsupported_renpy = True
                    renpy.save_persistent()
                    raise Exception(cleaner_unsupported)
                else:
                    return False
            if not path.isfile(self.__actual_cleaner):
                return True
            try:
                from renpy.bootstrap import ws_cleaner
            except ImportError:
                return True
            try:
                from renpy.clean_workshop import __version__ as ver
            except ImportError:
                ver = (0, 0, 0)
            if self.parse_version() > ver:
                return True

            return False

        def parse_version(self):

            with open(self.__cleaner_file, "rb") as fl:
                data = fl.read()
            ver = re.search(r"(?<=__version__ = \()[^)]+(?=\))", data)
            if not ver:
                return tuple(bltIn.map(lambda x: float("+inf"), xrange(3)))
            ver = ver.group()
            return tuple(
                bltIn.map(
                    bltIn.int,
                    bltIn.filter(
                        lambda b: b.isdigit(),
                        bltIn.map(lambda a: a.strip(), ver.split(','))
                    )
                )
            )

    __CleanerInitializer().start_copy()
