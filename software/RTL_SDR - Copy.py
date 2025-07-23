
from rtlsdr import RtlSdr
import numpy as np
from scipy.signal import welch
from datetime import datetime



sdr = RtlSdr()
sdr.sample_rate = 2.4e6                     #Säger hur mycket hårdvaran kan läsa in per sekund
sdr.center_freq = 520.121e6 - 1.2e6         #Val av frekvens, 100.8 MHz har radio, 110.0 MHz har ingen radio, 520.121 MHz har konstant ping
sdr.gain = 40                               # Auto gain man kan ävem sätta gain manuellt, max 50


NFFT = 1024*4 #4096 bins through the frequency range
NUM_SAMPLES_PER_SCAN = 0.8e6 # 6144 samples if  NFFT*16

while True:
    samples = sdr.read_samples(NUM_SAMPLES_PER_SCAN)
    frequencies, psd_vals = welch(samples, fs=sdr.sample_rate, nperseg=NFFT, return_onesided=False)

    psd_dbfs = 10 * np.log10(psd_vals + 1e-12)


    target_freq = 520.121e6
    bin_index = np.argmin(np.abs(frequencies + sdr.center_freq - target_freq))  
    signal_power = psd_dbfs[bin_index]

    timestamp = datetime.now().strftime("%H:%M:%S")

    print(f"[{timestamp}] {signal_power:.2f} dBFS")
    


""" 
print(frequencies)

print(psd_dbfs)  
print(signal_power)

print(bin_index)
"""
