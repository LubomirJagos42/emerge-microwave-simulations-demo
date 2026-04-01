## EMerge simulation - S11
#
#
import emerge as em
import numpy as np
from emerge.plot import smith, plot_sp

simulationObj = em.Simulation("Discone Antenna.FCStd", load_file=True)
simulationResult = simulationObj.data.mw

#######################################################################################################################################
# EXCITATION basic
#######################################################################################################################################
fmin = 0.5*1000000000.0
fmax = 5.0*1000000000.0
resolution = 0.2
npoints = 7
simulationObj.mw.set_frequency_range(fmin, fmax, npoints)
simulationObj.mw.set_resolution(resolution)

freqs = simulationResult.scalar.grid.freq
freq_dense = np.linspace(fmin, fmax, 1001)
S11 = simulationResult.scalar.grid.model_S(1, 1, freq_dense)  # reflection coefficient
plot_sp(freq_dense, S11)  # plot return loss in dB
smith(S11, f=freq_dense, labels='S11')  # Smith chart of S11

