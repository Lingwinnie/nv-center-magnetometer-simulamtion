# Numerical Simulation of an NV Center Audio Transducer

This repository provides a numerical proof-of-concept for a continuous-wave Optically Detected Magnetic Resonance (CW-ODMR) sensor. The code simulates the reverse transduction of acoustic signals into optical variations via the quantum spin dynamics of Nitrogen-Vacancy (NV) centers in diamond.

## Scientific Methodology

The simulation bridges quantum mechanics and signal processing through a rigorous four-step phenomenological approach:

### 1. Quantum Spin Dynamics
The audio-modulated magnetic field $\vec{B}(t)$ fluctuates at acoustic frequencies ($< 20$ kHz), which are orders of magnitude slower than the NV center's electron spin transitions ($\approx 2.87$ GHz). Consequently, the simulation operates strictly under the adiabatic approximation, treating the dynamic system as a continuous succession of instantaneous steady states. 

The quantum state is governed by the Spin-1 ground-state Hamiltonian:

$$
\hat{H}=D\hat{S}_{z}^{2}+\gamma_{NV}\vec{B}(t)\cdot\vec{S}
$$

Where $D \approx 2.87$ GHz is the Zero-Field Splitting parameter, $\gamma_{NV} \approx 28$ GHz/T is the electron gyromagnetic ratio, and $\vec{S}$ is the vector of Spin-1 matrices.

### 2. Matrix Diagonalization and Energy Tracking
For each temporal sample of the audio waveform, the algorithm constructs the $3 \times 3$ Hamiltonian matrix and solves the eigenvalue problem. The numerical difference between the lowest eigenvalues yields the exact instantaneous transition frequency $f_{res}(t)$ between the $m_s=0$ and $m_s=-1$ states, effectively translating the Zeeman effect into a computable frequency shift.

### 3. Phenomenological Optical Transduction (Slope Detection)
To bypass the bandwidth limitations of traditional frequency-sweep ODMR, the code implements a "slope detection" regime. A static microwave driving frequency is anchored exactly at the maximum gradient (inflection point) of the ODMR resonance flank. The mapping of the quantum energy shift to the raw photoluminescence intensity ($I_{PL}$) is modeled phenomenologically using a time-dependent Lorentzian distribution defined by its optical contrast ($C$) and full-width at half-maximum ($\Gamma$).

### 4. Signal Processing and Spectral Validation
The raw optical output undergoes DC background removal and phase inversion to reconstruct the original acoustic waveform into a normalized format. A real-time Fast Fourier Transform (FFT) analysis is then performed. This spectral overlap is critical: it physically validates that, provided the simulated drive current remains within the small-signal regime, the linear transduction holds, completely preventing higher-order harmonic distortions ($n \ge 2$) induced by the Lorentzian curvature.



## Execution

1. Place your target `.wav` file in the repository root and update the `FILENAME` variable within the script if necessary.
2. Execute the code.
3. **Outputs:** The algorithm generates a `_recovered.wav` file and displays a three-panel plot comparing the input current waveform, the raw optical output, and their spectral superposition.


## Author

**[Lingwinnie]** Master's Student in [Nanosciences and Nanotechnologies: Nanoscale and Quantum Engineering] at [Aix-Marseille Université].
