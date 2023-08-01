import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from scipy import constants as phys_const

import consts
from calc_nphotons import n_photons

def model_curve(t, A, C):
    tau = 140 #value from spec sheet
    #tau: CSA discharge time const. 140 us
    #A: signal slope, mV/us expected when no discharge
    #C: initial value due to crosstalk
    return (C + A*tau)*np.exp(-t/tau) - A*tau

def main(args):
    # Load the CSV file into a Pandas DataFrame, skipping the first row
    df = pd.read_csv(args.infile, skiprows=1)
    time = df['second']*1.0E6 # second to us
    voltage = df['Volt.2']*1000 # volt to milivolt
    
    #Correct offset of voltage at mean of values before signal
    #Uncertainty for each data point is evaluated as std of sideband
    voltage_sideband = voltage[time<-30]
    voltage_offset = voltage_sideband.mean()
    voltage_err = voltage_sideband.std()
    if voltage_err > 1:
        print("Warning: Uncertainty of voltage is",voltage_err,". Please check if it is correct")

    t0 = 10 #fit lower
    t1 = 90 #fit upper
    
    mask = (time>t0) & (time<t1)
    time_fit = time[mask]
    voltage_fit = voltage[mask] - voltage_offset
    
    #Fit waveform
    voltage_errs = np.full(len(time_fit), voltage_err)
    fit_params, fit_cov = curve_fit(model_curve, time_fit, voltage_fit, sigma=voltage_errs, absolute_sigma=True)
    fit_param_errs = np.sqrt(np.diag(fit_cov))
    
    # Calculate the reduced chi-squared (χ²/ndf)
    residuals = voltage_fit - model_curve(time_fit, *fit_params)
    chi_squared = np.sum((residuals / voltage_err) ** 2)
    ndf = len(time_fit) - len(fit_params)
    reduced_chi_squared = chi_squared / ndf

    if args.verbose:
        print("Fitted Parameters:")
        print(" Signal slope :", round(fit_params[0], 5), "±", round(fit_param_errs[0],5), "mV/us")
        print(" Initial value at t=0 :", round(fit_params[1], 3), "±", round(fit_param_errs[1],3), "mV")
        print(" χ²/ndf =", round(reduced_chi_squared, 3))
    
    # Generate points for the fitted curve
    time_bestfit = np.linspace(t0, t1, 1000)  # 1000 points between t0 and t1
    voltage_bestfit = model_curve(time_bestfit, *fit_params) + voltage_offset
    
    # Plot the original data and the fitted curve
    plt.plot(time, voltage, label='Data')
    plt.plot(time_bestfit, voltage_bestfit, 'r-', label='Fitted')
    plt.xlabel('Time [$\mu$s]')
    plt.ylabel('CSA voltage [mV]')
    plt.legend()
    plt.grid(True)
    plt.text(time.iat[0] + (time.iat[-1] - time.iat[0]) * 0.45,
             min(voltage) + (max(voltage) - min(voltage)) * 0.1,
             "Signal slope : "+r'$'+str(round(fit_params[0], 4))+r"\pm"+str(round(fit_param_errs[0],4))+'$'+" mV/$\mu$s",
             color="red")

    # QE calculation
    signal_charge = fit_params[0] * consts.pulse_length * 1.0E-3 \
                    / consts.postamp_gain / consts.CSAgain #pC
    n_pe = signal_charge *1.0E-12 / phys_const.elementary_charge
    QE = n_pe / n_photons
    if args.verbose:
        print("QE =",QE)

    if args.plot == 'f':
        file_name = args.infile.split('/')[-1]
        savefile = "Plots/"+file_name.replace(".csv", ".png")
        plt.savefig(savefile)
    elif args.plot == 's':
        plt.show()

    return QE

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        type = str,
                        help = 'CSV data obtained with oscilloscope')
    parser.add_argument('--plot', '-p',
                        type = str,
                        help = '\'f\': Save fit result plot to plots/ directory,\n \
                                \'s\': Show plot in window')
    parser.add_argument('--verbose', '-v',
                        action = 'store_true',
                        help = 'Print fit information and resultant QE')
    args = parser.parse_args()

    main(args)
