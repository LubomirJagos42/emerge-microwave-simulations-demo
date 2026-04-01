## EMerge simulation - S11
#
#
import emerge as em
import numpy as np
from emerge.plot import smith, plot_sp

simulationObj = em.Simulation("Helical_Antenna", load_file=True)
simulationResult = simulationObj.data.mw

###############################################################################
# PORT NAME AND THEIR NUMBERS LIST
###############################################################################
portNamesAndNumbersList = {}
portNamesAndNumbersList["input - feed_port"] = 1

###############################################################################
# PLOT S DATA
###############################################################################
sourcePortName = 'input - feed_port'
sourcePortNumber = portNamesAndNumbersList[sourcePortName]

freqs = simulationResult.scalar.grid.freq
fmin = freqs.min()
fmax = freqs.max()
freq_dense = np.linspace(fmin, fmax, 1001)
S_data = simulationResult.scalar.grid.model_S(sourcePortNumber, sourcePortNumber, freq_dense)  #reflection coefficient
plotLabel = f'S{sourcePortNumber}{sourcePortNumber} ({sourcePortName})'
plot_sp(freq_dense, S_data, dblim=[-20, 0])  #plot return loss in dB
smith(S_data, f=freq_dense, labels=plotLabel)  #smith chart

# import pandas as pd
#
# outputFile = "helical_antenna_s11.csv"
# df = pd.DataFrame({
#     'f (GHz)':  freq_dense,
#     'S11 (dB)':   20*np.log10(np.abs(S_data)),
#     'S11 (deg.)':   np.angle(S_data, deg=True),
# })
#
# df.to_csv(outputFile, index=False)
# print(f"✓ Saved {len(df)} rows to {outputFile}")
#
# import matplotlib.pyplot as plt
# df = pd.read_csv("helical_antenna_s11.csv")
# plt.plot(df['f (GHz)'], df['S11 (dB)'])
# plt.ylim(-20, 0)
# plt.show()

