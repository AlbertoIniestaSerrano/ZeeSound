import wx
from zeepanels.sliderPanel import SliderPanel
from zeepanels.knobPanel import KnobPanel
from zeepanels.toggleButtonPanel import ToggleButtonPanel
from zeepanels.imagePanel import ImagePanel
from zeepanels.texteditor import TextEditor

from zeeutilities.ZeeXMLManager import parseXML
#import zeeutilities.xmlgraphic

from zeecontrols.popupctrl import PopUpCtrl
from zeeutilities.xmlgraphic import XMLGraphic

GAP=10
ITEMSIZE=49

class InstrumentPanel(wx.Panel):#Carga los distintos controles o widgets en cada instrumento
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        self.bitmap_background=None
        wx.Panel.__init__(self, *args, **kwds)
    def Create(self,XMLFILENAME):
        
        self.listaElementos,texture_file,graphic_set,self.scale, fontOptions, cSoundFile=parseXML(XMLFILENAME)
        self.bitmap_background=wx.Bitmap(texture_file)
        
        self.filenames={}
        self.filenames['csd']=cSoundFile
        self.filenames['xml']=XMLFILENAME
        
        self.openCSDfile=PopUpCtrl(self, pos=(GAP,GAP))
        self.openXMLfile=PopUpCtrl(self, pos=(GAP+ITEMSIZE,GAP))
        self.updateInsButton=PopUpCtrl(self, pos=(GAP+ITEMSIZE*2,GAP))
        
        self.openCSDfile.SetTexture(wx.Bitmap("img/popup/csd1.png"), wx.Bitmap("img/popup/csd2.png"), self.bitmap_background)
        self.openXMLfile.SetTexture(wx.Bitmap("img/popup/xml1.png"), wx.Bitmap("img/popup/xml2.png"), self.bitmap_background)
        self.updateInsButton.SetTexture(wx.Bitmap("img/popup/update1.png"), wx.Bitmap("img/popup/update2.png"), self.bitmap_background)
        
        self.openCSDfile.Bind(wx.EVT_LEFT_DOWN,self.openCSDeditor)
        self.openXMLfile.Bind(wx.EVT_LEFT_DOWN,self.openXMLeditor2)
        self.updateInsButton.Bind(wx.EVT_LEFT_DOWN,self.updateInstrument)     
        
        self.listaWidgets=[]
        for e in self.listaElementos:
            w=None
            if e.get_wtype() == "slider":
                w=SliderPanel(self,pos=(e.get_pos()[0],e.get_pos()[1]),size=(e.get_span()[0]*self.scale,e.get_span()[1]*self.scale))
                w.SetWidget(e,self.bitmap_background,graphic_set,self.scale,fontOptions)
            elif e.get_wtype() == "knob":
                w=KnobPanel(self,pos=(e.get_pos()[0],e.get_pos()[1]),size=(e.get_span()[0]*self.scale,e.get_span()[1]*self.scale))
                w.SetWidget(e,self.bitmap_background,graphic_set,self.scale,fontOptions)
            elif e.get_wtype() == "button":
                w=ToggleButtonPanel(self,pos=(e.get_pos()[0],e.get_pos()[1]),size=(e.get_span()[0]*self.scale,e.get_span()[1]*self.scale))
                w.SetWidget(e,self.bitmap_background,graphic_set,self.scale,fontOptions)
            elif e.get_wtype() == "image":
                bitmap_image=wx.Bitmap(e.get_colour())
                w=ImagePanel(self,pos=(e.get_pos()[0],e.get_pos()[1]),size=bitmap_image.GetSize())
                w.SetWidget(None, self.bitmap_background,bitmap_image , None, None)

            else:
                w=wx.Button(self, wx.ID_ANY, label="WRONG TYPE WIDGET")
            self.listaWidgets.append(w)
            
        self.BackgroundImageFitter()

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        
        
    def updateInstrument(self,evt):
        self.DestroyChildren()
        self.Create(self.filenames['xml'])
        self.GetParent().ResetCSS()
        
    def openCSDeditor(self,evt):
        self.dialog1=TextEditor(self,self.filenames['csd'])
        try:
            f=open(self.filenames['csd'],"r")
            self.dialog1.control.SetValue(f.read())
        except:
            self.dialog1.control.SetForegroundColour("#FF0000")
            self.dialog1.control.SetValue("Error: archivo \""+self.filenames['csd']+"\" no encontrado")           
        self.dialog1.Show()
        evt.Skip()
        
    def openXMLeditor(self,evt):
        self.dialog2=TextEditor(self,self.filenames['xml'])
        try:
            f=open(self.filenames['xml'],"r")
            text=f.read()
            self.dialog2.control.SetValue(text)
        except:
            self.dialog1.control.SetForegroundColour("#FF0000")
            self.dialog1.control.SetValue("Error: archivo \""+self.filenames['xml']+"\" no encontrado")
        self.dialog2.Show()
        evt.Skip()
    def openXMLeditor2(self,evt):
        self.dialog2=XMLGraphic(self)
        self.dialog2.rellenarCositos(self.filenames['xml'])
        self.dialog2.ShowModal()
        self.dialog2.Destroy()
        evt.Skip()
        
    def BackgroundImageFitter(self):
        ###CODIGO PARA EL FILLER DE IMAGEN, hace que el instrumento sea tan grande como la imagen de fondo
        self.filler=ImagePanel(self)
        image=""
        if image=="":
            fill_image=None
            sizebutton=(1,1)
        else:
            fill_image=wx.Bitmap(image)
            sizebutton = fill_image.GetSize()  
        sizebmp=self.bitmap_background.GetSize()
        self.filler_position=(sizebmp[0]-sizebutton[0],sizebmp[1]-sizebutton[1])
        self.filler.SetPosition(self.filler_position)
        self.filler.SetWidget(None, self.bitmap_background, fill_image, None, None)
        #HASTA AQUI EL FILLER
    
    def OnEraseBackground(self, evt):#PINTA EL FONDO CON LA IMAGEN
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        if self.bitmap_background is not None:
            dc.DrawBitmap(self.bitmap_background, 0, 0)
            
    def SetCSoundSession(self,css):
        for i in self.listaWidgets:
            i.SetCSoundSession(css)
    def GetCSDFileName(self):
        return self.filenames['csd']