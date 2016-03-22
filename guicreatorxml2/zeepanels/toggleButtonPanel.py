import wx
from zeecontrols.buttonctrl_roland import RolandButtonCtrl
from zeecontrols.buttonctrl_moog import MoogButtonCtrl
from zeecontrols.labelctrl import LabelCtrl

#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
class ToggleButtonPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(ToggleButtonPanel, self).__init__(*args, **kw)
        self.name="default"
        self.channel=None

        self.controllerbutton=None
        self.minval=0
        self.maxval=100
        self.defval=0
        
        self.css=None
        
    def SetWidget(self,e,bitmap_background,graphic_set,scale,fontOptions):
        self.scale=scale
        controllersize=(e.get_span()[0]*scale,e.get_span()[1]*scale)
        self.bitmap_background=bitmap_background
        self.name=e.get_label()
        
        self.channel=e.get_channel()
        self.minval=e.get_values()[0]
        self.defval=e.get_values()[1]
        self.maxval=e.get_values()[2]
        self.description=e.get_label()+" ("+str(e.get_channel())+")"
        
        if graphic_set=='moog':
            self.controllerbutton=MoogButtonCtrl(self, label=self.name, size=controllersize)
        elif graphic_set=='roland':
            self.controllerbutton=RolandButtonCtrl(self, label=self.name, size=controllersize)
        else:
            print "no hay set grafico en el xml seleccionado"
        self.controllerbutton.SetTexture(bitmap_background)
        self.controllerbutton.SetColour(e.get_colour())
        
        self.controllerbutton.Bind(wx.EVT_MOUSE_EVENTS, self.ButtonEvents)
        if self.defval>((self.maxval+self.minval)/2):
            self.controllerbutton.SetValue(True)
        else:
            self.controllerbutton.SetValue(False)

        #LABEL
        x_size=self.controllerbutton.GetSize()[0]
        y_offset=self.controllerbutton.GetSize()[1]
        self.label=LabelCtrl(self,size=(x_size,15))
        self.label.SetOffset(y_offset)
        self.label.SetOptions(self.bitmap_background,fontOptions)
        self.label.SetLabel(self.name)
        ##
        
        self.__set_properties()
        self.__do_layout()     
    def GetDescriptionText(self):
        return self.description
    
    def SetReturnParameters(self,name, channel, defval, current_value, tooltipOn):
        self.name=name
        self.channel=channel
        self.defval=int(defval)
        if  current_value == "True":
            self.controllerbutton.SetValue(True)
        else:
            self.controllerbutton.SetValue(False)
        self.description=name+"_"+str(channel)
        
    def ButtonEvents(self, event):
        button=event.GetEventObject()

        if event.LeftIsDown():
            if button.GetValue():
                self.GetParent().GetParent().ZeeStatusBar.SetStatusText(self.GetDescriptionText()+': '+str(button.GetValue()))
                if self.css is not None:
                    self.css.SetChannel(self.channel, self.minval)
                
            else:
                self.GetParent().GetParent().ZeeStatusBar.SetStatusText(self.GetDescriptionText()+': '+str(button.GetValue()))
                if self.css is not None:
                    self.css.SetChannel(self.channel, self.maxval)
            
        event.Skip()
        
    def __set_properties(self):
        None
        
    def __do_layout(self):
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.controllerbutton, 0, wx.EXPAND, 5)
        sizer.Add(self.label,0,wx.EXPAND,5)
        self.SetSizer(sizer)  
        sizer.Fit(self)
        self.Layout()

    def SetCSoundSession(self,css):
        self.css=css
