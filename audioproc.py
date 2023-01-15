import numpy as np
import pyaudio
import serial
from time import *

# Set the parameters for the audio input
chunkSize = 1024
audioFormat = pyaudio.paInt16
channels = 1
rate = 44100

# Set the number of frequency bands
nBands = 10

# Initialize PyAudio
p = pyaudio.PyAudio()

arduino = serial.Serial("COM3", 9600)

# Open a stream for the audio input
stream = p.open(
    format=audioFormat,
    channels=channels,
    rate=rate,
    input=True,
    frames_per_buffer=chunkSize
)

# Continuously read and process audio data
while True:
  try:
    # Read a chunk of audio data from the input stream
    data = stream.read(chunkSize)
    
    # Convert the audio data to a NumPy array
    audioData = np.frombuffer(data, dtype=np.int16)
    
    # Split the audio data into frequency bands
    bands = np.array_split(audioData, nBands)
    
    # Calculate the magnitude of each frequency band
    magnitudes = [np.abs(band).mean() for band in bands]
    
    # Determine the strength of each frequency band
    # strengths = [int(m / (1800 / 6)) for m in magnitudes]
    strengths = []
    for m in magnitudes:
      if int(m / (1800 / 15 )) > 8:
        strengths.append(8)
      else:
        strengths.append(int(m / (1800 / 15 )))
     
    # Print the strengths in a neat list
    strengthString = ""
    for s in strengths:
      strengthString += str(s) + ""
    
    print(bytes(strengthString, encoding='utf8'))
    # arduino.write(strengthString[:-1])
    # print(strengths)
    arduino.write(bytes(strengthString, encoding='utf8'))
    sleep(0.02)
  except KeyboardInterrupt:
    break

# Close the audio stream
stream.stop_stream()
stream.close()

arduino.close()

# Terminate PyAudio
p.terminate()
