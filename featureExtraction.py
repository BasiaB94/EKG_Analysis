import pandas as pd
import numpy as np
import scipy
import wave # this is the wave.py file in the local folder
# np.set_printoptions(threshold=np.nan)


# Reading in matlab data

mat = scipy.io.loadmat('../Physionet_Challenge/training2017/A00001.mat')
data = np.divide(mat['val'][0],1000)
data = data[:1000]

reference = pd.read_csv('../Physionet_Challenge/training2017/REFERENCE.csv', names = ["file", "answer"]) # N O A ~
    

# Run Wavelet transforms

wave.plot(data[:200], "Original Signal", "Index n * 0.003")

rebuilt = wave.decomp(data, 'sym4', 5, omissions=([1,2,4,5], True))
wave.plot(rebuilt[:200], "rebuilt", "Index n * 0.003")


# Imperatively grabbing features

# Detecting R Peaks
xMax = np.argmax(rebuilt) # location of max peak
threshold = data[xMax] * 0.35
peaks = np.zeros_like(data)
# TODO: Find all the peak intervals using the threshold ad set them into peaks
# Check out https://www.mathworks.com/examples/wavelet/mw/wavelet-ex77408607-r-wave-detection-in-the-ecg


# Detecting noise

residual_feature = wave.all_residuals('RECORDS')


# TODO: Use fourier transforms to detect noisy datasets