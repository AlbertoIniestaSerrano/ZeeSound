import wx
from wx.lib.agw.knobctrl import KnobCtrl,KC_BUFFERED_DC
import math

class RolandKnobCtrl(KnobCtrl):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_FULL_REPAINT_ON_RESIZE,
                 agwStyle=KC_BUFFERED_DC):
        self.default_knob=False
        self.subBitmap=None
        
        if size==(256,256):
            self.bmp_back=wx.Bitmap("img/sets/roland_juno/knob_back_256.png")
            self.bmp_fore=wx.Bitmap("img/sets/roland_juno/knob_fore_256.png")
            self.bmp_plate=wx.Bitmap("img/sets/roland_juno/knob_plate_256.png")
        elif size == (128,128):
            self.bmp_back=wx.Bitmap("img/sets/roland_juno/knob_back_128.png")
            self.bmp_fore=wx.Bitmap("img/sets/roland_juno/knob_fore_128.png")
            self.bmp_plate=wx.Bitmap("img/sets/roland_juno/knob_plate_128.png")
        elif size == (64,64):
            self.bmp_back=wx.Bitmap("img/sets/roland_juno/knob_back_64.png")
            self.bmp_fore=wx.Bitmap("img/sets/roland_juno/knob_fore_64.png")
            self.bmp_plate=wx.Bitmap("img/sets/roland_juno/knob_plate_64.png")
        else:
            self.default_knob=True
        self._agwStyle = agwStyle #Necesario para el BufferedWindow
        KnobCtrl.__init__(self, parent, id, pos, size, agwStyle=agwStyle)
        self._anglestart = -45
        self._angleend = 225
        
    def SetTexture(self,bitmap_background):
        pos=self.GetParent().GetPosition()#La posicion del panel, no del widget
        size=self.GetSize()
        self.subBitmap=bitmap_background.GetSubBitmap(wx.Rect(pos[0],pos[1],size[0],size[1]))

        
    def tFromValue(self,value, v1, v2): 
        "returns a t (in range 0-1) given a value in the range v1 to v2" 
        return float(value-v1)/(v2-v1) 
    def Draw(self, dc):
        if self.default_knob is True:
            KnobCtrl.Draw(self,dc)
            return None
        if self.subBitmap is not None:
            dc.DrawBitmap(self.subBitmap,0,0)

        bb=(self.GetSize()[0]-self.bmp_back.GetSize()[0])/2
        dc.DrawBitmap(self.bmp_back,bb,bb)

        t = self.tFromValue(self.GetValue(), self._minvalue, self._maxvalue) 
        angulo_rotacion=7*math.pi/4-3*math.pi*t/2 # 0 corresponde a 315 grados y 127 a 45 grados
               
        s=self.bmp_fore.GetSize()
        b=(self.bmp_back.GetSize()[0]-s[0])/2 #borde entre knob y fondo

        # c es el hueco que tiene que dejar el cuadro al rotar
        c=math.fabs(math.sin(angulo_rotacion*2)*((math.sqrt(2)-1)/2)*s[0]) # doble frecuencia y valor absoluto
        c=int(round(c))
        
        img=self.bmp_fore.ConvertToImage()#*
        img2=img.Rotate(angulo_rotacion+math.pi, (0,0),True)
        bmp2=img2.ConvertToBitmap() #*
        
        dc.DrawBitmap(bmp2,bb+b-c,bb+b-c) #*
        
if __name__ == "__main__":
    class MyFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, -1, "")
            knob1 = RolandKnobCtrl(self, -1, size=(256, 256))
            knob1.SetTags(range(0, 128, 8))
            knob1.SetAngularRange(-45, 225)
            knob1.SetValue(45)
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            main_sizer.Add(knob1, 0, wx.EXPAND, 0)
            self.SetSizer(main_sizer)
            main_sizer.SetMinSize((256,256))
            main_sizer.Layout()
    app = wx.App(0)  
    frame = MyFrame(None)
    frame.SetSize((256+8,256+32))
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()