import numpy as np
# from cfrp_pino.signal.taps import contact_time

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

