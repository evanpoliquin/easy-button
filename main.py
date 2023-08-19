import time
import random
import digitalio
import audiopwmio
import audiomp3
import board
import pwmio

# Setup the Button
button = digitalio.DigitalInOut(board.D1)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Setup PWMAudioOut for STEMMA speaker on A0
audio = audiopwmio.PWMAudioOut(board.A0)

# DIP LED PWM setup on D2
led = pwmio.PWMOut(board.D2, frequency=5000, duty_cycle=0)

# List of mp3 tracks available
tracks = ["audio01.mp3", "audio02.mp3", "audio03.mp3", "audio04.mp3"]

last_played_track = None  # To store the last played track

def play_random_track():
    global last_played_track

    # Select a random track that isn't the same as the last played one
    track_name = random.choice(tracks)
    while track_name == last_played_track:
        track_name = random.choice(tracks)

    last_played_track = track_name  # Update the last played track

    brightness_file = track_name.replace(".mp3", ".txt")

    with open(track_name, "rb") as audio_file:
        mp3 = audiomp3.MP3Decoder(audio_file)
        
        with open(brightness_file, "r") as bf:
            audio.play(mp3)
            
            for line in bf:
                if not audio.playing:
                    break

                # Parse and set the brightness value from the file
                brightness = int(line.strip())
                led.duty_cycle = min(max(brightness, 0), 65535)
                time.sleep(0.011)  # Adjust this sleep time to match the rate of the brightness data
                
            # Ensure the audio finishes playing even if brightness values run out
            while audio.playing:
                time.sleep(0.05)
                
            audio.stop()
            led.duty_cycle = 0

while True:
    if not button.value:
        play_random_track()
        while not button.value:
            pass
        time.sleep(0.2)
