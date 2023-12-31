# QE_measurement

Fit waveforms taken in oscilloscope in CSV file and calculate QE for photo electron samples.

It can be called like:

```
python fitQE_1sample.py [--plot PLOT] [--verbose] infile.csv
```

Sample CSV file is attached as 20230731-S1_1.csv and the input file should have the same format, or the python code should be modified to match the input format.
When --plot option is selected with 's', the waveform fit result is shown in a window. When --plot with 'f', the result is saved as a PNG file in Data/ directory with the same name with CSV file.
Otherwise, the fit result is not shown.

## Fit and calculate for multiple files

This will process multiple files at one time:

```
python fitQE_samples.py [--plot PLOT] infileList
```

It calculates QE value for each input file, and gives average value of them.
