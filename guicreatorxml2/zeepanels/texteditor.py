##Modified from http://www.wellho.net/resources/ex.php4?item=y207/wx03_02.py

import wx
import os

ID_SAVE=103
ID_BUTTON1=300
ID_EXIT=200


class TextEditor(wx.Frame):
    def __init__(self,parent,title):

        wx.Frame.__init__(self,parent,wx.ID_ANY, title)

        self.control = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE,size=(800,600))
        self.CreateStatusBar()

        filemenu= wx.Menu()
        filemenu.Append(ID_SAVE, "&Save"," Save file")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") 
        self.SetMenuBar(menuBar)  
        
        self.saveCurrentButton=wx.Button(self,-1,"Quick Save and Exit")
        self.saveCurrentButton.Bind(wx.EVT_BUTTON,self.quickSave)

        wx.EVT_MENU(self, ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, ID_SAVE, self.OnSave)
        
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2.Add(self.saveCurrentButton,1,wx.EXPAND)
        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control,1,wx.EXPAND)
        self.sizer.Add(self.sizer2,0,wx.EXPAND)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        self.Show(1)

        self.dirname = ''
    def quickSave(self,e):
        itcontains = self.control.GetValue()
        filehandle=open(self.GetTitle(),'w')#CUTRE FORMA
        filehandle.write(itcontains)
        filehandle.close()
        self.Close(True)

    def OnExit(self,e):
        self.Close(True)

    def OnSave(self,e):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", \
                wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            itcontains = self.control.GetValue()
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            filehandle=open(os.path.join(self.dirname, self.filename),'w')
            filehandle.write(itcontains)
            filehandle.close()
        dlg.Destroy()

if __name__ == "__main__":
    class MyFrame(wx.Frame):
    
        def __init__(self, parent):
        
            wx.Frame.__init__(self, parent,-1, "texteditor Demo")
            knob1 = wx.Button(self, -1)
            knob1.Bind(wx.EVT_BUTTON,self.opentexteditordialog)
            
        def opentexteditordialog(self,evt):
            self.dialog=TextEditor(self,"dialog")
            self.dialog.control.SetValue("El texto al abrir")
            self.dialog.Show()
    
    app = wx.App(0)
    
    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()
    
    app.MainLoop()