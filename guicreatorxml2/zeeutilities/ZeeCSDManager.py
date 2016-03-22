from fnmatch import fnmatchcase

OPCODE_KEY_IN="opcode "
OPCODE_KEY_OUT="endop"
MAXSECONDS=36000
SEPARATOR="----------------------"
class ZeeCSDManager():
    def __init__(self):
        self.lista_opcode=[]
        self.lista_instr=[]
        self.lista_csoptions=[]
        self.lista_csscore=[]
        self.lista_csinstroptions=[]
        self.instr_idx=0
        self.opt_options='-f -i adc -o dac\n'
        self.ins_options="sr=48000\nksmps=32\nnchnls=2\n0dbfs=1\n"
    def SetOptions(self,opt_options, ins_options):
        self.opt_options =opt_options
        self.ins_options = ins_options
    def GetOpcodeList(self):
        return self.lista_opcode
    def SetOpcodeList(self,newlist):
        self.lista_opcode=newlist
    def GetInstrList(self):
        return self.lista_instr
    def SetInstrList(self,newlist):
        self.lista_opcode=newlist
    def GetCsOptionsList(self):
        return self.lista_csoptions
    def SetCsOptionsList(self,newlist):
        self.lista_csoptions=newlist
    def GetCsScoreList(self):
        return self.lista_csscore
    def SetCsScoreList(self,newlist):
        self.lista_csscore=newlist
    def GetCsInstrOptionsList(self):
        return self.lista_csinstroptions
    def SetCsInstrOptionsList(self,newlist):
        self.lista_csinstroptions=newlist
    def GetInstrCount(self):
        return self.instr_idx

        
        
    def _extractCSDPart(self,filecontent,key_in,key_out):
        #Extrae la primera ocurrencia de un bloque delimitado por las subcadenas key_in y key_out en la cadena filecontent.
        #Devuelve el bloque extraido y la cadena resultante de dicha extraccion, Respetando las lineas enteras!!!!
        index_in=filecontent.find(key_in)
        if index_in == -1:
            return None, filecontent   
        i=index_in
        while filecontent[i] != "\n" and i>0:
            i-=1
        index_in=i+1
        
        index_out=filecontent.find(key_out)   
        if index_out == -1:
            return None   
        i=index_out
        while filecontent[i] !="\n" and i<=len(filecontent):
            i+=1
        index_out=i
        
        block= filecontent[index_in:index_out+1]
        new_filecontent=filecontent[:index_in]+filecontent[index_out:]
        return block, new_filecontent
    
    def _extractTagContent(self,filecontent,key):##Case Sensitive
        key_in="<"+key+">\n"
        key_out="</"+key+">\n"
        index_in=filecontent.find(key_in)
        index_out=filecontent.find(key_out)
        
        block= filecontent[index_in+len(key_in):index_out-1]
        return block
    def _decomposeCSD(self,csdfile):
        with open(csdfile,"r") as f:
            new_file=f.read()
            
            moreOpcodes=True
            while moreOpcodes:
                opcode, new_file=self._extractCSDPart(new_file, OPCODE_KEY_IN, OPCODE_KEY_OUT)
                if opcode is not None:
                    self.lista_opcode.append(opcode)
                else:
                    moreOpcodes = False

            moreInstr=True
            while moreInstr:
                instr, new_file =self._extractCSDPart(new_file, "instr", "endin")
                if instr is not None:
                    #esto cambia los numeros de instr
                    stringlist=instr.splitlines(True)
                    for i in stringlist:
                        if fnmatchcase(i,'instr *\n'):
                            stringlist[stringlist.index(i)]='instr '+str(self.instr_idx+1)+'\n'
                            self.instr_idx+=1
                    instr=''.join(stringlist)
                    ##
                    
                    self.lista_instr.append(instr)
                else:
                    moreInstr = False
                     
            self.lista_csoptions.append(self._extractTagContent(new_file, "CsOptions"))
            self.lista_csscore.append(self._extractTagContent(new_file, "CsScore"))
            csinstrumentoptions=self._extractTagContent(new_file, "CsInstruments")# lo hace sobre un tag csinstruments ya limpio de instruments
            #asi elimina la multitud de \n
            new=''
            for l in csinstrumentoptions.splitlines(True):
                if l !='\n':
                    new+=l
            csinstrumentoptions=new
            self.lista_csinstroptions.append(new)
    def _BuildBridges(self):
        #puentes de entrada
        for i in range(1,self.GetInstrCount()):
            lineas=self.lista_instr[i].splitlines(True)
            for l in lineas:
                if fnmatchcase(l, '* ins*\n'):
                    index_out=l.find(' ins')
                    variables= l[:index_out].split(',')
                    lineas[lineas.index(l)] = variables[0]+' = '+self.lista_puentes[i-1]['l']+'\n'+variables[1]+' = '+self.lista_puentes[i-1]['r']+'\n'
            self.lista_instr[i]=''.join(lineas)
            
        #puentes de salida
        for i in range(self.GetInstrCount()-1):
            lineas=self.lista_instr[i].splitlines(True)
            for l in lineas:
                if fnmatchcase(l, 'outs *\n'):
                    index_in=l.find('outs ')
                    variables=l[index_in+5:].split(',')
                    lineas[lineas.index(l)] = self.lista_puentes[i]['l']+' = '+variables[0]+'\n'+self.lista_puentes[i]['r']+' = '+variables[1]#no lleva \n porque variables[1]  ya lo lleva
            self.lista_instr[i]=''.join(lineas)
    def _ExtractFunctionTables(self):
        new=[]
        for c in self.lista_csscore:    
            for l in c.splitlines(True):
                if l.startswith('f'):
                    new.append(l)     
        self.lista_csscore=new
    def DecomposeListCSDFiles(self,list_of_csdfiles):
        for c in list_of_csdfiles:
            self._decomposeCSD(c)
        self.lista_puentes=[]
        for i in range(self.GetInstrCount()-1):
            self.lista_puentes.append({'l':'ga'+str(i+1)+'l','r':'ga'+str(i+1)+'r'})
        self._BuildBridges()
        self._ExtractFunctionTables()
    
    def ComposeCSDFile(self):
        self.result='<CsoundSynthesizer>\n<CsOptions>\n'
        self.result+=';contenedor de opciones, dependeran del programa\n'+self.opt_options+"\n"
        self.result+='</CsOptions>\n<CsInstruments>\n'
        self.result+=';opciones de instrumento\n'+self.ins_options
        for i in self.lista_opcode:
            self.result+=i
        for i in self.lista_instr:
            self.result+=i
        self.result+='</CsInstruments>\n<CsScore>\n'
        for i in self.lista_csscore:
            self.result+=i
        for i in range(self.GetInstrCount()):
            self.result+='i'+str(i+1)+' 0 '+str(MAXSECONDS)+'\n'
        self.result+='</CsScore>\n</CsoundSynthesizer>\n'
        
        return self.result
    

if __name__ == "__main__": 
    CSDManager=ZeeCSDManager() 
    CSDManager.DecomposeListCSDFiles(['csd/freqshift.csd'])
    print CSDManager.ComposeCSDFile()
    '''
    for i in CSDManager.GetCsOptionsList():
        print i
    for i in CSDManager.GetCsInstrOptionsList():
        print i
    for i in CSDManager.GetOpcodeList():
        print i
    for i in CSDManager.GetInstrList():
        print i
    for i in CSDManager.GetCsScoreList():
        print i'''

    