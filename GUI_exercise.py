# -*- coding: utf-8 -*-
import sys
import urllib
import thread
import urllib2
import json
import qiniu
import recorder
import wx
import threading
import pymssql

from time import ctime, sleep
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    import paho.mqtt.client as mqtt
except ImportError:
    # This part is only required to run the example from within the examples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import paho.mqtt.client"
    import os
    import inspect
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import paho.mqtt.client as mqtt
    import paho.mqtt.publish as publish
def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))

def on_message(mqttc, obj, msg):
    global content_show
    message = json.loads(msg.payload)
    if message.get('sender') != username:
        content_show = content_show + message.get('time') + "\n    " + message.get('sender') + " is sending a message to you " + "\n"
        contents.SetValue(content_show)
        url = r"http://7xl178.com1.z0.glb.clouddn.com/"
        left_url = message.get('key')
        left_url = left_url.decode('gbk', 'replace')
        left_url = urllib.quote(left_url.encode('utf-8', 'replace'))
        url = url + left_url
        f = urllib2.urlopen(url)
        data = f.read()
        code = open(message.get('key'), "wb")
        code.write(data)
        code.close()
        content_show = content_show + "    " + message.get('sender') + "'s message received successfully" + "\n\n"
        contents.SetValue(content_show)

def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)
def upload(uploadFile):
    global key
    token = q.upload_token(bucket_name, uploadFile)
    ret, info = qiniu.put_file(token, uploadFile, uploadFile)
    assert ret['key'] == key
def stopten():
    print "START"
    sleep(10)
    recorder.JUDGE = False
    print "OK"

access_key = 'lo1dTUKUrTcmKtN-LbefdA3vVgHahqr4Bb22JKd5'
secret_key = 'Z2NNqSobYN26Hi22nvyVfaZ4gz3rFVGtWjLNypxS'
bucket_name = 'voicebear'
q = qiniu.Auth(access_key, secret_key)

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect("mqtt-reeky.myalauda.cn", 10157, 60)

def recordMessage(event):
    global win2, contents, win3
    win2.Close()
    win3 = wx.Frame(None, title="channal: " + topic + "   " + "username: " + username, size=(410, 335))
    sendButton = wx.Button(win3, label="send", pos=(150, 18), size=(80, 25))
    sendButton.Bind(wx.EVT_BUTTON, sendMessage)
    contents = wx.TextCtrl(win3, pos=(5, 65), size=(390, 260), style=wx.TE_MULTILINE | wx.HSCROLL)
    win3.Show()
    thread.start_new(recorder.record_wave, ())


def sendMessage(event):
    global key, content_show, now, win3, win2
    recorder.JUDGE = False
    sleep(1)
    key = recorder.FILENAME
    upload(key)
    now = recorder.NOW
    content_show = content_show + now + "\n    " + "message sent successfully" + "\n\n"
    message = {"sender": username, "key": key, "time": now}
    payload = json.dumps(message)
    import paho.mqtt.publish as publish
    publish.single(topic, payload, hostname='mqtt-reeky.myalauda.cn', port=10157)
    contents.SetValue(content_show)

def login(event):
    global key
    username = str(usernameWindow.GetValue())
    password = str(passwordWindow.GetValue())

    if username and password:
        login_data = "username:" + username + "#" + "password:" + password + "#"
        key = "login.txt"
        f = open(key, 'wb')
        f.write(login_data)
        f.close()
        url = r"http://7xl178.com1.z0.glb.clouddn.com/"



def enter_chatroom(event):
    global topic, contents, win2
    #topic = str(topicWindow.GetValue())

    if username and topic:
        win1.Close()
        mqttc.subscribe(topic, 0)
        thread.start_new(mqttc.loop_forever, ())
        win2 = wx.Frame(None, title="channal: " + topic + "   " + "username: " + username, size=(410, 335))
        recordButton = wx.Button(win2, label="Record", pos=(150, 18), size=(80, 25))
        recordButton.Bind(wx.EVT_BUTTON, recordMessage)
        contents = wx.TextCtrl(win2, pos=(5, 65), size=(390, 260), style=wx.TE_MULTILINE | wx.HSCROLL)
        win2.Show()
    else:
        text3 = wx.StaticText(win1, -1, "Username and password can not be blank.", pos=(20, 5),)
        text3.SetForegroundColour('red')

def register(event):
    global usernameWindow_1, passwordWindow_1, verifyWindow_1, emailWindow_1, win_register
    win_register = wx.Frame(None, title="Register", size=(280, 300))
    r_text1 = wx.StaticText(win_register, -1, "* Username  :", pos=(20, 32))
    r_text2 = wx.StaticText(win_register, -1, "* Password  :", pos=(20, 67))
    r_text3 = wx.StaticText(win_register, -1, "* Verify  :", pos=(20, 102))
    r_text4 = wx.StaticText(win_register, -1, "* Email  :", pos=(20, 137))
    usernameWindow_1 = wx.TextCtrl(win_register, pos=(110, 30), size=(120, 25))
    passwordWindow_1 = wx.TextCtrl(win_register, pos=(110, 65), size=(120, 25), style=wx.TE_PASSWORD)
    verifyWindow_1 = wx.TextCtrl(win_register, pos=(110, 100), size=(120, 25), style=wx.TE_PASSWORD)
    emailWindow_1 = wx.TextCtrl(win_register, pos=(110, 135), size=(120, 25))
    doneButton = wx.Button(win_register, label="Done", pos=(40, 180), size=(80, 25))
    doneButton.Bind(wx.EVT_BUTTON, click_register)
    resetButton = wx.Button(win_register, label="Reset", pos=(150, 180), size=(80, 25))
    resetButton.Bind(wx.EVT_BUTTON, click_reset)
    win_register.Show()

def click_register(event):
    global usernameWindow_1, passwordWindow_1, verifyWindow_1, emailWindow_1, win_register, key
    username_1 = str(usernameWindow_1.GetValue())
    password_1 = str(passwordWindow_1.GetValue())
    verify_1 = str(verifyWindow_1.GetValue())
    email_1 = str(emailWindow_1.GetValue())
    if username_1 and password_1 and verify_1 and email_1 :
        if password_1 == verify_1 :
            key = "user.txt"
            f = open(key, 'wb')
            data = "username:" + username_1 + "#" + "password:" + password_1 + "#" + "emal:" + email_1 + "#" + "\n"
            f.write(data)
            f.close()
            upload(key)
            win_register.Close()
        else:
            notice1 = wx.StaticText(win_register, -1, "Password and verify can not be different.", pos=(12, 220),)
            notice1.SetForegroundColour('red')
    else:
        notice2 = wx.StaticText(win_register, -1, "Information with stars can not be blank.", pos=(12, 220),)
        notice2.SetForegroundColour('red')

def click_reset(event):
    global usernameWindow_1, passwordWindow_1, verifyWindow_1, emailWindow_1
    usernameWindow_1.Clear()
    passwordWindow_1.Clear()
    verifyWindow_1.Clear()
    emailWindow_1.Clear()


topic = ""
username = ""
key = ""
content_show = ""
now = ""



app = wx.App()
win1 = wx.Frame(None, title="Login", size=(380, 160))
text1 = wx.StaticText(win1, -1, "Username  :", pos=(20, 32))
text2 = wx.StaticText(win1, -1, "Password  :", pos=(20, 67))
loginButton = wx.Button(win1, label="Login", pos=(260, 25), size=(80, 25))
loginButton.Bind(wx.EVT_BUTTON, login)
registerButton = wx.Button(win1, label="Register", pos=(260, 60), size=(80, 25))
registerButton.Bind(wx.EVT_BUTTON, register)
usernameWindow = wx.TextCtrl(win1, pos=(110, 30), size=(120, 25))
passwordWindow = wx.TextCtrl(win1, pos=(110, 65), size=(120, 25), style=wx.TE_PASSWORD)
win1.Show()
app.MainLoop()
