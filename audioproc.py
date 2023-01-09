import numpy as np
import pyaudio
import serial

# Set the parameters for the audio input
chunkSize = 1024
format = pyaudio.paInt16
channels = 1
rate = 44100

# Set the number of frequency bands
nBands = 10

# Set the parameters for the serial connection to the Arduino
arduinoPort = '/dev/ttyACM0'  # Replace this with the correct port for your Arduino
arduinoBaudRate = 9600

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a stream for the audio input
stream = p.open(
    format=format,
    channels=channels,
    rate=rate,
    input=True,
    frames_per_buffer=chunkSize
)

# Open a serial connection to the Arduino
ser = serial.Serial(arduinoPort, arduinoBaudRate)

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
    
    # Send "start" to the Arduino
    ser.write("start\n".encode())
    
    # Send the magnitudes to the Arduino, one per line
    for m in magnitudes:
        ser.write("{}\n".format(m).encode())
  except KeyboardInterrupt:
    print('Keyboard Interrupt received. Shutting down processes.')
    break
    

# Close the serial connection to the Arduino
ser.close()

# Close the audio stream
stream.stop_stream()
stream.close()

# Terminate PyAudio
p.terminate()
