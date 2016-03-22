import wx
import ConfigParser
import pyo

class DeviceInfo(wx.Dialog):
    def __init__(self, parent, *args, **kwds):

        wx.Dialog.__init__(self, parent, title="Devices Info...")
    def init(self):
        deviceInfoText=wx.StaticText(self,-1,self.GetDeviceInfoText())
        Grid =wx.BoxSizer(wx.VERTICAL)
        Grid.Add(deviceInfoText,0,0,50)
        self.SetSizer(Grid)
        Grid.Fit(self)
        self.Layout()

    def _GetDevicesDict(self):
        pa_input = pyo.pa_get_input_devices()
        pa_output = pyo.pa_get_output_devices()
        pm_input =  pyo.pm_get_input_devices()
        pm_output = pyo.pm_get_output_devices()
        
        i=0
        pa_input_list=[]
        for d in pa_input[0]:
            pa_input_list.append([i,d])
            i+=1
            
        i=0
        pa_output_list=[]
        for d in pa_output[0]:
            pa_output_list.append([i,d])
            i+=1
            
        i=0
        pm_input_list=[]
        for d in pm_input[0]:
            pm_input_list.append([i,d])
            i+=1
        
        i=0
        pm_output_list=[]
        for d in pm_output[0]:
            pm_output_list.append([i,d])
            i+=1
            
        return {'a_input':pa_input_list,'a_output':pa_output_list,'m_input':pm_input_list,'m_output':pm_output_list}
        
        
    def GetDeviceInfoText(self):
        devices=self._GetDevicesDict()
        text ="\n-----AUDIO IN DEVICES------(adc [n])\n"
        for l in devices['a_input']:
            text+= str(l[0]) + " -> " + str(l[1]) + "\n"
        text+="\n-----AUDIO OUT DEVICES-----(dac [n])\n"
        for l in devices['a_output']:
            text+= str(l[0]) + " -> "+ str(l[1])+ "\n"
        text+="\n------MIDI IN DEVICES------\n"
        for l in devices['m_input']:
            text+= str(l[0])+" -> "+ str(l[1])+ "\n"
        text+="\n-----MIDI OUT DEVICES------\n"
        for l in devices['m_output']:
            text+= str(l[0])+" -> "+ str(l[1])+ "\n"
        return text

class OptionsDlg(wx.Dialog):

    def __init__(self, parent, *args, **kwds):

        wx.Dialog.__init__(self, parent, title="Options...")
        
        self.CB_buffersize = wx.CheckBox(self, wx.ID_ANY, "")
        self.TC_buffersize = wx.TextCtrl(self, wx.ID_ANY, "")    
        
        self.CB_hwbuffersize = wx.CheckBox(self, wx.ID_ANY, "")
        self.TC_hwbuffersize = wx.TextCtrl(self, wx.ID_ANY, "")
        
        self.CB_audioin = wx.CheckBox(self, wx.ID_ANY, "")
        self.TC_audioin = wx.TextCtrl(self, wx.ID_ANY, "")
        
        self.CB_audioout = wx.CheckBox(self, wx.ID_ANY, "")
        self.TC_audioout = wx.TextCtrl(self, wx.ID_ANY, "")

        self.CB_midiin = wx.CheckBox(self, wx.ID_ANY, "")
        self.TC_midiin = wx.TextCtrl(self, wx.ID_ANY, "")
        
        self.CB_midiout = wx.CheckBox(self, wx.ID_ANY, "")
        self.TC_midiout = wx.TextCtrl(self, wx.ID_ANY, "")
        
        self.TC_samplerate = wx.TextCtrl(self, wx.ID_ANY, "")
        self.TC_ksmps = wx.TextCtrl(self, wx.ID_ANY, "")
        self.TC_nchnls = wx.TextCtrl(self, wx.ID_ANY, "")
        self.TC_zerodbfs = wx.TextCtrl(self, wx.ID_ANY, "")
        
        self.devicesDialog=DeviceInfo(self)
        self.devicesButton = wx.Button(self,wx.ID_ANY, "Devices Info")
        self.saveButton = wx.Button(self, wx.ID_ANY, "Save")
        self.Bind(wx.EVT_BUTTON,self.SaveConfig,self.saveButton)
        self.Bind(wx.EVT_BUTTON, self.ShowDevices, self.devicesButton)

        self.__set_properties()
        self.__do_layout()
    
    def SaveConfig(self,e):
        config=ConfigParser.RawConfigParser()
        config.add_section('CsOptions')
        config.set('CsOptions','buffer_size_enable',str(self.CB_buffersize.GetValue()))
        config.set('CsOptions','buffer_size_value',str(self.TC_buffersize.GetValue()))
        config.set('CsOptions','hw_buffer_size_enable', str(self.CB_hwbuffersize.GetValue()))
        config.set('CsOptions','hw_buffer_size_value',str(self.TC_hwbuffersize.GetValue()))
        config.set('CsOptions','audio_in_enable',str(self.CB_audioin.GetValue()))
        config.set('CsOptions','audio_in_value',str(self.TC_audioin.GetValue()))
        config.set('CsOptions','audio_out_enable',str(self.CB_audioout.GetValue()))
        config.set('CsOptions','audio_out_value',str(self.TC_audioout.GetValue()))
        config.set('CsOptions','midi_in_enable',str(self.CB_midiin.GetValue()))
        config.set('CsOptions','midi_in_value',str(self.TC_midiin.GetValue()))
        config.set('CsOptions','midi_out_enable',str(self.CB_midiout.GetValue()))
        config.set('CsOptions', 'midi_out_value', str(self.TC_midiout.GetValue()))
        
        config.add_section('CsInstruments')
        config.set('CsInstruments','sr',str(self.TC_samplerate.GetValue()))
        config.set('CsInstruments','ksmps',str(self.TC_ksmps.GetValue()))
        config.set('CsInstruments','nchnls',str(self.TC_nchnls.GetValue()))
        config.set('CsInstruments','zero_dbfs',str(self.TC_zerodbfs.GetValue()))
        
        with open('ZeeConf.ini', 'wb') as configfile:
            config.write(configfile)
    def ShowDevices(self,e):
        self.devicesDialog.init()
        self.devicesDialog.ShowModal()
    def _SetInitParameters(self):
        config = ConfigParser.RawConfigParser()
        config.read('ZeeConf.ini')
        if config.getboolean('CsOptions', 'buffer_size_enable'):
            self.CB_buffersize.SetValue(1)
            self.TC_buffersize.SetValue(config.get('CsOptions', 'buffer_size_value')) 
        else:
            self.CB_buffersize.SetValue(0)
            
        if config.getboolean('CsOptions', 'hw_buffer_size_enable'):
            self.CB_hwbuffersize.SetValue(1)
            self.TC_hwbuffersize.SetValue(config.get('CsOptions', 'hw_buffer_size_value'))
        else:
            self.CB_hwbuffersize.SetValue(0)
            
        if config.getboolean('CsOptions', 'audio_in_enable'):
            self.CB_audioin.SetValue(1)
            self.TC_audioin.SetValue(config.get('CsOptions','audio_in_value'))
        else:
            self.CB_audioin.SetValue(0)
            
        if config.getboolean('CsOptions', 'audio_out_enable'):
            self.CB_audioout.SetValue(1)
            self.TC_audioout.SetValue(config.get('CsOptions','audio_out_value'))
        else:
            self.CB_audioout.SetValue(0)
            
        if config.getboolean('CsOptions', 'midi_in_enable'):
            self.CB_midiin.SetValue(1)
            self.TC_midiin.SetValue(config.get('CsOptions', 'midi_in_value'))
        else:
            self.CB_midiin.SetValue(0)
            
        if config.getboolean('CsOptions', 'midi_out_enable'):
            self.CB_midiout.SetValue(1)
            self.TC_midiout.SetValue(config.get('CsOptions', 'midi_out_value'))
        else:
            self.CB_midiout.SetValue(0)
    
        self.TC_samplerate.SetValue(config.get('CsInstruments', 'sr'))
        self.TC_ksmps.SetValue(config.get('CsInstruments', 'ksmps'))
        self.TC_nchnls.SetValue(config.get('CsInstruments', 'nchnls'))
        self.TC_zerodbfs.SetValue(config.get('CsInstruments', 'zero_dbfs'))
    
    def _SetToolTips(self):
        self.TC_buffersize.SetToolTipString("Number of audio sample-frames per sound i/o software buffer. Should be set to an integer multiple of ksmps.")
        self.TC_hwbuffersize.SetToolTipString("Number of audio sample-frames held in the DAC hardware buffer.")
        self.TC_audioin.SetToolTipString("Input soundfile name. The value \"adc n\" will request sound from the host audio input device n.")
        self.TC_audioout.SetToolTipString("Output soundfile name. The name \"dac n\"  will request writing sound to the host audio output device n.")
        self.TC_midiin.SetToolTipString("Read MIDI IN events from device n (eg. -M n)")
        self.TC_midiout.SetToolTipString("Read MIDI OUT events from device n (eg. -Q n)")
        self.TC_samplerate.SetToolTipString("Sets the audio sampling rate.")
        self.TC_ksmps.SetToolTipString("Sets the number of audio samples in a control period kr: ksmps=sr/kr")
        self.TC_nchnls.SetToolTipString("Sets the number of channels of audio output.")
        self.TC_zerodbfs.SetToolTipString("Sets the value of 0 decibels using full scale amplitude.")
        
    def __set_properties(self):
        self.SetTitle("Options")
        self._SetInitParameters()
        self._SetToolTips()

    def __do_layout(self):

        Grid = wx.GridSizer(6, 2, 0, 0)
        S_mo = wx.BoxSizer(wx.HORIZONTAL)
        S_mi = wx.BoxSizer(wx.HORIZONTAL)
        S_zerodbfs = wx.BoxSizer(wx.HORIZONTAL)
        S_ao = wx.BoxSizer(wx.HORIZONTAL)
        S_nchnls = wx.BoxSizer(wx.HORIZONTAL)
        S_ai = wx.BoxSizer(wx.HORIZONTAL)
        S_ksmps = wx.BoxSizer(wx.HORIZONTAL)
        S_hwbuffer = wx.BoxSizer(wx.HORIZONTAL)
        S_sr = wx.BoxSizer(wx.HORIZONTAL)
        S_buffer = wx.BoxSizer(wx.HORIZONTAL)
        S_buffer.Add(wx.StaticText(self, wx.ID_ANY, "SW Buffer Size"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_buffer.Add(self.CB_buffersize, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_buffer.Add(self.TC_buffersize, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Grid.Add(S_buffer, 1, wx.EXPAND, 0)
        S_sr.Add(wx.StaticText(self, wx.ID_ANY, "Sample Rate"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_sr.Add(self.TC_samplerate, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Grid.Add(S_sr, 1, wx.EXPAND, 0)
        S_hwbuffer.Add(wx.StaticText(self, wx.ID_ANY, "HW Buffer Size"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_hwbuffer.Add(self.CB_hwbuffersize, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_hwbuffer.Add(self.TC_hwbuffersize, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Grid.Add(S_hwbuffer, 1, wx.EXPAND, 0)
        S_ksmps.Add(wx.StaticText(self, wx.ID_ANY, "Samples per control (srkr)"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_ksmps.Add(self.TC_ksmps, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Grid.Add(S_ksmps, 1, wx.EXPAND, 0)
        S_ai.Add(wx.StaticText(self, wx.ID_ANY, "Audio In"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_ai.Add(self.CB_audioin, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_ai.Add(self.TC_audioin, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Grid.Add(S_ai, 1, wx.EXPAND, 0)
        S_nchnls.Add(wx.StaticText(self, wx.ID_ANY, "N Channels"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_nchnls.Add(self.TC_nchnls, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Grid.Add(S_nchnls, 1, wx.EXPAND, 0)
        S_ao.Add(wx.StaticText(self, wx.ID_ANY, "Audio Out"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_ao.Add(self.CB_audioout, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_ao.Add(self.TC_audioout, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Grid.Add(S_ao, 1, wx.EXPAND, 0)
        S_zerodbfs.Add(wx.StaticText(self, wx.ID_ANY, "0 dbfs"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_zerodbfs.Add(self.TC_zerodbfs, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Grid.Add(S_zerodbfs, 1, wx.EXPAND, 0)
        S_mi.Add(wx.StaticText(self, wx.ID_ANY, "Midi In"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_mi.Add(self.CB_midiin, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_mi.Add(self.TC_midiin, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Grid.Add(S_mi, 1, wx.EXPAND, 0)
        Grid.Add(self.devicesButton, 0, wx.ALL | wx.EXPAND, 5)
        S_mo.Add(wx.StaticText(self, wx.ID_ANY, "Midi Out"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_mo.Add(self.CB_midiout, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        S_mo.Add(self.TC_midiout, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Grid.Add(S_mo, 1, wx.EXPAND, 0)
        Grid.Add(self.saveButton, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(Grid)
        Grid.Fit(self)
        self.Layout()

if __name__ == "__main__":
    class MyPanel(wx.Panel):
        def __init__(self, parent):
            """Constructor"""
            wx.Panel.__init__(self, parent)
            self.filename="Spacer"
            dlg = OptionsDlg(self)
            dlg.ShowModal()
            dlg.Destroy()
    class MyFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, title="Example frame")
            panel = MyPanel(self)
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()