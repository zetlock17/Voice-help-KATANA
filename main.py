import config
import stt
import tts
from fuzzywuzzy import fuzz
import datetime
import num2text
import webbrowser
import random
import os
import psutil


print(f"{config.VA_NAME} (v{config.VA_VER}) начала свою работу ...")

tts.va_speak('катана приветствует вас')


def va_respond(voice: str):
    print(voice)
    if voice.startswith(config.VA_ALIAS):
        # обращаются к ассистенту
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak("Что?")
        else:
            execute_cmd(cmd['cmd'])


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str):
    if cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказывать анекдоты ..."
        text += "и открывать браузер"
        tts.va_speak(text)
        pass
    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        text = "Сейч+ас " + num2text.num2text(now.hour) + " " + num2text.num2text(now.minute)
        tts.va_speak(text)

    elif cmd == 'joke':
        jokes = ['Как смеются программисты? ... ехе ехе ехе',
                 'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «м+ожно присоединиться?»',
                 'Программист это машина для преобразования кофе в код']

        tts.va_speak(random.choice(jokes))

    elif cmd == 'open_browser':
        operagx_path = 'C:/Users/1/AppData/Local/Programs/Opera GX/opera.exe %s'
        webbrowser.get(operagx_path).open("opera://startpage")
        tts.va_speak('браузер открыт')

    elif cmd == 'js_book':
        operagx_path = 'C:/Users/1/AppData/Local/Programs/Opera GX/opera.exe %s'
        webbrowser.get(operagx_path).open("https://learn.javascript.ru")
        tts.va_speak('учебник по джаве открыт')

    elif cmd == 'open_sublimetext':
        os.startfile('C:/Program Files/Sublime Text/sublime_text.exe')
        tts.va_speak('редактор кода открыт')

    elif cmd == 'open_cmd':
        os.startfile('C:/WINDOWS/system32/cmd.exe')
        tts.va_speak('командная строка открыта')

    elif cmd == 'pc_off':
    	os.system("shutdown /s /t 00")

    elif cmd == 'open_ya_music':
        operagx_path = 'C:/Users/1/AppData/Local/Programs/Opera GX/opera.exe %s'
        webbrowser.get(operagx_path).open("https://music.yandex.ru/home")
        tts.va_speak('яндекс музыка запущена')

    elif cmd == 'close_sublimetext':
        for process in (process for process in psutil.process_iter() if process.name()=="sublime_text.exe"):
        	process.kill()
        tts.va_speak('редактор кода закрыт')

    elif cmd == 'close_browser':
        for process in (process for process in psutil.process_iter() if process.name()=="opera.exe"):
            process.kill()
        tts.va_speak('браузер закрыт')


# начать прослушивание команд
stt.va_listen(va_respond)