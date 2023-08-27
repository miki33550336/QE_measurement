import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--relative_qe', '-r', action='store_true',
                    help='Plot QE relative to initial value')
parser.add_argument('--plot_N2', '-n', action='store_true',
                    help='Plot data in N2 purge')
args = parser.parse_args()


def plot_and_fit(ts, QEs_7th, label="default", color='k', marker='o', do_fit=True):
    QEs = [QE*(10**-7) for QE in QEs_7th]
    if args.relative_qe:
        initial_QE = QEs[0]
        QEs = [QE/initial_QE for QE in QEs]
    bef_QE = 0
    if ts[0] == bef_sand:
        bef_QE = QEs[0]
        del ts[0]
        del QEs[0]

    ts_hr = [t/60. for t in ts]
    plt.plot(ts_hr, QEs, label=label, color=color, marker=marker, linestyle='None')
    if ts[0] == aft_sand:
        del ts_hr[0]
        del QEs[0]
    
    def fit_func(x, norm, index):
        return norm * np.power(x,index)
    
    edge_log = 2.7
    edge = np.power(10,edge_log)
    if do_fit:
        result, pcov = curve_fit(fit_func, ts_hr, QEs, p0=[100,-0.5])
        fineX = np.logspace(-0.6, edge_log, 100)
        fineY = [fit_func(xi, result[0], result[1]) for xi in fineX]
        plt.plot(fineX, fineY, ls=':', color=color)
        plt.text(fineX[-1], fineY[-1], "idx: "+str(round(result[1], 2)), 
                 color=color, horizontalalignment='left', verticalalignment='center')

    if bef_QE > 0:
        plt.hlines(bef_QE, aft_sand/60./1.5, edge*7., color=color, linewidth=0.5)


### QE Data
# t[min] and QE[x10^-7]
bef_sand = -1.
aft_sand = 1. #min

# Measurement from Aug. 9
t_Alb = [bef_sand, aft_sand, 25.,  78.,  215., 353.,  1333., 1724., 3133., 7044., 17380.]
QE_Alb= [0.65,     66.1,     35.5, 21.6, 16.3, 14.1,  7.93,  5.93,  3.41,  1.80,  1.08]
t_S4  = [bef_sand, aft_sand, 25.,  150., 289., 1228., 1662., 2961., 6939., 17269., 19895]
QE_S4 = [0.85,     57.9,     30.3, 10.3, 7.55, 2.81,  1.97,  1.38,  1.11,  0.43,   0.37]

# Measurement from Aug.10
t_Zn  = [aft_sand, 45.,  133., 251., 1071., 1542., 5534., 15855.]
QE_Zn = [96.1,     46.1, 28.4, 15.6, 7.06,  4.78,  2.02,  1.13]

# Measurement from Aug.11, partly in vacuum
t_S5  = [bef_sand, aft_sand, 39.,  125., 3978.]
QE_S5 = [0.98,     44.7,     28.9, 17.9, 4.81]

# Measurement from Aug.14, in vacuum
t_S3  = [bef_sand, 12. , 28.,  61.,  1188., 2671., 5535., 9864.] 
QE_S3 = [0.50,     58.2, 43.9, 33.2, 16.4,  14.3,  13.1,  12.2]

# Measurement from Aug.23, in N2
t_B1  = [121., 1689., 2985.]
QE_B1 = [27.0, 18.6,  15.1]
t_S6  = [152., 1652., 2953.]
QE_S6 = [14.0, 6.60,  5.14]
t_B2  = [57.,  352.]
QE_B2 = [22.4, 13.2]
t_S7  = [86.,  381.]
QE_S7 = [16.7, 8.06]
t_B3  = [118.]
QE_B3 = [12.4]

plt.rcParams["font.size"] = 15
bFit = True
if not args.plot_N2:
    plot_and_fit(t_S3, QE_S3, "Vivid S3", 'm', 'v', bFit)
    plot_and_fit(t_S4, QE_S4, "Vivid S4", 'c', 'x', bFit)
    #plot_and_fit(t_S5, QE_S5, "Vivid S5", 'g', '+', bFit)
    plot_and_fit(t_Alb, QE_Alb, "Al", 'r', 'o', bFit)
    plot_and_fit(t_Zn, QE_Zn, "Zn", 'b', '^', bFit)
    plt.xlabel("Time exposed to air after sanding [hrs]")
else:
    plot_and_fit(t_B1, QE_B1, "Vivid B1", 'b', 'o', bFit)
    plot_and_fit(t_S6, QE_S6, "Vivid S6", 'r', 'x', bFit)
    plot_and_fit(t_B2, QE_B2, "Vivid B2", 'c', '+', bFit)
    plot_and_fit(t_S7, QE_S7, "Vivid S7", 'm', 'v', bFit)
    plot_and_fit(t_B3, QE_B3, "Vivid B3", 'g', '^', False)
    plt.xlabel(r"Time exposed to $N_2$ after sanding [hrs]")

if args.relative_qe:
    plt.ylabel("Relative QE")
else:
    plt.ylabel("QE")
plt.semilogx()
plt.semilogy()
#plt.ylim(bottom=0)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
