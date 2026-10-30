import numpy as np

## quick script to calculate Torneträsk Station precipitation

rainRawAlpha = np.loadtxt("smhi-opendata_23_189760_1971_1981.csv", delimiter = ";", skiprows = 10, usecols=(3))
rainRawBeta = np.loadtxt("smhi-opendata_23_189760_198109_199108.csv", delimiter = ";", skiprows = 11, usecols=(3))
rainRawGamma = np.loadtxt("smhi-opendata_23_189760_199108_199505.csv", delimiter = ";", skiprows = 11, usecols=(3))

rainRaw = np.concatenate((rainRawAlpha, rainRawBeta, rainRawGamma))
average = np.sum(rainRaw) / np.shape(rainRaw)[0]
print(f'Average rainfall was {average:.2f}mm')
