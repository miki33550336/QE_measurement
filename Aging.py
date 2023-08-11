import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def plot_and_fit(ts, QEs, label="default", color='k', marker='o'):
    ts_hr = [t/60. for t in ts]
    if ts_hr[0] == 0:
        del ts_hr[0]
        del QEs[0]
    plt.plot(ts_hr, QEs, label=label, color=color, marker=marker, linestyle='None')
    
    def fit_func(x, norm, index):
        return norm * np.power(x,index)
    
    result, pcov = curve_fit(fit_func, ts_hr, QEs, p0=[100,-0.5])
    fineX = np.logspace(-0.6, 1.7, 100)
    fineY = [fit_func(xi, result[0], result[1]) for xi in fineX]
    plt.plot(fineX, fineY, ls=':', color=color)
    plt.text(fineX[-1], fineY[-1], "idx: "+str(round(result[1], 2)), 
             color=color, horizontalalignment='left', verticalalignment='center')


# Measurement from Aug. 9
t_Alb = [0., 25., 78., 215., 353., 1333., 1724.]
QE_Alb = [66.1, 35.5, 21.6, 16.3, 14.1, 7.93, 5.93]
t_S4 = [0., 25., 150., 289., 1228., 1662.]
QE_S4 = [57.9, 30.3, 10.3, 7.55, 2.81, 1.97]

#Measurement from Aug.10
t_Zn = [0., 45., 133., 251., 1071.]
QE_Zn = [96.1, 46.1, 28.4, 15.6, 7.06]

plot_and_fit(t_Alb, QE_Alb, "Al", 'r', 'o')
plot_and_fit(t_S4, QE_S4, "Vivid", 'c', 'x')
plot_and_fit(t_Zn, QE_Zn, "Zn", 'b', '^')
plt.xlabel("Time exposed to air after sanding [hrs]")
plt.ylabel(r"QE "+"$[x10^{-7}]$")
plt.semilogx()
plt.semilogy()
#plt.ylim(bottom=0)
plt.legend()
plt.grid(True)
plt.show()
