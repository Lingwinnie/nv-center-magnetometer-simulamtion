# NV Center ODMR Audio Simulator

Numerical simulation of an acoustic sensor based on Nitrogen-Vacancy (NV) centers in diamond. This project provides a computational proof-of-concept for Continuous-Wave Optically Detected Magnetic Resonance (CW-ODMR) magnetometry applied to audio signal interception.

## Physical Model

The simulation solves the steady-state Spin-1 Hamiltonian of the NV center's ground state under the adiabatic approximation. The external magnetic field $\vec{B}(t)$ is induced by an audio-modulated current.

The Hamiltonian is defined as:
$$\hat{H} = D\hat{S}_z^2 + \gamma_{NV}\vec{B}(t)\cdot\vec{S}$$

Where:
* $D \approx 2.87$ GHz is the Zero-Field Splitting parameter.
* $\gamma_{NV} \approx 28$ GHz/T is the gyromagnetic ratio.
* $\vec{S}$ represents the Spin-1 matrices.

### Transduction Mechanism (Slope Detection)
The algorithm models a slope detection protocol to bypass the slow acquisition limits of standard frequency sweeps. The microwave drive frequency is locked onto the maximum gradient of the ODMR resonance. Instantaneous quantum energy shifts are dynamically mapped to optical photoluminescence (PL) variations using a time-dependent Lorentzian lineshape.

## Requirements

Install the required Python libraries:
`pip install numpy scipy matplotlib`

## Usage

1. Place a valid audio file in the repository root and name it `input_audio.wav` (or edit the `FILENAME` variable in the script).
2. Execute the solver:
   `python nv_audio_simulator.py`
3. **Outputs:** The script generates a `_recovered.wav` file and plots a real-time temporal and spectral analysis (FFT) to validate the linear transduction and the absence of higher-order harmonic distortions.
