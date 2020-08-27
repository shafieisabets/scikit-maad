#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
Endemble of functions to compute acoustic descriptors from 1D signals

"""

from scipy.signal import periodogram, welch
import pandas as pd
import numpy as np

def psd(s, fs, nperseg=256, method='welch', window='hanning', nfft=None, tlims=None):
    """ 
    Estimates power spectral density of 1D signal using Welch's or periodogram methods. 
    .. note:: This is a wrapper that uses functions from scipy.signal module
    
    Parameters
    ----------
    s: 1D array 
        Input signal to process 
    fs: float, optional
        Sampling frequency of audio signal
    nperseg: int, optional
        Lenght of segment for 'welch' method, default is 256
    nfft: int, optional
        Length of FFT for periodogram method. If None, length of signal will be used.
        Length of FFT for welch method if zero padding is desired. If None, length of nperseg will be used.
    method: {'welch', 'periodogram'}
        Method used to estimate the power spectral density of the signal
    tlims: tuple of ints or floats
        Temporal limits to compute the power spectral density in seconds (s)
        If None, estimates for the complete signal will be computed.
        Default is 'None'
    
    Returns
    -------
    psd: pandas Series
        Estimate of power spectral density
    f_idx: pandas Series
        Index of sample frequencies
    
    Examples
    --------
    >>> s, fs = sound.load('spinetail.wav')
    >>> psd, f_idx = features.psd(s, fs, nperseg=512)
    """
    
    if tlims is not None:
    # trim audio signal
        try:
            s = s[int(tlims[0]*fs): int(tlims[1]*fs)]
        except:
            raise Exception('length of tlims tuple should be 2')
    
    
    if method=='welch':
        f_idx, psd_s = welch(s, fs, window, nperseg, nfft)
    
    elif method=='periodogram':
        f_idx, psd_s = periodogram(s, fs, window, nfft, scaling='spectrum')
        
    else:
        raise Exception("Invalid method. Method should be 'welch' or 'periodogram' ")
        

    index_names = ['psd_' + str(idx).zfill(3) for idx in range(1,len(psd_s)+1)]
    psd_s = pd.Series(psd_s, index=index_names)
    f_idx = pd.Series(f_idx, index=index_names)
    return psd_s, f_idx

def rms(s):
    """
    Computes the root-mean-square (RMS) level of an input signal

    Parameters
    ----------
    s : 1D array
        Input signal to process

    Returns
    -------
    rms: float
        Root mean square of input signal
    
    Examples
    --------
    >>> s, fs = sound.load('spinetail.wav')
    >>> rms = features.rms(s)
    
    """
    return np.sqrt(np.mean(s**2))
