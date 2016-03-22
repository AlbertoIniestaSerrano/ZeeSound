import wx
from sliderctrl import SliderCtrl,KC_BUFFERED_DC,HORIZONTAL,VERTICAL

defaultcolour="orange"
PEN_WIDTH_FACTOR=8

class MoogSliderCtrl(SliderCtrl):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_FULL_REPAINT_ON_RESIZE,
                 agwStyle=KC_BUFFERED_DC):
        self.default_slider=False
        self.subBitmap=None
        self.colour=None

        if size==(128,512) or size==(512,128):
            self.bmp_fore=wx.Bitmap("img/sets/moog_opus/slider_fore_512.png")
            self.bmp_fore_size=self.bmp_fore.GetSize()
            
            self.bmp_back=wx.Bitmap("img/sets/moog_opus/slider_back_512.png")
            self.bmp_back_size=self.bmp_back.GetSize()
            
            #self.bmp_plate=wx.Bitmap("img/sets/moog_opus/slider_plate_"+defaultcolour+"_512.png")
            #self.bmp_plate_size=self.bmp_plate.GetSize()
        elif size==(64,256) or size==(256,64):

            self.bmp_fore=wx.Bitmap("img/sets/moog_opus/slider_fore_256.png")
            self.bmp_fore_size=self.bmp_fore.GetSize()
            
            self.bmp_back=wx.Bitmap("img/sets/moog_opus/slider_back_256.png")
            self.bmp_back_size=self.bmp_back.GetSize()
            
            #self.bmp_plate=wx.Bitmap("img/sets/moog_opus/slider_plate_"+defaultcolour+"_256.png")
            #self.bmp_plate_size=self.bmp_plate.GetSize()
        elif size==(32,128) or size==(128,32):

            self.bmp_fore=wx.Bitmap("img/sets/moog_opus/slider_fore_128.png")
            self.bmp_fore_size=self.bmp_fore.GetSize()
            
            self.bmp_back=wx.Bitmap("img/sets/moog_opus/slider_back_128.png")
            self.bmp_back_size=self.bmp_back.GetSize()
            
            #self.bmp_plate=wx.Bitmap("img/sets/moog_opus/slider_plate_"+defaultcolour+"_128.png")
            #self.bmp_plate_size=self.bmp_plate.GetSize()
        else:
            self.default_slider=True

            
        self._agwStyle = agwStyle #Necesario para el BufferedWindow
        SliderCtrl.__init__(self, parent, id, pos, size, agwStyle=agwStyle)
        
    def SetTexture(self,bitmap_background):

        pos=self.GetParent().GetPosition()#La posicion del panel, no del widget
        size=self.GetSize()
        self.subBitmap=bitmap_background.GetSubBitmap(wx.Rect(pos[0],pos[1],size[0],size[1]))

        
    def SetColour(self,colour):
        '''
        if colour is not None:
            size=self.GetSize()
            if size==(128,512) or size==(512,128):
                self.bmp_plate=wx.Bitmap("img/sets/moog_opus/slider_plate_"+colour+"_512.png")
                self.bmp_plate_size=self.bmp_plate.GetSize()
            elif size==(64,256) or size==(256,64):
                self.bmp_plate=wx.Bitmap("img/sets/moog_opus/slider_plate_"+colour+"_256.png")
                self.bmp_plate_size=self.bmp_plate.GetSize()'''
        if colour is None:
            self.colour=None
        else:
            self.colour=colour
            
    def Draw(self, dc):
        if self.default_slider is True:
            SliderCtrl.Draw(self, dc)
            return None
        if self.subBitmap is not None:
            dc.DrawBitmap(self.subBitmap,0,0)

                    
        w,h = self.GetSize() 
        
        t = self.tFromValue(self.GetValue(), self._minvalue, self._maxvalue)
        b=self.bmp_fore_size[1]/2
        pen_width=b/PEN_WIDTH_FACTOR
        
        if self._orientation==HORIZONTAL:
            bmp_new=self.bmp_fore.ConvertToImage().Rotate90().ConvertToBitmap()
            background_new=self.bmp_back.ConvertToImage().Rotate90().ConvertToBitmap()
            dc.DrawBitmap(background_new,0,0)

            pos = int(t * (w-2*b))  
            fix_pos=(self.bmp_back_size[0]-self.bmp_fore_size[0])/2
            dc.DrawBitmap(bmp_new,pos,fix_pos)
            #dc.DrawBitmap(self.bmp_plate,pos,fix_pos)
            #dibuja circulito
            if self.colour is not None:
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.SetPen(wx.Pen(self.colour,1,wx.SOLID))
                dc.DrawCircle(pos+b,fix_pos+b,b)
        else:
            dc.DrawBitmap(self.bmp_back,0,0)
            #cambio para slider vertical
            t=-t+1
            
            pos = int(t * (h-2*b))  
            fix_pos=(self.bmp_back_size[0]-self.bmp_fore_size[0])/2
            dc.DrawBitmap(self.bmp_fore,fix_pos,pos)
            #dc.DrawBitmap(self.bmp_plate,fix_pos,pos)
            #dibuja circulito
            if self.colour is not None:
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.SetPen(wx.Pen(self.colour,1,wx.SOLID))
                dc.DrawCircle(fix_pos+b,pos+b,b)


if __name__ == "__main__":
    class MyFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, -1, "")
            knob1 = MoogSliderCtrl(self, -1,size=(512,512))
            knob1._orientation=VERTICAL
            if knob1._orientation==HORIZONTAL:
                knob1.SetSize((512,128))
            else:
                knob1.SetSize((128,512))
            knob1.SetTags((0,127))
            knob1.SetValue(45)
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            main_sizer.Add(knob1, 0, wx.EXPAND, 0) 
            self.SetSizer(main_sizer)
            main_sizer.SetMinSize((512,512))
            main_sizer.Layout()
    app = wx.App(0)
    frame = MyFrame(None)
    frame.SetSize((128+128,512+32))
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()