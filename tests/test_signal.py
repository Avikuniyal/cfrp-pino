import numpy as np
from cfrp_pino.signal.taps import contact_time, make_pulse

np.random.seed(0)    
fs = 192000
tau = [0.15e-3, 1.08e-3]

for tau_val in tau:
    errors = []
    for i in range(20):
        onset = 0.001 + np.random.uniform(0, 1 / fs)
        t, force = make_pulse(tau_val, fs, 0.004, onset, peak = -1 if(i%2!=0) else 1.0)
        forceCopy = force.copy()
        errors.append((contact_time(force, fs)-tau_val)/tau_val)
        assert np.array_equal(force, forceCopy), "Force Array Not Changed"
    print("tau = ", tau_val, "\nbiggest error = ", np.max(np.abs(errors)) * 100, "%", "\nmean error = ", np.mean(errors) * 100, "%" )
    assert np.max(np.abs(errors)) * 100 < 3, "All errors are within 3% tolerance."
    print("\n")

        
        
    
