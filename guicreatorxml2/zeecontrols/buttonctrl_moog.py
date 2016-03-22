import wx
from buttonctrl import ToggleButtonCtrl, KC_BUFFERED_DC

class MoogButtonCtrl(ToggleButtonCtrl):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_FULL_REPAINT_ON_RESIZE,
                 agwStyle=KC_BUFFERED_DC, label=""):
        self.default_button=False
        self.subBitmap=None
        self.bmp_back=None
        self.colour=None

        if size==(128,128):
            self.default_button=True
        elif size==(64,64):

            self.bmp_fore_on=wx.Bitmap("img/sets/moog_opus/button_fore_on_64.png")
            self.bmp_fore_size=self.bmp_fore_on.GetSize()
            self.bmp_fore_off=wx.Bitmap("img/sets/moog_opus/button_fore_off_64.png")
            
            self.bmp_back=wx.Bitmap("img/sets/moog_opus/button_back_64.png")
            self.bmp_back_size=self.bmp_back.GetSize()
        else:
            self.default_button=True
        
        self._agwStyle = agwStyle #Necesario para el BufferedWindow
        ToggleButtonCtrl.__init__(self, parent, id, pos, size, agwStyle=agwStyle)
    
    def SetTexture(self,bitmap_background):
        pos=self.GetParent().GetPosition()#La posicion del panel, no del widget
        size=self.GetSize()
        self.subBitmap=bitmap_background.GetSubBitmap(wx.Rect(pos[0],pos[1],size[0],size[1]))

    def SetColour(self,colour):
        if colour is None:
            self.colour='#777777'
        else:
            self.colour=colour
    def Draw(self, dc):
        if self.default_button is True:
            ToggleButtonCtrl.Draw(self, dc)
            return None
        if self.subBitmap is not None:
            dc.DrawBitmap(self.subBitmap,0,0)
            
        w,h = self.GetSize()
        del h
        b=self.bmp_fore_size[0]
        
        #pinta cuadrado de color
        dc.SetBrush(wx.Brush(self.colour,wx.SOLID))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(0,0,self.bmp_back_size[0],self.bmp_back_size[1])
        
        if self._buttonON is True:
            dc.DrawBitmap(self.bmp_fore_on,w/2-b/2,b/2) 
            img=self.bmp_back.ConvertToImage()
            bmp_rotated=img.Rotate180().ConvertToBitmap()
            dc.DrawBitmap(bmp_rotated,0,0)
        else:
            dc.DrawBitmap(self.bmp_back,0,0) 
            dc.DrawBitmap(self.bmp_fore_off,w/2-b/2,b/2)    
   
if __name__ == "__main__":
    class MyFrame(wx.Frame):   
        def __init__(self, parent):        
            wx.Frame.__init__(self, parent, -1, "K")         
            knob1 = MoogButtonCtrl(self, -1,size=(64,64))
            knob1.SetMinMaxValues((0,127))
            knob1.SetValue(45)       
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            main_sizer.Add(knob1, 0, wx.EXPAND, 0)  
            self.SetSizer(main_sizer)
            main_sizer.Layout()
    app = wx.App(0)  
    frame = MyFrame(None)
    frame.SetSize((128+128,512+32))
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()