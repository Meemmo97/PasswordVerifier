import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import InputText
import hashlib
import requests
import ssl
import json
import re
from getpass import getpass
import win32gui, win32con
ssl._create_default_https_context = ssl._create_unverified_context

hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide , win32con.SW_HIDE)

layout = [
    [sg.Text('')],
    [sg.Text('Password tester')],
    [sg.Text('')],
    [sg.Text('Insert your password: '), sg.InputText(key='-PASSWORD-', password_char='*')],
    [sg.Text('')],
    [sg.Button('Close'), sg.Button('Test your password')]
]

window = sg.Window("Password Tester V 1.0.b by Edoardo Sirico", layout)

while True:
    event, values = window.read()
    if event in ['Close', sg.WIN_CLOSED]:
        break

    if event == 'Test your password':  
        password = str(None)
        password = str(values['-PASSWORD-'])
        passwordverifier = hashlib.sha1(password.encode('utf-8'))
        passwordverifier.hexdigest()
        pwdsha5 = passwordverifier.hexdigest()[:5]
        try:
            response = requests.get('https://api.pwnedpasswords.com/range/' + pwdsha5)
        except:
            sg.popup("No internet connection, please try again or change connection!")
        found = False
        for line in response.text.splitlines():
            pwdsharem = passwordverifier.hexdigest()[5:]
            lineacompleta = line[:35]
            if pwdsharem.upper() in line:
                found = True
                sg.popup('Your password has been leaked: ' + line[36:] + ' times, consider to change it. Please insert a new password to test or close the application\n')
                break
        if not found:
            sg.popup('This password are not leaked!')
            
window.close()