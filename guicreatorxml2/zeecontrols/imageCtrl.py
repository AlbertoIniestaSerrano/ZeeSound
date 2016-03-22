import wx
from wx.lib.agw.knobctrl import BufferedWindow, KC_BUFFERED_DC

class ImageCtrl(BufferedWindow):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 agwStyle=KC_BUFFERED_DC):

        self.bitmap_image=None
        self.subBitmap=None

        self._agwStyle = agwStyle #Necesario para el BufferedWindow
        BufferedWindow.__init__(self, parent, id, pos, size,
                                style=wx.NO_FULL_REPAINT_ON_RESIZE,
                                agwStyle=agwStyle)
    def SetTexture(self,bitmap_background,bitmap_image):
        self.bitmap_image=bitmap_image
        pos=self.GetParent().GetPosition()#La posicion del panel, no del widget
        size=self.GetSize()

        if bitmap_background is not None:
            if bitmap_image is not None:
                self.subBitmap=bitmap_background.GetSubBitmap(wx.Rect(pos[0],pos[1],size[0],size[1]))
            else:
                self.subBitmap=bitmap_background.GetSubBitmap(wx.Rect(pos[0],pos[1],1,1))#para el caso de que no haya imagen

    def Draw (self,dc):
        if self.subBitmap is not None:
            dc.DrawBitmap(self.subBitmap,0,0)
        if self.bitmap_image is not None:
            dc.DrawBitmap(self.bitmap_image,0,0)
            #aqui dibujaria la imagen transparente
   
if __name__ == "__main__":
    class MyFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, -1, "")
            panel = wx.Panel(self)   
            knob1 = ImageCtrl(panel, -1, size=(500, 500))
            knob1.SetTexture(None, wx.Bitmap("pruebaspacer.png")) 
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            main_sizer.Add(knob1, 0, wx.EXPAND|wx.ALL, 20)
            panel.SetSizer(main_sizer)
            main_sizer.Layout()    
    app = wx.App(0)
    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()