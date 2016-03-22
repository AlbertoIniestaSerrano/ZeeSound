import wx
from optionsDialog import OptionsDlg
from zeeutilities.xmlgraphic import XMLGraphic

class FirstDialog(wx.Dialog):
    def __init__(self, parent, *args, **kwds):

        wx.Dialog.__init__(self, parent, title="Welcome to ZeeSound")
        self.zeeFileName=''
        self.optDlg=OptionsDlg(self)
        self.bitmap_1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap("zeelogo.png", wx.BITMAP_TYPE_ANY))
        self.Create = wx.Button(self, wx.ID_ANY, label="New ZeeRack")
        self.Select = wx.Button(self, wx.ID_ANY, label="Select ZeeRack")
        self.selected= wx.TextCtrl(self, wx.ID_ANY)
        self.Play = wx.Button(self, wx.ID_ANY, label="Play ZeeRack")
        self.Options = wx.Button(self, wx.ID_ANY, label="Options")
        self.ZSICreator = wx.Button(self, wx.ID_ANY, label="New ZeeInstrument")
        self.Quit = wx.Button(self, wx.ID_ANY, label="Quit")
        
        self.Bind(wx.EVT_BUTTON, self.NewZeeRack, self.Create)
        self.Bind(wx.EVT_BUTTON, self.OnOpen, self.Select)
        self.Bind(wx.EVT_BUTTON, self.OnPlay, self.Play)
        self.Bind(wx.EVT_BUTTON, self.OnOptions, self.Options)
        self.Bind(wx.EVT_BUTTON, self.openXMLeditor2, self.ZSICreator)
        self.Bind(wx.EVT_BUTTON, self.OnQuit, self.Quit)

        self.__set_properties()
        self.__do_layout()
        
    def __set_properties(self):
        self.SetTitle("ZeeSound")

    def __do_layout(self):
        Hsizer = wx.BoxSizer(wx.HORIZONTAL)
        Vsizer = wx.BoxSizer(wx.VERTICAL)
        Hsizer.Add(self.bitmap_1, 0, 0, 0)
        Hsizer.AddSpacer(5)
        
        Vsizer.AddSpacer(5)
        Vsizer.Add(self.Create, 0, wx.EXPAND, 0)
        Vsizer.AddSpacer(5)
        Vsizer.Add(self.Select, 0, wx.EXPAND, 0)
        Vsizer.AddSpacer(2)
        Vsizer.Add(self.selected, 0, wx.EXPAND, 0)
        Vsizer.AddSpacer(10)
        Vsizer.Add(self.Play, 2, wx.EXPAND, 0)
        Vsizer.AddSpacer(50)
        Vsizer.Add(self.Options, 0, wx.EXPAND, 0)
        Vsizer.AddSpacer(5)
        Vsizer.Add(self.ZSICreator, 0, wx.EXPAND, 0)
        Vsizer.AddSpacer(30)
        Vsizer.Add(self.Quit, 0, wx.EXPAND, 0)
        Vsizer.AddSpacer(70)
        Vsizer.Add(wx.StaticText(self,-1,'(C) Alberto Iniesta 2016'))
        
        Hsizer.Add(Vsizer, 1, 0, 0)
        Hsizer.AddSpacer(5)
        self.SetSizer(Hsizer)
        Hsizer.Fit(self)
        self.Layout()
    def GetZeeFileName(self):
        return self.zeeFileName
    
    def OnOpen(self,e):
        self.dirname = ''
        dlgOpen = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.zsr*", wx.OPEN)
        if dlgOpen.ShowModal() == wx.ID_OK:
            self.selected.SetValue(dlgOpen.GetPath())
        dlgOpen.Destroy()
        
    def OnPlay(self,e):
        value=self.selected.GetValue()
        if value=="":
            style=wx.OK|wx.ICON_EXCLAMATION
            dlg = wx.MessageDialog(parent=None, 
                               message="Select one Rack file", 
                               caption="Warning", style=style)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.zeeFileName=value
            self.Close()
    def OnOptions(self,e):
        self.optDlg.ShowModal()
    def NewZeeRack(self,evt):
        print str(evt)
    def openXMLeditor2(self,evt):
        self.dialog2=XMLGraphic(self)
        self.dialog2.ShowModal()
        self.dialog2.Destroy()
        evt.Skip()
        
    def OnQuit(self, e):
        self.Close()
        self.GetParent().GetParent().Destroy()