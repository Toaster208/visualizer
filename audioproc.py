import numpy as np
import pyaudio

# Set the parameters for the audio input
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Set the number of frequency bands
N_BANDS = 10

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a stream for the audio input
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK_SIZE
)

# Continuously read and process audio data
while True:
    # Read a chunk of audio data from the input stream
    data = stream.read(CHUNK_SIZE)
    
    # Convert the audio data to a NumPy array
    audio_data = np.frombuffer(data, dtype=np.int16)
    
    # Split the audio data into frequency bands
    bands = np.array_split(audio_data, N_BANDS)
    
    # Calculate the magnitude of each frequency band
    magnitudes = [np.abs(band).mean() for band in bands]
    
    # Print the magnitudes in a neat fashion
    print("Magnitudes:", ["{:.2f}".format(m) for m in magnitudes])

# Close the audio stream
stream.stop_stream()
stream.close()

# Terminate PyAudio
p.terminate()
