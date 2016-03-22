import wx
from zeecontrols.imageCtrl import ImageCtrl

class ImagePanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(ImagePanel, self).__init__(*args, **kw)
        
    def SetWidget(self,e,bitmap_background,bitmap_image,scale, fontOptions):#graphic set se cambia por image
        if bitmap_image is not None:
            self.blankcontroller=ImageCtrl(self, size=bitmap_image.GetSize())
        else:
            self.blankcontroller=ImageCtrl(self)
        self.blankcontroller.SetTexture(bitmap_background, bitmap_image)
        
        self.__do_layout()
        
    def __do_layout(self):       
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.blankcontroller, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()
        
    def SetCSoundSession(self,css):
        None