# Kill Test: Can a Cheap Tap Test Detect Hidden Damage in Carbon Fiber?

**Status:** In progress (September to October 2026)

This document describes the first experiment in the project: a detection feasibility test that determines whether the core idea works before any modeling or machine learning is built on top of it. 


## Why this test comes first

The project aims to detect **delamination** in carbon fiber reinforced polymer (CFRP) panels. CFRP is made of thin bonded layers, and delamination is when those layers separate. It is one of the most serious forms of damage in composite parts because it is usually invisible from the surface and significantly reduces strength.

The proposed method is meant to be low cost. It is to tap the panel at a grid of points, record the vibration with a cheap piezoelectric sensor, and use a physics model of plate bending to reconstruct a map of where the panel is stiffer or softer than expected.

That approach only works if the damage actually leaves a measurable trace in the sensor data. If a cheap sensor and a simple tap cannot distinguish a damaged region from a healthy one, no model can recover information that was never recorded. This test makes sure the sensor can acually pick up that data.



## Research questions

1. **Sensitivity:** Does subsurface damage in a thin CFRP panel change a low-cost tap measurement by clearly more than the measurement's own natural variation?
2. **Signal source:** Which part of the measurement carries the damage signal: the tap's contact time, the local vibration of the damaged region, or shifts in the whole panel's natural frequencies? The answer is important for how the rest of the model is designed.



## Test specimen

Real delamination is difficult to create in a controlled way, so this test uses the standard reference defect in nondestructive testing: the **flat-bottom hole**. Shallow circular pockets are machined into the back of a 1.6 mm (1/16 in) woven CFRP panel using a CNC router, leaving a thin skin on the front. The front surface appears undamaged, and all measurements are taken from that side, as they would be on a real part.

The panel contains eight holes covering four diameters and two remaining skin thicknesses:

| Diameter | 0.5 mm skin remaining | 1.0 mm skin remaining |
|---|---|---|
| 40 mm | H1 | H8 |
| 30 mm | H3 | H6 |
| 19 mm | H5 | H4 |
| 12.7 mm | H7 | H2 |

Larger holes and thinner skins produce softer regions and should be easier to detect. Sizes and depths are distributed across the panel so that defect size is not confounded with position.

Flat-bottom holes are a simplified case. Real delamination is a thinner internal gap that can partially close or rattle. Passing this test serves as a condition for the model, not proof that it will detect delamination. Delamination detection will be evaluated later with real impact damage.


## Measurement setup

- **Support:** The panel rests on soft foam pads so it vibrates freely.
- **Response sensor:** A 20 mm piezoelectric disc coupled to the panel with beeswax, placed away from corners and symmetry lines so it responds to all major vibration patterns.
- **Instrumented impactor:** A second piezo disc built into the tip of the tapper, with a small steel ball as the striking surface. It records the force and duration of each impact. Both a pendulum based hammer and an Arduino-controlled solenoid tapper are evaluated for repeatability.
- **Acquisition:** A two-channel USB audio interface with high-impedance instrument inputs, recording at 192 kHz.




## What is measured

**Contact time (primary metric).** The duration the impactor stays in contact with the surface during a tap. A thinner, softer region allows the tapper to sink in more rather than resisting: the tip sinks further and stays in contact longer. This is the physical basis of the traditional "coin tap" inspection, where damaged areas sound dull. A simple spring model predicts contact time over the largest, thinnest hole should increase by a factor of roughly 3.5 to 7 relative to healthy material, while the smallest, shallowest hole may produce only a 10 to 30 percent increase.

**Local resonance.** The thin skin over each hole behaves like a small drumhead with its own natural frequency. This signal is expected to be weak under tap excitation.

**Global mode shifts.** The panel as a whole has natural vibration frequencies. Each hole shifts them slightly (well under 1 percent). Temperature also shifts them, but uniformly across all modes, while a localized defect shifts different modes by different amounts. That distinction is used to separate damage from environmental drift.

The response signal is also normalized by the measured tap force, so variation in tapping strength does not affect the result.



## Experimental design

Different locations on a panel respond differently even without damage (for example, near edges versus the center). To remove that effect, every location is compared **to itself**:

1. Thirteen locations (the eight future hole sites, four healthy control sites, and one reference site) are measured **before** machining, in two separate sessions on different days with the sensor removed and reattached between them.
2. The holes are machined.
3. The same thirteen locations are measured **after** machining with an identical setup.
4. Two additional sessions on following days check that the result is stable over time.

Each location receives 10 taps per session, measured in randomized order. The two pre-machining sessions establish how much measurements vary with no change to the panel at all, which serves as the baseline for judging whether a post-machining change is real.

Before any CFRP is measured, the full signal chain is validated on an aluminum plate whose vibration behavior is well understood, and a single test pocket is measured on a small CFRP coupon before the main panel is machined.



## Success criteria (pre-registered)

The pass rule is fixed and recorded before any CFRP data is collected, and is not altered after results are seen.

A hole is counted as **detected** if its before-to-after increase in contact time exceeds **three times** the combined measurement noise (tap-to-tap scatter plus day-to-day drift measured at undamaged sites). A threshold of three rather than two standard deviations is used because many comparisons are made, and a looser threshold would produce false detections from noise alone.

| Outcome | Criteria | Interpretation |
|---|---|---|
| **Strong pass** | All four 0.5 mm holes detected, at least two of the four 1.0 mm holes detected, and defects rank in the predicted order of difficulty | Method is viable; project proceeds as designed |
| **Weak pass** | At least the two largest thin-skin holes (H1, H3) detected | Method is viable with a stated minimum detectable defect size |
| **Fail** | The easiest defect (H1) not detected by any metric | Method as designed is not viable; fallback options are pursued |

Two additional analyses are reported without pass/fail thresholds: whether the measured changes agree with the physics model's predictions (ranking and approximate magnitude), and which of the measured signals carries the defect information.

All results are also checked visually with before/after signal overlays for every hole.



## Controls for confounding factors

| Potential confound | Control |
|---|---|
| Location-dependent response | Same-location before/after comparison |
| Sensor reattachment | Primary metrics (contact time, frequencies) are insensitive to coupling; remount variation quantified separately |
| Temperature and humidity | Logged each session; uniform-shift drift check; repeated baseline sessions |
| Tap strength variation | Force normalization; rejection of weak taps |
| Double impacts | Automatic detection and rejection |
| Machining damage beyond design | Controlled cutting parameters; inspection and photographs of every hole |
| Incorrect hole depth | Remaining thickness measured directly after machining; mass checked before and after |
| Experimenter bias | Pre-registered criteria; randomized measurement order; by-ear assessments recorded before viewing data |



## Relation to existing methods

Commercial tap-testing systems (for example, the Computer-Aided Tap Tester developed at Iowa State) already use contact time to identify damaged regions. They model each tap point independently as a simple spring. This project's broader goal is to replace that point-by-point model with a full plate model in which neighboring points are physically linked, which could allow detection of deeper defects or reconstruction from fewer measurements. The kill test establishes which signals are available for that reconstruction, and its contact-time measurements are used directly to implement the commercial-style method as a comparison baseline.



## If the test fails

A fixed sequence of fallback options is evaluated, each with a time limit:

1. Full audit of the measurement setup
2. Relocating the sensor next to or on top of the defect
3. Swept-frequency excitation to directly excite the thin skin's resonance
4. Replacing the piezo disc with a MEMS accelerometer
5. Reframing the project as a study of the detection limits of low-cost acoustic inspection

A final go / modify / pivot decision is made by **October 15, 2026**.



## Outputs

- Before/after measurements for all defect and control sites
- Predicted versus measured contact-time comparison
- Measured panel properties (density, thickness variation, natural frequencies) used to calibrate the physics model
- A determination of which signal carries defect information, which sets the design of the downstream model
- A contact-time baseline implementation for comparison against the final method

# Formatted by AI (Claude)

