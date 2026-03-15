import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
import time
import os


# Csts
D_ZFS = 2.87 
GAMMA_NV = 28.0 
MU_0 = 4 * np.pi * 1e-7
DISTANCE_FIL_NV = 1e-3
I_MAX = 0.1
B_BIAS = 0.002
LINEWIDTH = 0.010
CONTRAST = 0.20

#  Spin Matrix
Sx = (1.0/np.sqrt(2)) * np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=complex)
Sy = (1.0j/np.sqrt(2)) * np.array([[0, -1, 0], [1, 0, -1], [0, 1, 0]], dtype=complex)
Sz = np.array([[1, 0, 0], [0, 0, 0], [0, 0, -1]], dtype=complex)

def get_nv_resonances(Bx, By, Bz):
    H = D_ZFS * (Sz @ Sz) + GAMMA_NV * (Bx * Sx + By * Sy + Bz * Sz)
    energies, _ = np.linalg.eigh(H)
    f_lower = np.real(energies[1] - energies[0])
    return f_lower

### Audio

def load_audio_file(filename, max_duration_sec=5.0):
    """Loads a WAV file, converts to mono, normalizes, and truncates to save compute time."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"ERROR: Audio file '{filename}' not found. Please place it in the working directory.")

    fs, data = wavfile.read(filename)

    if len(data.shape) > 1:
        data = data[:, 0]
    
    #  Normalization 
    if data.dtype == np.int16:
        data = data / 32768.0
    elif data.dtype == np.int32:
        data = data / 2147483648.0
    
    # Duration limit
    n_samples_max = int(max_duration_sec * fs)
    if len(data) > n_samples_max:
        print(f"Warning: File truncated to the first {max_duration_sec} seconds for computation.")
        data = data[:n_samples_max]
        
    return fs, data

def audio_to_magnetic_field(audio_signal):
    current_I = audio_signal * I_MAX
    B_wire = (MU_0 * current_I) / (2 * np.pi * DISTANCE_FIL_NV)
    return B_wire + B_BIAS

def simulate_pl_response(B_field_array):
    f_res_static = get_nv_resonances(0, 0, B_BIAS)
    f_mw_fixed = f_res_static - (LINEWIDTH / 2.0)
    print(f" -> Laser fixed at {f_mw_fixed:.4f} GHz")

    pl_signal = []
    total = len(B_field_array)
    start_t = time.time()
    
    print(f"Starting Quantum simulation on {total} points...")
    
    for i, B_val in enumerate(B_field_array):
        current_resonance = get_nv_resonances(0, 0, B_val)
        
        # Lorentzienne
        detuning = f_mw_fixed - current_resonance
        fluorescence = 1.0 - CONTRAST * ( (LINEWIDTH**2) / (LINEWIDTH**2 + 4 * detuning**2) )
        pl_signal.append(fluorescence)
        
        if i % (total // 10) == 0:
            print(f"   Progress: {i/total*100:.0f}%")

    print(f"Simulation done in {time.time() - start_t:.2f} s")
    return np.array(pl_signal)


### Execution

if __name__ == "__main__":
 
    FILENAME = "voix.wav" 
    
    DURATION = 6.0 
    
    
    fs, audio_in = load_audio_file(FILENAME, max_duration_sec=DURATION)
    
    if audio_in is not None:
        # 2. B Field conversion
        B_field = audio_to_magnetic_field(audio_in)
        
        # 3. Physics Simulation 
        pl_output = simulate_pl_response(B_field)
        
        # 4. Audio reconstruction and save 
        audio_recovered = pl_output - np.mean(pl_output)
        audio_recovered = audio_recovered / np.max(np.abs(audio_recovered))
        
        # Phase inversion (here left slope)
        audio_recovered = -audio_recovered
        
        # WAV save
        output_filename = f"{FILENAME}_interception.wav"
        wavfile.write(output_filename, fs, (audio_recovered * 32767).astype(np.int16))
        print(f"audio file generated : {output_filename}")
        
        t = np.arange(len(audio_in)) / fs
        
        plt.figure(figsize=(10, 8))
        
        # Input Signal
        plt.subplot(3, 1, 1)
        plt.plot(t, audio_in, 'b')
        plt.title("1. Input: Original Music (Current)")
        plt.grid(True)
        
        # Output Signal
        plt.subplot(3, 1, 2)
        plt.plot(t, audio_recovered, 'r')
        plt.title("2. Output: NV Center Reconstructed Signal")
        plt.grid(True)
        
        # FFT Comparaison
        plt.subplot(3, 1, 3)
        N = len(audio_in)
        yf_in = fft(audio_in - np.mean(audio_in)); xf = fftfreq(N, 1/fs)[:N//2]
        yf_out = fft(audio_recovered - np.mean(audio_recovered))
        
        plt.plot(xf, np.abs(yf_in[:N//2]), 'b', alpha=0.5, label='Original')
        plt.plot(xf, np.abs(yf_out[:N//2]), 'r--', label='Reconstructed')
        plt.title("3. Spectral Comparison (FFT)")
        plt.xlim(0, 2000) 
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()