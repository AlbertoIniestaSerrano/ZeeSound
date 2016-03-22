#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
import ZeeXMLManager

class NewControlPanel(wx.Panel):
    def __init__(self, parent, *args, **kwds):

        wx.Panel.__init__(self, parent)
        
        self.CB_type=wx.ComboBox(self,-1,choices=['slider','knob','button'])
        self.TC_label=wx.TextCtrl(self,-1,value='label')
        self.SC_posx=wx.SpinCtrl(self,-1,size=(60,25),min=-sys.maxint,max=sys.maxint, initial=20)
        self.SC_posy=wx.SpinCtrl(self,-1,size=(60,25),min=-sys.maxint,max=sys.maxint,initial=20)
        self.RB_size=wx.RadioBox(self,-1,choices=['Big ','Small '])
        
        self.SC_minvalue=wx.SpinCtrl(self,-1,size=(75,25),min=-sys.maxint,max=sys.maxint,initial=0)
        self.SC_defvalue=wx.SpinCtrl(self,-1,size=(75,25),min=-sys.maxint,max=sys.maxint,initial=20)
        self.SC_maxvalue=wx.SpinCtrl(self,-1,size=(75,25),min=-sys.maxint,max=sys.maxint,initial=100)
        self.CB_orientation=wx.ComboBox(self,-1,choices=['H','V'],style=wx.CB_READONLY)
        self.CP_ColorPicker=wx.ColourPickerCtrl(self,-1,size=(75,25),style=wx.CLRP_SHOW_LABEL)
        self.TC_csdchannel=wx.TextCtrl(self,-1,value='channel')
        
        self.__set_properties()
        self.__do_layout()
    
    def __set_properties(self):
        None
    def __do_layout(self):
        Vsizer = wx.BoxSizer(wx.VERTICAL)
        
        Hsizer= wx.BoxSizer(wx.HORIZONTAL)
        Hsizer.Add(wx.StaticText(self,-1,'Type'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.CB_type,0,0,0)
        Hsizer.Add(wx.StaticText(self,-1,'Label'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.TC_label,0,0,0)
        Hsizer.Add(wx.StaticText(self,-1,'Pos X Y'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.SC_posx,0,0,0)
        Hsizer.Add(self.SC_posy,0,0,0)
        Hsizer.Add(wx.StaticText(self,-1,'Size'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.RB_size,0,0,0)
        Vsizer.Add(Hsizer, 1, 0, 0)
        
        Hsizer= wx.BoxSizer(wx.HORIZONTAL)
        Hsizer.Add(wx.StaticText(self,-1,'Values: Min:'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.SC_minvalue,0,0,0)
        Hsizer.Add(wx.StaticText(self,-1,'Default:'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.SC_defvalue,0,0,0)
        Hsizer.Add(wx.StaticText(self,-1,'Max:'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.SC_maxvalue,0,0,0)
        Vsizer.Add(Hsizer, 1, 0, 0)
        
        Hsizer= wx.BoxSizer(wx.HORIZONTAL)
        Hsizer.Add(wx.StaticText(self,-1,'Orientation'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.CB_orientation,0,0,0)
        Hsizer.Add(wx.StaticText(self,-1,'Color'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.CP_ColorPicker,0,0,0)
        Hsizer.Add(wx.StaticText(self,-1,'CSD Channel'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.TC_csdchannel,0,0,0)
        Vsizer.Add(Hsizer, 1, 0, 0)
        
        self.SetSizer(Vsizer)
        Vsizer.Fit(self)
        self.Layout()
        
class XMLGraphic(wx.Dialog):
    def __init__(self, parent, *args, **kwds):

        wx.Dialog.__init__(self, parent)
        #declara objetos
        
        ###OBJETOS COMUNES
        self.B_texture_fn=wx.Button(self,-1,"BG Filename")
        self.TC_texture_fn=wx.TextCtrl(self)
        self.CB_graphic_set=wx.ComboBox(self,-1,choices=['moog','roland'],value='moog')
        self.B_csdfile=wx.Button(self,-1,'CSD Filename')
        self.TC_csdfile=wx.TextCtrl(self)
        
        self.SC_fontsize=wx.SpinCtrl(self,-1,size=(75,25),min=-sys.maxint,max=sys.maxint,initial=7)
        self.CB_fontfamily=wx.ComboBox(self,choices=['default','decorative','roman','script','swiss','modern','teletype','max'],value='default')
        self.CB_fontstyle=wx.ComboBox(self,choices=['normal','italic','slant','max'],value='normal')
        self.CB_fontweight=wx.ComboBox(self,choices=['normal','light','bold','max'],value='normal')
        self.ColorPicker=wx.ColourPickerCtrl(self,-1,size=(75,25),style=wx.CLRP_SHOW_LABEL)
        
        #######
        #Aqui se crearan los panel de cada instrumento
        self.listapanelines=[]
        #####
        self.B_addInstrument=wx.Button(self,-1,"+")
        self.B_save=wx.Button(self,-1,"Save")
        #binds
        self.Bind(wx.EVT_BUTTON, self.OnOpenBG, self.B_texture_fn)
        self.Bind(wx.EVT_BUTTON, self.OnOpenCSD, self.B_csdfile)
        self.Bind(wx.EVT_BUTTON,self.AddPanelin,self.B_addInstrument)
        self.Bind(wx.EVT_BUTTON,self.OnSave,self.B_save)
        
        
        self.__set_properties()
        self.__do_layout()
    def AddPanelin(self,e):
        panelin=NewControlPanel(self)
        self.listapanelines.append(panelin)
        self.Vsizer.Add(wx.StaticLine(self),0,wx.ALL|wx.EXPAND,5)
        self.Vsizer.Add(panelin,1,0,0)
        self.Vsizer.Fit(self)
        
        self.Layout()
        self.GetParent().Fit()
    def OnSave(self,e):
        dlgSave=wx.FileDialog(self, "Save As", "", "", "*.zsi", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlgSave.ShowModal() == wx.ID_OK:
            self.XMLSave(dlgSave.GetPath())
            #codigo de salvar
        dlgSave.Destroy()
    def XMLSave(self,filename):
        def prettify(elem):
            """Return a pretty-printed XML string for the Element.
            """
            rough_string = ET.tostring(elem, 'utf-8')
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="  ")
        zee=ET.Element('ZeeInstrument')
        inst_prop=ET.SubElement(zee, 'instrument-properties')
        graphic=ET.SubElement(inst_prop, 'graphic', {'texture':self.TC_texture_fn.GetValue(), 'set':self.CB_graphic_set.GetValue(),\
                                                'fontsize':str(self.SC_fontsize.GetValue()), 'fontfamily':self.CB_fontfamily.GetValue(),\
                                                'fontstyle':self.CB_fontstyle.GetValue(), 'fontweight':self.CB_fontweight.GetValue(),\
                                                'fontcolor':self.ColorPicker.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)})
        scale=ET.SubElement(graphic,'scale')
        scale.text='32'
        csoundfile=ET.SubElement(inst_prop,'csound-file')
        csoundfile.text=self.TC_csdfile.GetValue()
        
        elem=ET.SubElement(zee, 'element-list')
        for i in self.listapanelines:
            widget=ET.SubElement(elem,'widget',{'type':i.CB_type.GetValue(),'label':i.TC_label.GetValue()})
            pos=ET.SubElement(widget, 'pos')
            pos.text=str(i.SC_posx.GetValue())+','+str(i.SC_posy.GetValue())
            span=ET.SubElement(widget, 'span')
            if i.CB_type.GetValue()=='slider':
                if i.RB_size.GetSelection()==0:#Big
                    if i.CB_orientation.GetValue()=='H':
                        span.text='8,2'
                    else:
                        span.text='2,8'
                elif i.RB_size.GetSelection()==1:#Small
                    if i.CB_orientation.GetValue()=='H':
                        span.text='4,1'
                    else:
                        span.text='1,4'
            elif i.CB_type.GetValue()=='knob':
                if i.RB_size.GetSelection()==0:#Big
                    span.text='4,4'
                elif i.RB_size.GetSelection()==1:#Small
                    span.text='2,2'
            elif i.CB_type.GetValue()=='button':
                span.text='2,2'
            #values
            values=ET.SubElement(widget, 'values')
            values.text=str(i.SC_minvalue.GetValue())+','+str(+i.SC_defvalue.GetValue())+','+str(i.SC_maxvalue.GetValue())
            style=ET.SubElement(widget, 'style',{'orientation':i.CB_orientation.GetValue(),\
                                                 'colour':i.CP_ColorPicker.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)})
            csound_instrument=ET.SubElement(widget, 'csound_instrument', {'channel':i.TC_csdchannel.GetValue()})
        with open(filename,'w+') as f:
            f.write(prettify(zee))

    def OnOpenBG(self,e):
        self.dirname = ''
        dlgOpen = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlgOpen.ShowModal() == wx.ID_OK:
            self.TC_texture_fn.SetValue(dlgOpen.GetPath())
        dlgOpen.Destroy()
        
    def OnOpenCSD(self,e):
        self.dirname = ''
        dlgOpen = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.csd", wx.OPEN)
        if dlgOpen.ShowModal() == wx.ID_OK:
            self.TC_csdfile.SetValue(dlgOpen.GetPath())
        dlgOpen.Destroy()
        
    def rellenarCositos(self,filename):
        listaElementos,texture_file,graphic_set,scale,fontOptions,csound_file=ZeeXMLManager.parseXML(filename)
        self.TC_texture_fn.SetValue(texture_file)
        self.CB_graphic_set.SetValue(graphic_set)
        del scale
        self.SC_fontsize.SetValue(int(fontOptions['size']))
        self.ColorPicker.SetColour(fontOptions['color'])
        self.CB_fontfamily.SetValue(ZeeXMLManager._delectorFontFamily(fontOptions['family']))
        self.CB_fontstyle.SetValue(ZeeXMLManager._delectorFontStyle(fontOptions['style']))
        self.CB_fontweight.SetValue(ZeeXMLManager._delectorFontWeight(fontOptions['weight']))
        self.TC_csdfile.SetValue(csound_file)
        for e in listaElementos:
            panelin=NewControlPanel(self)
            panelin.CB_type.SetValue(e.get_wtype())
            panelin.TC_label.SetValue(e.get_label())
            panelin.SC_posx.SetValue(int(e.get_pos()[0]))
            panelin.SC_posy.SetValue(int(e.get_pos()[1]))
            if e.get_wtype()=='slider':
                if e.get_span()==(8,2) or e.get_span()==(2,8):
                    panelin.RB_size.SetSelection(0)
                else:
                    panelin.RB_size.SetSelection(1)
            elif e.get_wtype()=='knob':
                if e.get_span()==(4,4):
                    panelin.RB_size.SetSelection(0)
                else:
                    panelin.RB_size.SetSelection(1)
            else:
                panelin.RB_size.SetSelection(0)
            panelin.SC_minvalue.SetValue(int(e.get_values()[0]))
            panelin.SC_defvalue.SetValue(int(e.get_values()[1]))
            panelin.SC_maxvalue.SetValue(int(e.get_values()[2]))
            print e.get_orientation()
            if e.get_orientation()==wx.HORIZONTAL:
                
                panelin.CB_orientation.SetSelection(0)
            elif e.get_orientation()==wx.VERTICAL:
                panelin.CB_orientation.SetSelection(1)
            else:
                None
            if e.get_colour() is not None:

                panelin.CP_ColorPicker.SetColour(e.get_colour())
            panelin.TC_csdchannel.SetValue(e.get_channel())
            
            self.listapanelines.append(panelin)
            self.Vsizer.Add(wx.StaticLine(self),0,wx.ALL|wx.EXPAND,5)
            self.Vsizer.Add(panelin,1,0,0)
            self.Vsizer.Fit(self)
        
            self.Layout()
            self.GetParent().Fit()
        
        
        
    def __set_properties(self):
        None
    def __do_layout(self):
        self.Vsizer = wx.BoxSizer(wx.VERTICAL)
        
        Hsizer = wx.BoxSizer(wx.HORIZONTAL)       
        Hsizer.Add(self.B_texture_fn,0,0,0)
        Hsizer.Add(self.TC_texture_fn,0,0,0)
        Hsizer.Add(wx.StaticText(self,-1,'    Graphic Set    '),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.CB_graphic_set,0,0,0)
        Hsizer.Add(self.B_csdfile,0,0,0)
        Hsizer.Add(self.TC_csdfile,0,0,0)
        self.Vsizer.Add(Hsizer, 0, 0, 0)
        
        
        
        Hsizer = wx.BoxSizer(wx.HORIZONTAL)
        Hsizer.Add(wx.StaticText(self,-1,'Font: Size'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.SC_fontsize,0,0,0)
        Hsizer.Add(wx.StaticText(self, -1, 'Family'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.CB_fontfamily,0,0,0)
        Hsizer.Add(wx.StaticText(self, -1, 'Style'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.CB_fontstyle,0,0,0)
        Hsizer.Add(wx.StaticText(self, -1, 'Weight'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.CB_fontweight,0,0,0)
        Hsizer.Add(wx.StaticText(self, -1, 'Color'),0,wx.ALL|wx.EXPAND,5)
        Hsizer.Add(self.ColorPicker,0,0,0)
        self.Vsizer.Add(Hsizer, 0, 0, 0)
        
        self.Vsizer.Add(wx.StaticLine(self),0,wx.ALL|wx.EXPAND,5)
        Hsizer = wx.BoxSizer(wx.HORIZONTAL)
        Hsizer.Add(self.B_addInstrument,0,0,0)
        Hsizer.Add(self.B_save,0,wx.ALL|wx.EXPAND,5)
        self.Vsizer.Add(Hsizer, 0, 0, 0)
        
        #aqui añadimos panelines
        for i in self.listapanelines:
            None
        
        self.SetSizer(self.Vsizer)
        self.Vsizer.Fit(self)
        self.Layout()
        #self.GetParent().Fit()
        
'''
if __name__ == "__main__":
    class MyFrame(wx.Frame):
        def __init__(self, parent):      
            wx.Frame.__init__(self, parent, -1, "")
            panel = XMLGraphic(self)
            panel.rellenarCositos('E:\EclipseWS_64\guicreatorxml2\useless\pruebasmalas\\test8.xml')


            #main_sizer = wx.BoxSizer(wx.VERTICAL)
            #main_sizer.Add(knob1, 0, wx.EXPAND|wx.ALL, 20)
            #panel.SetSizer(main_sizer)
            #main_sizer.Layout()
    app = wx.App(0) 
    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()'''
if __name__ == "__main__":
    class MyPanel(wx.Panel):
        def __init__(self, parent):
            """Constructor"""
            wx.Panel.__init__(self, parent)
            self.filename='E:\EclipseWS_64\guicreatorxml2\useless\pruebasmalas\\test8.xml'
            dlg = XMLGraphic(self)
            dlg.rellenarCositos(self.filename)
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