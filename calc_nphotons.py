import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from scipy import constants as phys_const

import configs

df = pd.read_csv("LEDpattern.txt", comment='#')
df.sort_values(by='angle')
angle = df["angle"].values
intensity = df["relative_intensity"].values
interp_func = interp1d(angle, intensity, kind='linear')

def averaged_intensity(angle):
    if angle < 0 or angle >90:
        print("Error: angle should be in [0,90]")
    firstHalf = interp_func(90 - angle)
    secondHalf = interp_func(90 + angle)
    return (firstHalf + secondHalf) / 2.

def integrate_2d(upper):
    s = 0
    for angle in range(0,round(upper)):
        s += angle * averaged_intensity(angle)
    return s

opening_angle = np.rad2deg( np.arctan(configs.window_diameter / 2. / configs.dist_LED_cathod) )
angle_factor = integrate_2d(opening_angle) / integrate_2d(90)

pulse_energy = configs.pulse_current * configs.efficiency_min * 1.0E-3 * configs.pulse_length * 1.0E-6 #J
photon_energy = phys_const.h * phys_const.c / (configs.wave_length * 1.0E-9) #J
n_photons = pulse_energy * angle_factor / photon_energy
