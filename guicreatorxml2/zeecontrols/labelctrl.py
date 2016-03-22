import wx
from wx.lib.agw.knobctrl import BufferedWindow, KC_BUFFERED_DC

class LabelCtrl(BufferedWindow):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 agwStyle=KC_BUFFERED_DC):

        self.subBitmap=None
        self.fontOptions=None
        self._agwStyle = agwStyle #Necesario para el BufferedWindow
        BufferedWindow.__init__(self, parent, id, pos, size,
                                style=wx.NO_FULL_REPAINT_ON_RESIZE,
                                agwStyle=agwStyle)
    def SetOffset(self,y_offset):#Trae el dato de la altura del control para tenerlo en cuenta al coger el subbitmap
        self.y_offset=y_offset
    def SetOptions(self,bitmap_background,fontOptions):
        self.fontOptions=fontOptions
        pos=self.GetParent().GetPosition()#La posicion del panel, no del widget
        size=self.GetSize()
        try:
            self.subBitmap=bitmap_background.GetSubBitmap(wx.Rect(pos[0],pos[1]+self.y_offset,size[0],size[1]))#AQUI ENTRA EL y_offset
        except:
            print "Fallo con el Layout del instrumento"

    def Draw (self,dc):
        if self.subBitmap is not None:
            dc.DrawBitmap(self.subBitmap,0,0)
        w,h=dc.GetTextExtent(self.GetLabel())
        del h
        if self.fontOptions is not None:
            dc.SetTextForeground(self.fontOptions['color'])
            font=wx.Font(self.fontOptions['size'], self.fontOptions['family'], self.fontOptions['style'], self.fontOptions['weight'])
            dc.SetFont(font)
        
        if self.GetSize()[0]>w:
            dc.DrawText(self.GetLabel(),(self.GetSize()[0]-w)/2,0)
        else:
            dc.DrawText(self.GetLabel(),0,0)


if __name__ == "__main__":
    class MainFrame(wx.Frame): 
        def __init__(self, parent): 
            wx.Frame.__init__(self, parent, -1, "")
            panel = wx.Panel(self)      
            knob1 = LabelCtrl(panel, -1, size=(500, 500))
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            main_sizer.Add(knob1, 0, wx.EXPAND|wx.ALL, 20)
            panel.SetSizer(main_sizer)
            main_sizer.Layout()
    app = wx.App(0)  
    frame = MainFrame(None)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()