import ConfigParser

config=ConfigParser.RawConfigParser()
config.add_section('CsOptions')
config.set('CsOptions','buffer_size_enable','true')
config.set('CsOptions','buffer_size_value','4096')
config.set('CsOptions','hw_buffer_size_enable', 'true')
config.set('CsOptions','hw_buffer_size_value','16384')
config.set('CsOptions','audio_in_enable','true')
config.set('CsOptions','audio_in_value','adc')
config.set('CsOptions','audio_out_enable','true')
config.set('CsOptions','audio_out_value','dac')
config.set('CsOptions','midi_in_enable','false')
config.set('CsOptions','midi_in_value','0')
config.set('CsOptions','midi_out_enable','false')
config.set('CsOptions', 'midi_out_value', '0')

config.add_section('CsInstruments')
config.set('CsInstruments','sr','48000')
config.set('CsInstruments','ksmps','32')
config.set('CsInstruments','nchnls','2')
config.set('CsInstruments','zero_dbfs','1')

with open('ZeeConf.ini', 'wb') as configfile:
    config.write(configfile)
