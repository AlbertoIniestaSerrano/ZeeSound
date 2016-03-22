#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from zeeutilities.csoundSession import CsoundSession
from zeeutilities.firstDialog import FirstDialog
from zeeutilities.ZeeXMLManager import parseRackXML
from zeeutilities.ZeeCSDManager import ZeeCSDManager

from zeepanels.instrumentPanel import InstrumentPanel

ID_CLOSE=1001
ID_EXIT=1002

def readZeeConf():
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    config.read('ZeeConf.ini')
    options_text=""
    if config.getboolean('CsOptions', 'buffer_size_enable'):
        options_text+=" -b "+config.get('CsOptions', 'buffer_size_value')
    if config.getboolean('CsOptions', 'hw_buffer_size_enable'):
        options_text+=" -B "+config.get('CsOptions', 'hw_buffer_size_value')
    if config.getboolean('CsOptions', 'audio_in_enable'):
        options_text+=" -i "+config.get('CsOptions','audio_in_value')
    else:
        options_text+=" -i adc "
    if config.getboolean('CsOptions', 'audio_out_enable'):
        options_text+=" -o "+config.get('CsOptions','audio_out_value')
    else:
        options_text+=" -o dac "
    if config.getboolean('CsOptions', 'midi_in_enable'):
        options_text+=" -M "+config.get('CsOptions', 'midi_in_value')
    if config.getboolean('CsOptions', 'midi_out_enable'):
        options_text+=" -Q "+config.get('CsOptions', 'midi_out_value')
    instruments_text=""
    instruments_text+="sr="+config.get('CsInstruments', 'sr')+"\n"
    instruments_text+="ksmps="+config.get('CsInstruments', 'ksmps')+"\n"
    instruments_text+="nchnls="+config.get('CsInstruments', 'nchnls')+"\n"
    instruments_text+="0dbfs="+config.get('CsInstruments', 'zero_dbfs')+"\n"
    return options_text,instruments_text
            
class ZeeSound(wx.Frame):#Carga los distintos instrumentos
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle("ZeeSound")
        self.SetSize((500,500))
        self.csdFileList=[]
        
        self.ZeeStatusBar=self.CreateStatusBar()
        filemenu= wx.Menu()
        filemenu.Append(ID_CLOSE, "&Close"," Close ZeeRack")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT, "E&xit"," Exit ZeeSound")
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)
        wx.EVT_MENU(self, ID_CLOSE, self.OnClose)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)

    def init(self):
        dlg = FirstDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
        
        self.insPanelsList=[]
        rack, orientation=parseRackXML(dlg.GetZeeFileName())
        sizer=wx.BoxSizer(orientation)
        for i in rack:#Esta los archivos xml

            panel=InstrumentPanel(self)
            panel.Create(i['file'])
            sizer.Add(panel,0,wx.EXPAND,0)
            self.csdFileList.append(panel.GetCSDFileName())
            self.insPanelsList.append(panel)
            
        self.SetSizer(sizer)
        sizer.Fit(self)
        #self.Layout()
        opt_options, ins_options = readZeeConf()
    
        self.zCSD_m=ZeeCSDManager()
        self.zCSD_m.SetOptions(opt_options, ins_options)
        self.zCSD_m.DecomposeListCSDFiles(self.csdFileList)
        with open("_cmp_.csd","w+") as f:
            f.write(self.zCSD_m.ComposeCSDFile())
        
        self.PassCSoundSession("_cmp_.csd")
        
    def PassCSoundSession(self,cSoundFile):
        self.css=CsoundSession(cSoundFile)
        for i in self.insPanelsList:
            i.SetCSoundSession(self.css)
            
    def ResetCSS(self):#Lo utiliza el botón UPDATE

        self.zCSD_m.DecomposeListCSDFiles(self.csdFileList)
        with open("_cmp_.csd","w+") as f:
            f.write(self.zCSD_m.ComposeCSDFile())
        self.css.resetSession("_cmp_.csd")
        for i in self.insPanelsList:
            i.SetCSoundSession(self.css)
            

    def OnClose(self,evt):
        self.css.stopPerformance()
        for i in self.insPanelsList:
            i.DestroyChildren()
        self.Hide()
        self.init()
        self.Show()
        #print "close"
    def OnExit(self,evt):
        self.css.stopPerformance()
        for i in self.insPanelsList:
            i.DestroyChildren()
        self.DestroyChildren()
        self.Destroy()
        #print "quit"
       
if __name__ == "__main__":
    
    #gettext.install("app")
    app = wx.App(0)
    main_frame = ZeeSound(None, wx.ID_ANY, "", style=wx.TR_DEFAULT_STYLE)
    main_frame.init()
    app.SetTopWindow(main_frame)
    main_frame.SetTitle("ZeeSound")
    main_frame.Show()
    app.MainLoop()
    
        

        