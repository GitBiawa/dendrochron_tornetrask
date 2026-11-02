import numpy as np
import math

## quick script to calculate Torneträsk Station precipitation

rainRawAlpha = np.loadtxt("smhi-opendata_23_189760_1971_1981.csv", delimiter = ";", skiprows = 10, usecols=(3))
rainRawBeta = np.loadtxt("smhi-opendata_23_189760_198109_199108.csv", delimiter = ";", skiprows = 11, usecols=(3))
rainRawGamma = np.loadtxt("smhi-opendata_23_189760_199108_199505.csv", delimiter = ";", skiprows = 11, usecols=(3))

rainRaw = np.concatenate((rainRawAlpha, rainRawBeta, rainRawGamma))
average = np.sum(rainRaw) / np.shape(rainRaw)[0]
print(f'Average rainfall was {average:.2f}mm')

# starting from January
rainRawYearStart = rainRaw[3:]

yearlySums = []
mod = math.floor(np.shape(rainRawYearStart)[0] / 12)

index = 0
for k in range(mod):
    sums = []
    for n in range(12):
        sums = np.append(sums, rainRawYearStart[index])
        index += 1
    yearlySums = np.append(yearlySums, np.sum(sums))

print(f'Average yearly rainfall was {np.average(yearlySums):.2f}mm')
