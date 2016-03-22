import wx
from wx.lib.agw.knobctrl import BufferedWindow, KC_BUFFERED_DC

class PopUpCtrl(BufferedWindow):
    
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=(49,32),
                 agwStyle=KC_BUFFERED_DC):

        self._state = 0
        self._trackposition = False
        
        self._buttonON=False
        self.subBitmap=None
        self.img1=None
        self._agwStyle = agwStyle #Necesario para el BufferedWindow
        BufferedWindow.__init__(self, parent, id, pos, size,
                                style=wx.NO_FULL_REPAINT_ON_RESIZE,
                                agwStyle=agwStyle)

        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvents)
    
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
            self.SetTrackPosition()
        event.Skip()

    def Draw (self,dc):
         
        dc.Clear()
        if self.subBitmap is not None:
            dc.DrawBitmap(self.subBitmap,0,0)
        if (self.img1 is not None) and (self.img2 is not None):
            if self._buttonON:
                dc.DrawBitmap(self.img2,0,0)
            else:
                dc.DrawBitmap(self.img1,0,0)

    def SetTrackPosition(self):
        if self._buttonON is False:
            self._buttonON=True
            self.UpdateDrawing()
        else:
            self._buttonON=False
            self.UpdateDrawing()

    def GetValue(self):
        return self._trackposition
    
    def SetTexture(self,img1, img2,bitmap_background):
        pos=self.GetPosition()#La posicion del panel, no del widget
        size=self.GetSize()
        self.img1=img1
        self.img2=img2

        if bitmap_background is not None:
            self.subBitmap=bitmap_background.GetSubBitmap(wx.Rect(pos[0],pos[1],size[0],size[1]))
            self.UpdateDrawing()

if __name__ == "__main__":
    class MyFrame(wx.Frame):
        def __init__(self, parent):  
            wx.Frame.__init__(self, parent, -1, "")
            panel = wx.Panel(self)
            knob1 = PopUpCtrl(panel, -1)
            knob1.SetTexture(wx.Bitmap("img/ms20.jpg"))
    app = wx.App(0)
    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()