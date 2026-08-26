"""Generate a short audible example of acoustic beats."""

from pathlib import Path
import wave

import numpy as np


sample_rate = 44_100
duration = 10.0
t = np.arange(int(sample_rate * duration)) / sample_rate

# Two constant, nearby frequencies: their interference changes the amplitude,
# although neither oscillator changes frequency.
signal = 0.38 * (np.sin(2 * np.pi * 440 * t) + np.sin(2 * np.pi * 443 * t))
fade_samples = int(0.08 * sample_rate)
fade = np.linspace(0, 1, fade_samples)
signal[:fade_samples] *= fade
signal[-fade_samples:] *= fade[::-1]
pcm = np.int16(np.clip(signal, -1, 1) * 32767)

output = Path(__file__).resolve().parents[1] / "notebooks/week06/audio/uncoupled_beats_440_443.wav"
output.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(output), "wb") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)
    wav.writeframes(pcm.tobytes())

print(output)
