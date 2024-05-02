import asyncio
import time
from bleak import BleakScanner
import pyaudio
import wave
import tkinter as tk
import math


def play_sound(wav_file):
    # Open the WAV file
    wf = wave.open(wav_file, 'rb')

    # Create a PyAudio object
    p = pyaudio.PyAudio()

    # Open a stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data from the WAV file
    data = wf.readframes(1024)

    # Play the audio data
    while data != b'':
        stream.write(data)
        data = wf.readframes(1024)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate the PyAudio object
    p.terminate()

async def BLErun():
    print('Scanning for BLE devices with names...')
    target_num_iterations = 15  # Number of iterations
    readings = 0                                # Reading counter
    scan = 0                                    # Scan counter
    rssi_readings = []
    while readings<=(target_num_iterations-1):  
        devices = await BleakScanner.discover(timeout=3.75)
        scan+=1                                 # Scan counter
        for device in devices:
            if device.name == "Ttag123456789":  # Check if the device has a name
                readings+=1                     # if Ttag is picked up, add 1 to readings
                print(f"{readings}, Signal Strength: {device.rssi} dBm")
                rssi_readings.append(device.rssi)

    sum_rssi = sum(rssi_readings)
    average_rssi = sum_rssi/readings
    print(f"Number of scans = {scan},\n \
          Number of readings = {readings},\n \
          Average RSSI value = {average_rssi}, \n \
            RSSI list = {rssi_readings}")

def start_scanning():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(BLErun())
    play_sound(r"C:\Users\olive\OneDrive - University of Bath\Year 4\Semester 2\Python Venvs\Alex_test\alex_implementation\ooooh my short.wav")

def wait_for_next_click():
    print("Waiting for the next click...")

def on_first_click(event):
    start_scanning()
    wait_for_next_click()

def log_average(list):
    # Convert RSSI dBm values to milliwatts
    mw_list = [10**(i/10) for i in list]

    # Calculate the average in milliwatts
    avg_mw = sum(mw_list) / len(mw_list)

    # Convert the average back to dBm
    log_avg = 10 * math.log10(avg_mw)

    return log_avg

# Create a window
window = tk.Tk()
window.title("Click to Start Scanning")
window.attributes('-fullscreen', True)  # Set window to fullscreen

# Create a button to start scanning
start_button = tk.Button(window, text="Click to start scanning", command=start_scanning)
start_button.pack(expand=True, fill='both')  # Expand the button to fill the window

# Start the GUI event loop
window.mainloop()