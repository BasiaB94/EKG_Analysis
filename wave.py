import pywt
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

def plot(y, title, xLab, folder = ""):
    plt.plot(y)
    plt.ylabel("mV")
    plt.xlabel(xLab)
    plt.title(title)
    if folder != "":
        plt.savefig(folder + title + ".png")
    plt.show()

# Wavelet transforms

def omit(coeffs, levels):
    
    for i in levels[0]:
        coeffs[-i] = {k: np.zeros_like(v) for k, v in coeffs[-i].items()}
    
    if levels[1]: # If we want to exclude cA
        coeffs[0] = np.zeros_like(coeffs[0])
    
    return coeffs

def decomp(cA, wavelet, levels, mode='constant', omissions=([], False)):
    
    if omissions[0] and max(omissions[0]) > levels:
        raise ValueError("Omission level %d is too high.  Maximum allowed is %d." % (max(omissions[0]), levels))
        
    coeffs = pywt.wavedecn(cA, wavelet, level=levels, mode=mode)
    coeffs = omit(coeffs, omissions)
    
    return pywt.waverecn(coeffs, wavelet, mode=mode)

##helper functions
def load(filename, path = '../Physionet_Challenge/training2017/'):
    #
    ### A helper function to load data
    # input:
    #   filename = the name of the .mat file
    #   path = the path to the file
    # output:
    #   data = data output
    
    mat = sio.loadmat(path + filename + '.mat')
    data = np.divide(mat['val'][0],1000)
    return data

def multiplot(data, graph_names):
    #plot multiple lines in one graph
    # input:
    #   data = list of data to plot
    #   graph_names = list of record names to show in the legend
    for l in data:
        plt.plot(l)
    plt.legend(graph_names)
    plt.show()
    
def calculate_residuals(original, wavelets, levels, mode='symmetric', omissions=([],True)):
    # calculate residuals for a single EKG
    rebuilt = decomp(original, wavelets, levels, mode, omissions)
    residual = sum(abs(original-rebuilt[:len(original)]))/len(original)
    return residual

def all_residuals(records, wavelets='sym4', levels=3, mode='symmetric', omissions=([1],False), path = '../Physionet_Challenge/training2017/'):
    #calculate residuals for all the EKGs
    residual_list = []
    file = open(path+records, 'r')
    while (True):
        newline = file.readline().rstrip('\n')
        if newline == '':
            break
        data = load(newline)
        residuals = calculate_residuals(data, wavelets, levels, mode, omissions)
        residual_list.append(residuals)
    file.close()
    return residual_list


    