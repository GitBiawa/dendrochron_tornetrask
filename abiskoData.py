import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as spn

## quick script to calculate the min, max, and averages of Abisko Station Data

tempsRaw = np.loadtxt("smhi_simple_2025.csv", skiprows = 1, delimiter = ",")
years = tempsRaw[:,0]

minArray = []
maxArray = []
averageArray = []


index = 0
runningSum = 0
for n in years:
    monthTemps = tempsRaw[index,1:]
    runningSum = runningSum + np.sum(monthTemps)
    minimum = min(monthTemps)
    maximum = max(monthTemps)
    average = np.average(monthTemps)
    minArray = np.append(minArray, minimum)
    maxArray = np.append(maxArray, maximum)
    averageArray = np.append(averageArray, average)
    index += 1
    print(f'{n:.0f}: \tmin. = {minimum}\t|\tmax. = {maximum}\t|\taverage = {average:.3f}')

fullAverage = runningSum / (np.shape(years)[0] * 12)
print(f'Average temp. throughout whole time period: {fullAverage:.2f}°C')

fig, ax = plt.subplots()
ax.plot(years, averageArray)
ax.plot(years, minArray)
ax.plot(years, maxArray)
#plt.show()
plt.close()

print(min(minArray))
print(max(maxArray))

monthlyAverages = []
index = 1
for n in range(12):
    monthlyAverages = np.append(monthlyAverages, np.average(tempsRaw[:,index]))
    index += 1

sigma = 2
gaussian = spn.gaussian_filter(monthlyAverages, sigma)

fig, ax2 = plt.subplots()
ax2.plot(np.linspace(1,12,12), gaussian)
plt.show()
