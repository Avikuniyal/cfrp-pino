import numpy as np
from cfrp_pino.signal.taps import contact_time, make_pulse

np.random.seed(0)    
fs = 192000
tau = [0.15e-3, 1.08e-3]



# Test 1: Accuracy across different tau values with random onset times
print("Testing contact_time function with various tau values and random onset times:")
for tau_val in tau:
    errors = []
    for i in range(20):
        onset = 0.001 + np.random.uniform(0, 1 / fs)
        t, force = make_pulse(tau_val, fs, 0.004, onset, peak = -1 if(i%2!=0) else 1.0)
        forceCopy = force.copy()
        errors.append((contact_time(force, fs)-tau_val)/tau_val)
        assert np.array_equal(force, forceCopy), "Force Array Changed"
    print("\ttau = ", tau_val, "\n\tbiggest error = ", np.max(np.abs(errors)) * 100, "%", "\n\tmean error = ", np.mean(errors) * 100, "%" )
    assert np.max(np.abs(errors)) * 100 < 0.5, "Some errors larger than 0.5%"
    print("\n")


# Known Pulse for Remaining Tests
onset = 0.001 + np.random.uniform(0, 1/fs)
t, force = make_pulse(0.3e-3, fs, 0.004, onset)
onset_index = int(onset * fs)


# Test 2: Check that contact time still works with a constant offset added to the signal
print("Testing that contact time still works with a constant offset added to the signal:")

err = np.abs(contact_time(force + 0.3, fs) - 0.3e-3) / 0.3e-3
print("\tError = ", err * 100, "%\n")
assert err * 100 < 0.5, "Offset broke the contact time calculation"


# Test 3: Check that valueAlert for peak landing in quiet region works
print("Testing if valueAlert for peak landing in quiet region works:")

start = onset_index + 20
raised = False
try:
    contact_time(force[start:], fs)
except ValueError as e:
    raised = "too late" in str(e)

print("\tValueError raised: ", raised,)
assert raised, "Contact time did not raise ValueError when peak landed in quiet region"


# Test 4: Check that valueAlert for signal running off the edge of the window works
print("Testing if valueAlert for signal going out of the window works:")

end = onset_index + 40
raised = False
try:
    contact_time(force[:end], fs)
except ValueError as e:
    raised = "off the edge" in str(e)

print("\tValueError raised: ", raised,)
assert raised, "Contact time did not raise ValueError when signal ran off the edge of the window"


        
    
