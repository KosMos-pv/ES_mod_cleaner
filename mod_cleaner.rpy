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

screen NLT_cleaner tag NLT:
    modal True

    window background get_image("gui/settings/preferences_bg.jpg"):
        hbox xalign 0.5 yalign 0.08:
            add get_image("gui/settings/star.png") yalign 0.65
            text " " + NLT_tl["mod_cleaner"][NLT_lang] + " " style "settings_link" yalign 0.5 color "#ffffff"
            add get_image("gui/settings/star.png") yalign 0.65
        textbutton translation["Back"][_preferences.language] style "log_button" text_style "settings_link" xalign 0.015 yalign 0.92 action Show("NLT_main_menu", transition=dspr)

        side "c b r":
            area (0.25, 0.23, 0.51, 0.71)
            viewport id "NLT_menu":
                mousewheel True
                scrollbars None
                has vbox xfill True spacing 15
                null height 15
                text NLT_tl["mod_cleaner_descr"][NLT_lang] style "settings_text" xpos 0.1 xmaximum 0.8
                if NLT_platform() == "win":
                    text NLT_tl["windows_log_file"][NLT_lang] style "settings_text" xpos 0.1 xmaximum 0.8
                    textbutton NLT_tl["open_ws_page"][NLT_lang] style "log_button" text_style "settings_header" xalign 0.5 action OpenURL("steam://url/CommunityFilePage/930965068")
                    textbutton NLT_tl["open_log"][NLT_lang] style "log_button" text_style "settings_header" xalign 0.5 action Function(NLT_open_file, "deleted_mods.txt")
                else:
                    text NLT_tl["others_log_file"][NLT_lang] style "settings_text" xpos 0.1 xmaximum 0.8

            bar value XScrollValue("NLT_menu") left_bar "images/misc/none.png" right_bar "images/misc/none.png" thumb "images/misc/none.png" hover_thumb "images/misc/none.png"
            vbar value YScrollValue("NLT_menu") bottom_bar "images/misc/none.png" top_bar "images/misc/none.png" thumb "images/gui/settings/vthumb.png" thumb_offset -12

label NLT_after_clean:
    stop music fadeout 1
    scene black with dissolve
    $ NLT_game_restarting = NLT_tl["game_restarting"][NLT_lang]
    show text "{=credits}{size=50}[NLT_game_restarting]{/size}" at truecenter with dspr
    pause 1
    $ renpy.quit(relaunch=True)
    return
# Unpacked by VladyaBot-decompiler-module on 28 September 2017. 03:56:17.
