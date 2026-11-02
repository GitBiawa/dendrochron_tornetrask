import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

## Big Mess of Code Analyzing Tree Ring Width Indices in the Torneträsk Region
## plt.show() commented out for ease of use. can be subbed with plt.savefig() depending on requirements

monthlyTempsAbisko = np.loadtxt("smhi_simple_2025.csv", skiprows=1, delimiter = ",")
treeRingMaster = np.loadtxt("TRN_Master.txt", skiprows=1)

tempYears = monthlyTempsAbisko[:,0]
averageJA = (monthlyTempsAbisko[:,7]) 

treeYears = treeRingMaster[:,0]
treeRaw = treeRingMaster[:,4]
treeNum = treeRingMaster[:,1]

## GRAPH MAKING


## Raw results against tree number
fig, ax = plt.subplots()
ax.plot(treeYears, treeRaw, color='darkorchid')

ax.set(xlabel='Year (CE)', ylabel='Tree Ring Index',
       title='Torneträsk 2026 data')

ax2 = ax.twinx()
ax2.set(ylabel='Number of trees sampled')
ax2.plot(treeYears, treeNum, color='darkcyan')

ax.grid()
#plt.show()
plt.close()


year = 2025
index = 1
rSquaredVals = []
dataLength = np.shape(averageJA)[0]
treeLength = np.shape(treeRaw)[0]
for n in averageJA:
    trees = treeRaw[treeLength - index - 1:treeLength - 1]
    temps = averageJA[dataLength - index:]
    rValue = np.corrcoef(trees, temps)[0,1]
    rSquaredVals = np.append(rSquaredVals, (rValue * rValue))
    index += 1
    year -= 1

rSquaredVals = rSquaredVals[1:]
xLine = 2025 - np.linspace(0,np.shape(rSquaredVals)[0], num = np.shape(rSquaredVals)[0])
#plt.plot(xLine, rSquaredVals)
#plt.show()
# we established here that the R² value stabilized if you go back to ~2012, and 1969 is a nice place to measure before it drops off

targetYear = 2025 - 1969 + 1
treeIndices1969 = treeRaw[treeLength - targetYear - 1:treeLength - 1]
temps1969 = averageJA[dataLength - targetYear:]
fit1969 = np.polyfit(treeIndices1969, temps1969, 1)
yAxis1969 = [fit1969[0] * n + fit1969[1] for n in treeIndices1969]
rValue = np.corrcoef(treeIndices1969, temps1969)[0,1]
rSquared1969 = rValue * rValue
print(f'R² of section 1969 is {rSquared1969}')

fig, ax9 = plt.subplots()
ax9.plot(treeIndices1969, yAxis1969, color='darkcyan', label=f'y = {fit1969[0]:.3f}x + {fit1969[1]:.3f}\nR² = {rSquared1969:.3f}')
plt.scatter(treeIndices1969, temps1969)
ax9.set(xlabel='Tree Ring Index', ylabel='July temperatures (°C)', title='Variable Correlation for 1969 to 2025 period')
ax9.legend()
ax9.grid()
#plt.show()
plt.close()


## Variable Correlation Graph

# cropped to match timespan of Absiko data
treeRawCropped = treeRingMaster[271:384,4]

fit = np.polyfit(treeRawCropped, averageJA, 1)
yAxis = [fit[0] * n + fit[1] for n in treeRawCropped]
rValue = np.corrcoef(treeRawCropped, averageJA)[0,1]
rSquared = rValue * rValue
print(f'R² of gathered data w/o 1969 is {rSquared:.3f}')
# cut at 4 significant figures


fig, ax3 = plt.subplots()
ax3.plot(treeRawCropped, yAxis, color='darkcyan', label=f'y = {fit[0]:.3f}x + {fit[1]:.3f}\nR² = {rSquared:.3f}')
plt.scatter(treeRawCropped, averageJA, color='darkcyan')

ax3.set(xlabel='Tree Ring Index', ylabel='July temperature average (°C)', title='Variable Correlation')

ax3.legend()
ax3.grid()
#plt.show()
plt.close()


## Verifying validity of 1969 period reconstruction
reconstructedTemps1969 = treeRaw * fit1969[0] + fit1969[1]
reconstructedTemps = treeRaw * fit[0] + fit[1]

fig, ax4 = plt.subplots()
ax4.plot(treeYears[271:327], reconstructedTemps[271:327], color = "turquoise", label = "Full range reconstruction")
ax4.plot(treeYears[271:327], reconstructedTemps1969[271:327], color = "mediumpurple", label = "1969 to 2025 reconstruction")
ax4.plot(treeYears[271:327], averageJA[:56], label = "Observed Temperatures", color = "darkolivegreen", linestyle = "dotted")
ax4.set(xlabel = 'Year (CE)', ylabel = 'Temperature (°C)', title = 'Reconstruction Verification')

ax4.legend(loc = "upper center")
ax4.grid()
#plt.show()
plt.close()

## 1913 to 2025 reconstruction vs observed

rValueFull = np.corrcoef(reconstructedTemps1969[271:384], averageJA)[0,1]
rSquaredFull = rValueFull * rValueFull
print(f'Gathered R² 1969 {rSquaredFull}:.3f')

## Reconstructed temperatures and Gaussian Filter
sigma = 3
gaussian = sp.ndimage.gaussian_filter(reconstructedTemps1969, sigma)

fig, ax4 = plt.subplots()
ax4.plot(treeYears, reconstructedTemps1969, color = "turquoise", label = "1969 to 2025 reconstruction", linestyle = "dotted")
ax4.set(xlabel = 'Year (CE)', ylabel = 'Temperature (°C)', title = 'Reconstructed Temperature')
ax4.plot(treeYears, gaussian, color = "mediumpurple", label = f"Gaussian with σ = {sigma}")

ax5 = ax4.twinx()
ax5.set(ylabel='Number of trees sampled')
ax5.plot(treeYears, treeNum, color='darkcyan')

ax4.legend(loc = "upper center")
ax4.grid()
#plt.show()
plt.close()


## Comparison of Reconstruction aginst Observed
fig, ax5 = plt.subplots()
reconstructedTempsCropped = treeRawCropped * fit[0] + fit[1]
ax5.plot(tempYears, reconstructedTempsCropped, label = "reconstructed", color = "turquoise")
ax5.plot(tempYears, averageJA, label = "observed", color = "mediumpurple", linestyle = "dotted")

ax5.set(ylabel = "Temperature (°C)", xlabel = "Year (CE)", yticks = np.arange(7, 15), title = "Verifying Reconstruction")
ax5.legend()

#plt.show()
plt.close()


## Calculating a regression and R-value for long torneträsk chronology
longChron = np.loadtxt("Torne-chron-long.txt", skiprows=1)
longChronYears = longChron[:,0]
longChronIndex = longChron[:,3]

sliceChronIndexShort = longChronIndex[(np.shape(longChronIndex)[0] - 98):]
sliceYears = tempYears[:(np.shape(tempYears)[0] - 15)]
sliceAbiskoTemps = averageJA[:(np.shape(averageJA)[0] - 15)]
sliceFit = np.polyfit(sliceChronIndexShort, sliceAbiskoTemps, 1)
sliceRValue = np.corrcoef(sliceChronIndexShort, sliceAbiskoTemps)[0,1]
print(f"R² of long Torneträsk data is {sliceRValue * sliceRValue:.3f}")


# Comparison of Long Torneträsk Reconstruction aginst Observed
fig, ax5 = plt.subplots()
reconstructedTempsLongChron = sliceChronIndexShort * sliceFit[0] + sliceFit[1]
ax5.plot(sliceYears, reconstructedTempsLongChron, label = "reconstructed", color = "turquoise")
ax5.plot(sliceYears, sliceAbiskoTemps, label = "observed", color = "mediumpurple", linestyle = "dotted")

ax5.set(ylabel = "Temperature (°C)", xlabel = "Year (CE)", yticks = np.arange(7, 15), title = "Verifying Reconstruction of Long Torneträsk")
ax5.legend()

#plt.show()
plt.close()

## Plotting Long Chronology
sigma = 15
longChronReconstruction = longChronIndex * sliceFit[0] + sliceFit[1]
longChronGaussian = sp.ndimage.gaussian_filter(longChronReconstruction, sigma)

fig, ax5 = plt.subplots()
ax5.plot(longChronYears, longChronReconstruction, color = "turquoise", linestyle = "dotted", label = "Reconstructed temperatures")
ax5.plot(longChronYears, longChronGaussian, color = "mediumpurple", label = f"Gaussian with σ = {sigma}")

ax5.set(ylabel = "Reconstructed Temperature (°C)", xlabel = "Year (CE)", title = "Long Chronology Temperature Reconstruction")
ax5.vlines([-3580, -1610, 431, 1257, 1815], 6, 16.4, label = "VEI 7 volcanic eruptions", color = "firebrick")
ax5.annotate("Tambora", (1820, 6.5))
ax5.annotate("Samalas", (1262, 6.5))
ax5.annotate("Ilopango", (436, 6.5))
ax5.annotate("Santorini", (-1605, 6.5))
ax5.annotate("Talisay Caldera", (-3575, 6.5))
ax5.grid()
ax5.legend()
plt.show()
plt.close()

## Comparison of Long Chronology with Gathered Data Reconstructed Temperatures
sliceChronIndexLong = longChronIndex[(np.shape(longChronIndex)[0] - 369):]
sliceLongChronYears = longChronYears[(np.shape(longChronYears)[0] - 369):]
reconstructedTempsLongChron = sliceChronIndexLong * sliceFit[0] + sliceFit[1]
reconstructedGathered = treeRaw * fit1969[0] + fit1969[1]

fig, ax6 = plt.subplots()

line1 = ax6.plot(treeYears, reconstructedGathered, label = "Gathered Data", color = "mediumpurple")
line2 = ax6.plot(sliceLongChronYears, reconstructedTempsLongChron, label = "Long Chronology", color = "turquoise")

ax6.set(ylabel = "Reconstructed Temperature (°C)", xlabel = "Years (CE)", title = "Comparison of Reconstructed Temperatures")
plt.legend()

ax7 = ax6.twinx()
ax7.set(ylabel='Number of trees sampled')
line3 = ax7.plot(treeYears, treeNum, color='darkcyan', label='Tree Numbers - Gathered Data')

lines = line1 + line2 + line3
labels = [l.get_label() for l in lines]
ax6.legend(lines, labels, loc = 'upper center')
ax6.grid()
#plt.show()
plt.close()

min(reconstructedGathered)
# two minima, of 9.20816255 in 1739 and 1741
max(reconstructedGathered)
# max of 17.46745628 in 1655

index = 0
low = reconstructedGathered[0]
high = reconstructedGathered[0]
for x in reconstructedGathered:
    if (x < low):
        low = x
        indexLow = index
    if (x > high):
        high = x
        indexHigh = index
    index += 1
print(f'Low of {low:.3f} at {indexLow + treeYears[0]:.0f} and high of {high:.3f} at {indexHigh + treeYears[0]:.0f}')

