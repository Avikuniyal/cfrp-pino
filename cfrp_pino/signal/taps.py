import numpy as np

def contact_time(window, fs, pre=0.5e-3, frac=0.1):
    win = window.astype(float)
    num_quiet_samples = int(pre * fs)
    quiet_samples = win[0:num_quiet_samples]
    med = np.median(quiet_samples)
    win -= med
    peak= np.argmax(np.abs(win))
    if(peak < num_quiet_samples):
       raise ValueError("Peak inside quiet region, window starts too late")
    if win[peak] < 0:
        win *= -1

    threshold = win[peak] * frac

    L = None
    for i in range(peak, -1, -1):
        if (win[i] <= threshold):
            L = i
            break

    R = None
    for i in range(peak, len(win)):
        if (win[i] <= threshold):
            R = i
            break
    if (L is None) or (R is None):
        raise ValueError("pulse runs off the edge of the window")
    
    leftInterpolation = L + ((threshold - win[L]) / (win[L+1] - win[L]))
    rightInterpolation = R - 1 + ((threshold - win[R-1]) / (win[R] - win[R-1]))
    
    Width = (rightInterpolation - leftInterpolation) / fs
    correction = 1 - (2 * np.arcsin(frac) / np.pi)
    return Width / correction
    
def make_pulse(tau, fs, duration, onset, peak=1.0, noise_db=-60):
    num_samples = int(duration * fs)
    t = np.arange(num_samples) / fs
    force = np.zeros(num_samples)
    mask = (t >= onset) & (t <= (onset + tau))
    times_masked = t[mask] - onset
    force[mask] = peak * np.sin(np.pi * (times_masked) / tau)

    noise_std = np.abs(peak) * (10**(noise_db/20))
    noise = np.random.normal(0, noise_std, len(force))
    force += noise

    return t, force



    