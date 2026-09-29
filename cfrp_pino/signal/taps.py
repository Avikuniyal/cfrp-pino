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
    
def make_pulse(tau, fs, duration, onset, peak=1.0, noise_db=-60):
    num_samples = int(duration * fs)
    t = np.arange(num_samples) / fs
    force = np.zeros(num_samples)
    mask = (t >= onset) & (t <= (onset + tau))
    times_masked = t[mask] - onset
    force[mask] = peak * np.sin(np.pi * (times_masked) / tau)

    noise_std = peak * (10**(noise_db/20))
    noise = np.random.normal(0, noise_std, len(force))
    force += noise

    return t, force



    