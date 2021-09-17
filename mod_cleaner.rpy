init 50 python:
    """
    Фикс для Славя-мода, если вместе с ним установлен 7дл.
    """
    if "slavyana_mod__launcher" in mods:
        colors['fbt'] = {'night': (0, 20, 137, 255), 'sunset': (0, 20, 137, 255), 'day': (0, 20, 137, 255), 'prolog': (0, 20, 137, 255)}
        names['fbt'] = u"Автор"
        store.names_list.append('fbt')

init 410:
    if "NLT_toolbox" in mods:
        $ NLT_addons["cleaner"] = True
        $ NLT_tl["mod_cleaner_descr"] = (
        "Начиная с версии 2.0, этот мод работает полностью в автоматическом режиме. Теперь вам не нужно заходить в этот раздел самостоятельно - вся работа выполняется при запуске игры. Подробнее о работе мода написано на странице мода в мастерской.",
        "Since version 2.0, this mod works completely in automatic mode. Now you do not need to go into this section yourself - all the work is done when the game starts. More about the work of the mod is written on the mod workshop page."
        )
        $ NLT_tl["windows_log_file"] = (
        "Вы можете посмотреть отчёт удаления модов, нажав на кнопку ниже или открыв файл deleted_mods.txt в папке с игрой.",
        "You can view log of deleting mods by pressing button below or opening file deleted_mods.txt in game folder."
        )
        $ NLT_tl["others_log_file"] = (
        "Вы можете посмотреть отчёт удаления модов, открыв файл deleted_mods.txt в папке с игрой.",
        "You can view log of deleting mods by opening file deleted_mods.txt in game folder."
        )
        $ NLT_tl["open_ws_page"] = ("Открыть страницу мода в мастерской", "Open mod workshop page")
        $ NLT_tl["open_log"] = ("Открыть файл отчёта", "Open log file")
        $ NLT_tl["cant_open_cleaner_log"] = ("Не удалось открыть отчёт удаления модов.", "Couldn't open cleaner log.")

init -10:
    screen NLT_interface(mod, type="mod", scroll=False):
        null
        
screen NLT_cleaner:
    modal True
    tag NLT
    use NLT_interface(NLT_tl["mod_cleaner"][NLT_lang]):
        viewport id "NLT_menu":
            mousewheel True
            scrollbars None
            has vbox xfill True spacing 15
            null height 15
            text NLT_tl["mod_cleaner_descr"][NLT_lang] style "settings_text" xpos 0.05 xmaximum 0.85
            if NLT_platform() == "win":
                text NLT_tl["windows_log_file"][NLT_lang] style "settings_text" xpos 0.05 xmaximum 0.85
                textbutton NLT_tl["open_ws_page"][NLT_lang] style "log_button" text_style "settings_header" xalign 0.5 action OpenURL("steam://url/CommunityFilePage/930965068")
                textbutton NLT_tl["open_log"][NLT_lang] style "log_button" text_style "settings_header" xalign 0.5 action Function(NLT_open_file, "deleted_mods.txt")
            else:
                text NLT_tl["others_log_file"][NLT_lang] style "settings_text" xpos 0.05 xmaximum 0.85
            if NLT_error:
                text NLT_tl["cant_open_cleaner_log"][NLT_lang] style "settings_text" xalign 0.5

    on "replace" action SetVariable("NLT_error", False)
