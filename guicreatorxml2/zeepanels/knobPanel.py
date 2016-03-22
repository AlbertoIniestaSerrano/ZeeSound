import wx
from zeecontrols.knobctrl_roland import RolandKnobCtrl
from zeecontrols.knobctrl_moog import MoogKnobCtrl
from zeecontrols.labelctrl import LabelCtrl

#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
class KnobPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(KnobPanel, self).__init__(*args, **kw)
        
        self.name="default"
        self.channel=None

        self.controllerknob=None
        self.minval=0
        self.defval=0
        self.maxval=100
        
        self.css=None
        
    def SetWidget(self,e,bitmap_background,graphic_set,scale,fontOptions):

        controllersize=(e.get_span()[0]*scale,e.get_span()[1]*scale)
        
        self.name=e.get_label()
        
        self.channel=e.get_channel()
        self.minval=e.get_values()[0]
        self.defval=e.get_values()[1]
        self.maxval=e.get_values()[2]

        self.description=e.get_label()+" ("+str(self.channel)+")"
        if graphic_set=='moog':
            self.controllerknob=MoogKnobCtrl(self, size=controllersize)
        elif graphic_set=='roland':
            self.controllerknob=RolandKnobCtrl(self, size=controllersize)
        else:
            print "no hay set grafico en el xml seleccionado"
        
        self.controllerknob.SetTexture(bitmap_background)
        
        self.controllerknob._minvalue=self.minval
        self.controllerknob._maxvalue=self.maxval

        self.controllerknob.Bind(wx.EVT_MOUSE_EVENTS, self.KnobEvents)
        self.controllerknob.SetValue(self.defval)
        
        #LABEL
        x_size=self.controllerknob.GetSize()[0]
        y_offset=self.controllerknob.GetSize()[1]
        self.label=LabelCtrl(self,size=(x_size,15))
        self.label.SetOffset(y_offset)
        self.label.SetOptions(bitmap_background,fontOptions)
        self.label.SetLabel(self.name)
        ##
        
        self.__set_properties()
        self.__do_layout()
    def GetDescriptionText(self):
        return self.description
    
    def KnobEvents(self, event):
        slider=event.GetEventObject()
        if event.LeftIsDown():   
            self.GetParent().GetParent().ZeeStatusBar.SetStatusText(self.GetDescriptionText()+': '+str(slider.GetValue()))
            
            if self.css is not None:
                self.css.SetChannel(self.channel, slider.GetValue())

        event.Skip()
    
    '''def KnobEvents(self,event):#override the OnMouseEvents function in KnobCtrl, very USEFUL! ->Porque no tienes que redefinir KnobCtrl
        knob=event.GetEventObject()
        
        if knob._state == 0 and event.Entering():
            knob._state = 1 
        elif knob._state >= 1 and event.Leaving():
            knob._state = 0 
        elif knob._state == 1 and event.LeftDown():
            knob._state = 2 
            knob._mousePosition = event.GetPosition()
            knob.SetTrackPosition()
        elif knob._state == 2 and event.LeftIsDown():
            knob._mousePosition = event.GetPosition()
            knob.SetTrackPosition() 
            
            knob.GetToolTip().SetTip(str(knob.GetValue()))#Actualiza el ToolTip con el valor actual
            
            self.GetParent().GetParent().ZeeStatusBar.SetStatusText(self.GetDescriptionText()+': '+str(knob.GetValue()))
            if self.css is not None:
                self.css.SetChannel(self.channel, knob.GetValue())

        elif knob._state == 2 and event.LeftUp():
            knob._state = 1
        elif knob._state ==2 and event.RightUp():
            knob._state =1
        #CAPTURA EL EVENTO PARA SI, NO HACE SKIP()'''
    
    def __set_properties(self):
        None
        
    def __do_layout(self):
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.controllerknob, 0, wx.EXPAND, 5)
        sizer.Add(self.label,0,wx.EXPAND,5)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()

    def SetCSoundSession(self,css):
        self.css=css
        self.css.SetChannel(self.channel, self.defval)
