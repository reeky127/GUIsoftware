# -*- coding: utf-8 -*-
import sys
import urllib
import thread
import urllib2
import json
import qiniu
import recorder
import wx
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
        url = r"http://7xkr9c.com1.z0.glb.clouddn.com/"
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

access_key = 'lo1dTUKUrTcmKtN-LbefdA3vVgHahqr4Bb22JKd5'
secret_key = 'Z2NNqSobYN26Hi22nvyVfaZ4gz3rFVGtWjLNypxS'
bucket_name = 'reeky'
q = qiniu.Auth(access_key, secret_key)

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect("m-lmh5257.myalauda.cn", 53469, 60)

def sendmessage(event):
    global key, content_show, now
    recorder.record_wave()
    key = recorder.FILENAME
    upload(key)
    now = recorder.NOW
    content_show = content_show + now + "\n    " + "message sent successfully" + "\n\n"
    message = {"sender": username, "key": key, "time": now}
    payload = json.dumps(message)
    import paho.mqtt.publish as publish
    publish.single(topic, payload, hostname='m-lmh5257.myalauda.cn', port=53469)
    contents.SetValue(content_show)

def enter(event):
    global topic, username, contents
    topic = str(topicWindow.GetValue())
    username = str(usernameWindow.GetValue())
    win1.Close()
    mqttc.subscribe(topic, 0)
    thread.start_new(mqttc.loop_forever, ())
    win2 = wx.Frame(None, title="channal: " + topic + "   " + "username: " + username, size=(410, 335))
    sendButton = wx.Button(win2, label="Record", pos=(150, 18), size=(80, 25))
    sendButton.Bind(wx.EVT_BUTTON, sendmessage)
    contents = wx.TextCtrl(win2, pos=(5, 65), size=(390, 260), style=wx.TE_MULTILINE | wx.HSCROLL)
    win2.Show()

topic = ""
username = ""
key = ""
content_show = ""
now = ""
app = wx.App()
win1 = wx.Frame(None, title="Enter the channal and username", size=(410, 200))
enterButton = wx.Button(win1, label="enter", pos=(280, 42), size=(80, 25))
enterButton.Bind(wx.EVT_BUTTON, enter)
topicWindow = wx.TextCtrl(win1, pos=(80, 30), size=(180, 25))
usernameWindow = wx.TextCtrl(win1, pos=(80, 65), size=(180, 25))
win1.Show()
app.MainLoop()



