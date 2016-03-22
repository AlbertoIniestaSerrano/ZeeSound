import wx
from wx.lib.agw.knobctrl import BufferedWindow, KC_BUFFERED_DC

HORIZONTAL=0
VERTICAL=1

class SliderCtrl(BufferedWindow):
   
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 agwStyle=KC_BUFFERED_DC):

        self._startcolour = wx.WHITE
        self._endcolour = wx.Colour(170, 170, 150)
        self._tagscolour = wx.BLACK
        self._tags = []
        self._state = 0
        self._minvalue = 0
        self._maxvalue = 100
        self._trackposition = 0
        
        self._orientation = VERTICAL
        self._agwStyle = agwStyle #Necesario para el BufferedWindow
        BufferedWindow.__init__(self, parent, id, pos, size,
                                style=wx.NO_FULL_REPAINT_ON_RESIZE,
                                agwStyle=agwStyle)

        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvents)
        self.SetValue(self._trackposition)


    ###USADAS INTERNAMENTE
    def interpFloat(self, t, v1, v2): 
        "interpolator for a single value; interprets t in [0-1] between v1 and v2" 
        return (v2-v1)*t + v1 

    def tFromValue(self,value, v1, v2): 
        "returns a t (in range 0-1) given a value in the range v1 to v2" 
        return float(value-v1)/(v2-v1) 

    def clamp(self,v, minv, maxv): 
        "clamps a value within a range" 
        if v<minv: v=minv 
        if v>maxv: v=maxv 
        return v 
    ########
    
    def OnMouseEvents(self, event):

        if self._state == 0 and event.Entering():
            self._state = 1 
        elif self._state >= 1 and event.Leaving():
            self._state = 0 
        elif self._state == 1 and event.LeftDown():
            self._state = 2 
            self._mousePosition = event.GetPosition()
            self.SetTrackPosition() 
        elif self._state == 2 and event.LeftIsDown():
            self._mousePosition = event.GetPosition()
            self.SetTrackPosition() 
        elif self._state == 2 and event.LeftUp():
            self._state = 1

    def SetTags(self, tags):
        
        self._tags = tags
        if min(tags) < self._minvalue:
            self._minvalue = min(tags)

        if max(tags) > self._maxvalue:
            self._maxvalue = max(tags)

        self.OnSize(None)

    def Draw (self,dc):

        OUTLINE=(230,230,230)
        w,h = self.GetSize() 
        size=self.GetClientSize()
        
        dc.Clear()
        self.DrawDiagonalGradient(dc, size)
        if self._tags:
            self.DrawTags(dc, size)

        if self._orientation==HORIZONTAL:
            a=w/15 #lo gordo del slider
            b=w/60 # lo gordo de la aguja del slider
            
            t = self.tFromValue(self.GetValue(), self._minvalue, self._maxvalue) 
            pos = a + int(t * (w-2*a))  
            
            dc.SetBrush(wx.Brush((200,200,200))) 
            dc.SetPen(wx.Pen(OUTLINE, width=2, style=wx.SOLID)) 
            dc.DrawRectangle(pos-a,a/2,2*a,h-a) 
            
            dc.SetBrush(wx.Brush((150,150,150))) 
            dc.SetPen(wx.Pen(OUTLINE, width=2, style=wx.SOLID))
            dc.DrawRectangle(pos-b,a/2,2*b,h-a)
            
        else:
            a=h/15 #lo gordo del slider
            b=h/60 # lo gordo de la aguja del slider
     
            t = self.tFromValue(self.GetValue(), self._minvalue, self._maxvalue) 
            #cambio para slider vertical
            t=-t+1
            
            pos = a + int(t * (h-2*a)) 

            dc.SetBrush(wx.Brush((200,200,200))) 
            dc.SetPen(wx.Pen(OUTLINE, width=2, style=wx.SOLID)) 
            dc.DrawRectangle(a/2,pos-a,w-a,2*a)
            
            dc.SetBrush(wx.Brush((150,150,150))) 
            dc.SetPen(wx.Pen(OUTLINE, width=2, style=wx.SOLID))
            dc.DrawRectangle(a/2,pos-b,w-a,2*b)
    
    def DrawTags(self, dc, size):

        deltarange = abs(self._tags[-1] - self._tags[0])
        width = size.x
        height = size.y

        if self._orientation==HORIZONTAL:
            dimension=width
        else: 
            dimension=height
        coeff=float(dimension)/float(deltarange)
        dcPen = wx.Pen(self._tagscolour, 1)
        for tags in self._tags:
            if tags == self._tags[0] or tags == self._tags[-1]:
                dcPen.SetWidth(-1)
                tagGap = 100
                pass
            elif tags == self._tags[1] or tags == self._tags[-2]:
                dcPen.SetWidth(3)
                tagGap = 10
            else:
                dcPen.SetWidth(1)
                tagGap = 20
                
            dc.SetPen(dcPen)

            pixeldimension=coeff*tags
            #dc.SetBrush(wx.TRANSPARENT_BRUSH)
            if self._orientation == HORIZONTAL:
                dc.DrawLine(pixeldimension,tagGap,pixeldimension,height-tagGap)
            else:
                dc.DrawLine(tagGap,pixeldimension,width-tagGap,pixeldimension)
                
        dcPen.SetWidth(7)
        dcPen.SetColour((80,80,80))
        dc.SetPen(dcPen)
        if self._orientation == HORIZONTAL:
            
            dc.DrawLine(width/30,height/2,width-(width/30),height/2)
        else:
            dc.DrawLine(width/2,height/30,width/2,height-(height/30))   

    def DrawDiagonalGradient(self, dc, size):

        col1 = self._startcolour
        col2 = self._endcolour
        
        r1, g1, b1 = int(col1.Red()), int(col1.Green()), int(col1.Blue())
        r2, g2, b2 = int(col2.Red()), int(col2.Green()), int(col2.Blue())

        maxsize = max(size.x, size.y)
        
        flrect = maxsize
        
        if flrect == 0:
            return

        rstep = float((r2 - r1)) / flrect
        gstep = float((g2 - g1)) / flrect
        bstep = float((b2 - b1)) / flrect

        rf, gf, bf = 0, 0, 0
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
            
        for ii in xrange(0, maxsize, 2):
            currCol = (r1 + rf, g1 + gf, b1 + bf)                
            dc.SetPen(wx.Pen(currCol, 2))
            dc.DrawLine(0, ii+2, ii+2, 0)
            rf = rf + rstep
            gf = gf + gstep
            bf = bf + bstep

        for ii in xrange(0, maxsize, 2):
            currCol = (r1 + rf, g1 + gf, b1 + bf)                
            dc.SetPen(wx.Pen(currCol, 2))
            dc.DrawLine(ii+2, maxsize, maxsize, ii+2)
            rf = rf + rstep
            gf = gf + gstep
            bf = bf + bstep

    def SetTrackPosition(self):
        
        if self._orientation==HORIZONTAL:
            a=self.Width/15#ES igual al ancho del slider

            t = self.tFromValue(self._mousePosition[0], a, self.GetSize()[0]-a) 
        else:
            a=self.Height/15###ES igual al ancho del slider

            t = self.tFromValue(self._mousePosition[1], a, self.GetSize()[1]-a) 
            #cambio para slider vertical
            t=-t+1
        self.SetValue(self.interpFloat(t, self._minvalue, self._maxvalue)) 

    def SetValue(self,val):
        self._trackposition = self.clamp(val, self._minvalue, self._maxvalue) 
        self.UpdateDrawing()

    def GetValue(self):
        return int(self._trackposition)

if __name__ == "__main__":
    class MyFrame(wx.Frame):
        def __init__(self, parent):      
            wx.Frame.__init__(self, parent, -1, "")
            panel = wx.Panel(self)
            knob1 = SliderCtrl(panel, -1, size=(500, 500))
            knob1.SetTags(range(0, 129, 8))
            knob1.SetValue(45)
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            main_sizer.Add(knob1, 0, wx.EXPAND|wx.ALL, 20)
            panel.SetSizer(main_sizer)
            main_sizer.Layout()
    app = wx.App(0) 
    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()