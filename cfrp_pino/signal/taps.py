import numpy as np

def contact_time(window, fs):
    win = window.copy()
    peak = np.argmax(np.abs(window))
    if window[peak] < 0:
        win *= -1

    threshold = win[peak] * 0.1

    L = 0
    for i in range(peak, 0, -1):
        if (win[i] <= threshold):
            L = i
            break

    R = len(win) - 1
    for i in range(peak, len(win)-1):
        if (win[i] <= threshold):
            R = i
            break

    leftInterpolation = L + ((threshold - win[L]) / (win[L+1] - win[L]))
    rightInterpolation = R - 1 + ((threshold - win[R-1]) / (win[R] - win[R-1]))
    
    Width = (rightInterpolation - leftInterpolation) / fs

    return Width / 0.9362
    


    