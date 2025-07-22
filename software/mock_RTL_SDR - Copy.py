from rtlsdr import RtlSdr
import numpy as np
import threading
import time
from datetime import datetime

sdr = RtlSdr()
sdr.sample_rate = 2.4e6     #Säger hur mycket hårdvaran kan läsa in per sekund
sdr.center_freq = 119e6  # Val av frekvens, t.ex. 433.92 MHz
sdr.gain = 20.7          # Auto gain man kan ävem sätta gain manuellt, max 50


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



#Main loop för att läsa samples och beräkna signalstyrka
try:
    while True:
        samples = sdr.read_samples(256 * 10240)
        signal_power_dbfs = calculate_dbfs(samples)
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Frequncy: {sdr.center_freq / 1e6:.2f} MHz | {signal_power_dbfs:.2f} dBFS | Gain: {sdr.gain}")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    sdr.close()
