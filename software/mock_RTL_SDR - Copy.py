from rtlsdr import RtlSdr
import numpy as np
import threading
import time
from datetime import datetime

# Class MockRtlSdr simulerar sälva beteendet som RtlSdr har, ta bort den när du har tillgång till RTL-SDR hårdvaran.
class MockRtlSdr:
    def __init__(self):
        self.sample_rate = 2.4e6
        self.center_freq = 433.92e6
        self.gain = 'auto'
    
    def read_samples(self, num_samples):
        # Generate synthetic IQ samples (complex values)
        # Simulating a sine wave signal + noise
        t = np.arange(num_samples) / self.sample_rate
        freq = 10e3  # Simulate a 10 kHz tone
        signal = 0.7 * np.exp(2j * np.pi * freq * t)
        noise = 0.3 * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        samples = signal + noise
        return samples

    def close(self):
        pass

#Funktion för att övervaka konfigurationsfilen och uppdatera gain och frekvens
def config_file_watcher():
    global sdr
    config_file = "sdr_config.txt" #Gör en fil som heter sdr_config.txt med gain=25 & freq=420.92 som exempel
    last_gain = None
    last_freq = None

    while True:
        try:
            with open(config_file, 'r') as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith("gain="):
                    value = line.split("=")[1].strip()
                    if value.lower() == "auto":
                        if sdr.gain != 'auto':
                            sdr.gain = 'auto'
                            print("Gain set to AUTO.")
                    else:
                        try:
                            gain_value = float(value)
                            if 0 <= gain_value <= 50 and sdr.gain != gain_value:
                                sdr.gain = gain_value
                                print(f"Gain set to {gain_value} dB.")
                        except:
                            pass

                elif line.startswith("freq="):
                    try:
                        freq_mhz = float(line.split("=")[1].strip())
                        new_freq = freq_mhz * 1e6
                        if new_freq != sdr.center_freq:
                            sdr.center_freq = new_freq
                            print(f"Center frequency set to {freq_mhz:.2f} MHz.")
                    except:
                        pass
        except FileNotFoundError:
            pass  # Ignore if file doesn't exist
        time.sleep(1)

# Start gain input in a separate thread
threading.Thread(target=config_file_watcher, daemon=True).start()

# Funktion för att räkna styrkan i dBFS¨
""" Vi får en array från samples, i komplex form. Vi använder np.abs och kvadrerar den för att få signalens magnitud.
    Sedan konverterar vi den till dBFS för att få signalens styrka.
"""
def calculate_dbfs(samples):
    power = np.mean(np.abs(samples)**2)
    dbfs = 10 * np.log10(power) 
    return dbfs

# Simulering av SDR, lägg till sen riktiga RtlSdr kod när du har tillgång till hårdvaran

#RTL-SDR klarar av en sample rate på 2.4 MS/s, vilket innebär att den kan läsa 2.4 miljoner I/Q värden per sekund.
#Vi har en sample rate på 256*1024, detta motsvara 262144 av I/Q värden i en array, som vi vill processera.
#För att ta in mer data höj sdr.sample_rate men det påverkar RAM ju högre sample rate du har.
sdr = MockRtlSdr()
"""   
sdr = RtlSdr()
sdr.sample_rate = 2.4e6     #Säger hur mycket hårdvaran kan läsa in per sekund
sdr.center_freq = 433.92e6  # Val av frekvens, t.ex. 433.92 MHz
sdr.gain = 'auto'           # Auto gain man kan ävem sätta gain manuellt, max 50
"""

#Main loop för att läsa samples och beräkna signalstyrka
try:
    while True:
        samples = sdr.read_samples(256 * 1024)
        signal_power_dbfs = calculate_dbfs(samples)
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Frequncy: {sdr.center_freq / 1e6:.2f} MHz | {signal_power_dbfs:.2f} dBFS | Gain: {sdr.gain}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    sdr.close()
