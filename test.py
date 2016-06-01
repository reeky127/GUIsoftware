import wx
x="sb"
def load(event):
        global x
        contents.SetValue(x)
        x = x + "sb"
app = wx.App()
win = wx.Frame(None, title="GOOD DAY", size=(410, 335))
loadbutton = wx.Button(win, label="open", pos=(225, 5), size=(80, 25))
loadbutton.Bind(wx.EVT_BUTTON, load)
savebutton = wx.Button(win, label="save", pos=(315, 5), size=(80, 25))
filename = wx.TextCtrl(win, pos=(5, 5), size=(210, 25))
contents = wx.TextCtrl(win, pos=(5, 35), size=(390, 260), style=wx.TE_MULTILINE | wx.HSCROLL)
win.Show()
app.MainLoop()