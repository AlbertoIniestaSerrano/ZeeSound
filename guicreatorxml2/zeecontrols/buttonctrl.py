import wx
from wx.lib.agw.knobctrl import BufferedWindow, KC_BUFFERED_DC

class ToggleButtonCtrl(BufferedWindow):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 agwStyle=KC_BUFFERED_DC):

        self._agwStyle = agwStyle
        self._startcolour = wx.WHITE
        self._endcolour = wx.Colour(170, 170, 150)

        self._state = 0
        self._minvalue = 0
        self._maxvalue = 100
        self._trackposition = False
        
        self._buttonON=False
        
        self._agwStyle = agwStyle #Necesario para el BufferedWindow
        BufferedWindow.__init__(self, parent, id, pos, size,
                                style=wx.NO_FULL_REPAINT_ON_RESIZE,
                                agwStyle=agwStyle)

        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvents)
        self.SetValue(self._trackposition)
    
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
            None
        elif self._state == 2 and event.LeftUp():
            self._state = 1

    def SetMinMaxValues(self, tags):
        if min(tags) < self._minvalue:
            self._minvalue = min(tags)
        if max(tags) > self._maxvalue:
            self._maxvalue = max(tags)
        self.OnSize(None)

    def GetMinValue(self):
        return self._minvalue

    def GetMaxValue(self):
        return self._maxvalue

    def Draw (self,dc):
        OUTLINE=(230,230,230)
        w,h = self.GetSize() 
        size=self.GetClientSize()
         
        dc.Clear()
        self.DrawDiagonalGradient(dc, size)
        
        dc.SetBrush(wx.Brush((150,150,150))) 
        dc.SetPen(wx.Pen(OUTLINE, width=2, style=wx.SOLID))
        dc.DrawRectangle(w/4,h/4,w-(w/2),h-(h/2))
        
        if self._buttonON:
            dc.SetBrush(wx.Brush(OUTLINE)) 
            dc.SetPen(wx.Pen((150,150,150), width=2, style=wx.SOLID))
            dc.DrawRectangle(w/4,h/4,w-(w/2),h-(h/2))


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
        if self._buttonON is False:
            self._buttonON=True
            self.SetValue(self._maxvalue)
        else:
            self._buttonON=False
            self.SetValue(self._minvalue)

    def SetValue(self,val):
        if val>(self._maxvalue-self._minvalue)/2:
            self._trackposition = True
        else:
            self._trackposition = False
        self.UpdateDrawing()

    def GetValue(self):
        return self._trackposition
   
if __name__ == "__main__":
    class MyFrame(wx.Frame): 
        def __init__(self, parent):    
            wx.Frame.__init__(self, parent, -1, "")
            panel = wx.Panel(self)
            knob1 = ToggleButtonCtrl(panel, -1, size=(500, 500))
            knob1.SetMinMaxValues((0, 127))
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