import wx
from zeecontrols.sliderctrl_roland import RolandSliderCtrl,VERTICAL,HORIZONTAL
from zeecontrols.sliderctrl_moog import MoogSliderCtrl
from zeecontrols.labelctrl import LabelCtrl
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
class SliderPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(SliderPanel, self).__init__(*args, **kw)
        
        self.name="default"
        self.channel=None

        self.minval=0
        self.defval=0
        self.maxval=100

        self.controllerslider=None
        
        self.css=None
        
    def SetWidget(self,e,bitmap_background,graphic_set,scale,fontOptions): 
        self.bitmap_background=bitmap_background
        self.scale=scale
        controllersize=(e.get_span()[0]*scale,e.get_span()[1]*scale)  
        
        self.name=e.get_label()
        
        self.channel=e.get_channel()
        self.minval=e.get_values()[0]
        self.defval=e.get_values()[1]
        self.maxval=e.get_values()[2]

        if graphic_set=='moog':
            self.controllerslider=MoogSliderCtrl(self, size=controllersize)
        elif graphic_set=='roland':
            self.controllerslider=RolandSliderCtrl(self, size=controllersize)
        else:
            print "no hay set grafico en el xml seleccionado"
            
        self.controllerslider.SetTexture(bitmap_background)
        self.controllerslider.SetColour(e.get_colour())
        
        if e.get_orientation() is wx.VERTICAL:
            self.controllerslider._orientation=VERTICAL
        else:
            self.controllerslider._orientation=HORIZONTAL
        self.controllerslider.SetSize(controllersize)
        
        self.controllerslider._minvalue=self.minval
        self.controllerslider._maxvalue=self.maxval

        self.controllerslider.SetValue(self.defval)

        self.controllerslider.SetLabel(self.name)
        self.controllerslider.Bind(wx.EVT_MOUSE_EVENTS, self.SliderEvents)
        
        self.description=e.get_label()+" ("+str(e.get_channel())+")"

        
        #LABEL
        x_size=self.controllerslider.GetSize()[0]
        y_offset=self.controllerslider.GetSize()[1]
        self.label=LabelCtrl(self,size=(x_size,15))
        self.label.SetOffset(y_offset)
        self.label.SetOptions(self.bitmap_background,fontOptions)
        self.label.SetLabel(self.name)
        ##
        
        self.__set_properties()
        self.__do_layout()
        
    def GetDescriptionText(self):
        return self.description     
        
    def SliderEvents(self, event):
        slider=event.GetEventObject()
        if event.LeftIsDown():   
            self.GetParent().GetParent().ZeeStatusBar.SetStatusText(self.GetDescriptionText()+': '+str(slider.GetValue()))
            
            if self.css is not None:
                self.css.SetChannel(self.channel, slider.GetValue())

        event.Skip()
        
    def __set_properties(self):
        None
        
    def __do_layout(self):
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.controllerslider, 1, wx.EXPAND, 0)
        sizer.Add(self.label,0,wx.EXPAND,5)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()
    
    def SetCSoundSession(self,css):
        self.css=css
        self.css.SetChannel(self.channel, self.defval)
