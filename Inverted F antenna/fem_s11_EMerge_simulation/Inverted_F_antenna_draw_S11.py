## EMerge simulation - S11
#
#
import emerge as em
import numpy as np
from emerge.plot import smith, plot_sp

simulationObj = em.Simulation("Inverted_F_antenna.FCStd", load_file=True)
simulationResult = simulationObj.data.mw

###############################################################################
# PORT NAME AND THEIR NUMBERS LIST
###############################################################################
portNamesAndNumbersList = {}
portNamesAndNumbersList["in - port_in"] = 1

###############################################################################
# PLOT S DATA
###############################################################################
sourcePortName = 'in - port_in'
sourcePortNumber = portNamesAndNumbersList[sourcePortName]

freqs = simulationResult.scalar.grid.freq
fmin = freqs.min()
fmax = freqs.max()
freq_dense = np.linspace(fmin, fmax, 1001)
S_data = simulationResult.scalar.grid.model_S(sourcePortNumber, sourcePortNumber, freq_dense)  #reflection coefficient
plotLabel = f'S{sourcePortNumber}{sourcePortNumber} ({sourcePortName})'
plot_sp(freq_dense, S_data)  #plot return loss in dB
smith(S_data, f=freq_dense, labels=plotLabel)  #smith chart

