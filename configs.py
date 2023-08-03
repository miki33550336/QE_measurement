### Values from LED data sheet
### https://download.luminus.com/datasheets/Luminus_XST-3535-UV_Datasheet.pdf
wave_length = 275. #nm
efficiency_min = 90./800. #mW/mA
efficiency_max = efficiency_min*45./40. #mW/mA

### Values related to gain
CSAgain = 1.4 #V/pC
postamp_gain = 2.93 #V/V

### Setup configuration
pulse_current = 727 #mA
pulse_length = 100 #us
#dist_LED_cathod = 12 #mm #old_setup
dist_LED_cathod = 7.7 #mm
window_diameter = 7 #mm
