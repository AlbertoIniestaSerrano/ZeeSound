#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import xml.etree.ElementTree as ET

#===============================================================================
# <tag attrib=attrib.get>text</tag>
#===============================================================================

class ElementoXML():

    def __init__(self, wtype, label, pos, span, values, orientation, colour, channel):
        self.__wtype = wtype
        self.__label = label
        self.__pos = pos
        self.__span = span
        self.__values = values
        self.__orientation = orientation
        self.__colour = colour
        self.__channel = channel

    def get_wtype(self):
        return self.__wtype

    def get_label(self):
        return self.__label

    def get_pos(self):
        return self.__pos

    def get_span(self):
        return self.__span

    def get_values(self):
        return self.__values

    def get_orientation(self):
        return self.__orientation


    def get_colour(self):
        return self.__colour


    def get_channel(self):
        return self.__channel



    
def _selectorFontFamily(name):
    if name == 'unknown':
        return wx.FONTFAMILY_UNKNOWN
    elif name == 'decorative':
        return wx.FONTFAMILY_DECORATIVE
    elif name == 'roman':
        return wx.FONTFAMILY_ROMAN
    elif name == 'script':
        return wx.FONTFAMILY_SCRIPT
    elif name == 'swiss':
        return wx.FONTFAMILY_SWISS
    elif name == 'modern':
        return wx.FONTFAMILY_MODERN
    elif name == 'teletype':
        return wx.FONTFAMILY_TELETYPE
    elif name == 'max':
        return wx.FONTFAMILY_MAX
    else:
        return wx.FONTFAMILY_DEFAULT
def _selectorFontStyle(name):
    if name == 'italic':
        return wx.FONTSTYLE_ITALIC
    elif name == 'slant':
        return wx.FONTSTYLE_SLANT
    elif name == 'max':
        return wx.FONTSTYLE_MAX
    else:
        return wx.FONTSTYLE_NORMAL
def _selectorFontWeight(name):
    if name == 'light':
        return wx.FONTWEIGHT_LIGHT
    elif name == 'bold':
        return wx.FONTWEIGHT_BOLD
    elif name == 'max':
        return wx.FONTWEIGHT_MAX
    else:
        return wx.FONTWEIGHT_NORMAL
    
#---------------------------
def _delectorFontFamily(name):
    if name == wx.FONTFAMILY_UNKNOWN:
        return 'unknown'
    elif name == wx.FONTFAMILY_DECORATIVE:
        return 'decorative'
    elif name == wx.FONTFAMILY_ROMAN:
        return 'roman'
    elif name == wx.FONTFAMILY_SCRIPT:
        return 'script'
    elif name == wx.FONTFAMILY_SWISS:
        return 'swiss'
    elif name == wx.FONTFAMILY_MODERN:
        return 'modern'
    elif name == wx.FONTFAMILY_TELETYPE:
        return 'teletype'
    elif name == wx.FONTFAMILY_MAX:
        return 'max'
    else:
        return wx.FONTFAMILY_DEFAULT
def _delectorFontStyle(name):
    if name == wx.FONTSTYLE_ITALIC:
        return 'italic'
    elif name == wx.FONTSTYLE_SLANT:
        return 'slant'
    elif name == wx.FONTSTYLE_MAX:
        return 'max'
    else:
        return 'normal'
def _delectorFontWeight(name):
    if name == wx.FONTWEIGHT_LIGHT:
        return 'light'
    elif name == wx.FONTWEIGHT_BOLD:
        return 'bold'
    elif name == wx.FONTWEIGHT_MAX:
        return 'max'
    else:
        return 'normal'
#-------------------------    

def parseRackXML(RackXMLFileName):
    from wx import VERTICAL, HORIZONTAL
    root = ET.parse(RackXMLFileName).getroot()
    listaInstrumentos=[]
    orientation=VERTICAL
    if root.get('orientation') == "H":
        orientation=HORIZONTAL
    for n in root.iter("instrument"):
        dict={}
        dict['name']=n.get('name')
        dict['file']=n.get('file')
        listaInstrumentos.append(dict)
    return listaInstrumentos, orientation
def parseXML(XMLfilename):
    '''
    text=""
    with open(XMLfilename) as f:
        write=False
        for line in f:
            if "<ZeeInstrument>" in line:
                write=True
            if write:
                text+=line
            else:
                break
            if "</ZeeInstrument>" in line:
                write=False
    '''

    root = ET.parse(XMLfilename).getroot()
    listaElementos=[]

    i=root.find('instrument-properties')
    if i is not None:
        texture_file=i.find('graphic').get('texture')
        graphic_set=i.find('graphic').get('set')
        scale= int(i.find('graphic').find('scale').text)
        fontOptions={}
        try:
            fontOptions['size']=int(i.find('graphic').get('fontsize'))
        except:
            fontOptions['size']=7
        try:
            fontOptions['color']=i.find('graphic').get('fontcolor')
        except:
            fontOptions['color']='#000000'
        #estos incluyen su "por si acaso"
        fontOptions['family']=_selectorFontFamily(i.find('graphic').get('fontfamily'))
        fontOptions['style']=_selectorFontStyle(i.find('graphic').get('fontstyle'))
        fontOptions['weight']=_selectorFontWeight(i.find('graphic').get('fontweight'))
    else:
        texture_file='leather'
        scale=32
    #instrument_number=int(i.find('instrument').text)
    csound_file=i.find('csound-file').text
    for n in root.iter('widget'):
        wtype=None
        label=None
        pos=(0,0)
        span=(0,0)
        values=(0,0,100)#min, def, max
        orientation=None
        colour=None
        channel=None
        
        wtype= n.get('type')
        label = n.get('label')
        
        pos=tuple(map(int,n.find('pos').text.split(',')))
        elem_span=n.find('span')
        if elem_span is not None:
            span=tuple(map(int,elem_span.text.split(',')))
        
        elem_values=n.find('values')
        if elem_values is not None:
            #map aplica la funcion int a los elementos de la lista, creada haciendo split por comas al texto del elemento values del xml
            values=tuple(map(int,elem_values.text.split(',')))
        
    
        style_elem=n.find('style')   
        if style_elem is not None:
            textorientation = style_elem.get('orientation')
            colour= style_elem.get('colour')
            if textorientation == 'V':
                orientation=wx.SL_VERTICAL
            elif textorientation == 'H':
                orientation=wx.SL_HORIZONTAL
                
        csound_elem=n.find('csound_instrument')
        if csound_elem is not None:
            channel=csound_elem.get('channel')
        
        listaElementos.append(ElementoXML(wtype, label, pos, span, values, orientation, colour, channel))
        
    return listaElementos,texture_file,graphic_set,scale,fontOptions,csound_file

