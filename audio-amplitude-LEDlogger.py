##This script will take a mp3's amplitude and will log it to a txt document with its outputs adjusted between 0 and 65535 so it can be used to control the brightness of the button's LEDs

from pydub import AudioSegment
import numpy as np

def rms_to_value(rms, max_rms):
    """
    Converts RMS to a value between 0 and 65535.
    """
    return int((rms / max_rms) * 65535)

def main():
    # Load the mp3 file
    song = AudioSegment.from_mp3("audio-name-here.mp3")  #put the audio files in the same directory as this script

    # Convert audio segment to raw audio data
    samples = np.array(song.get_array_of_samples(), dtype=np.float64)

    # Calculate RMS (Root Mean Square) for each frame
    rms_values = []
    for i in range(0, len(samples), 1024):
        frame_samples = samples[i:i+1024]
        if len(frame_samples) > 0:  # Check to ensure frame has samples
            mean_square = np.mean(frame_samples**2)
            
            if mean_square < 0:
                print(f"Negative mean square value at frame starting at index {i}: {mean_square}")
                mean_square = 0
                
            rms = np.sqrt(mean_square)
            if np.isnan(rms):
                print(f"NaN RMS value at frame starting at index {i} with mean square: {mean_square}")
                rms = 0
                
            rms_values.append(rms)

    # Find the max RMS value for normalization
    max_rms = max(rms_values)

    # Convert RMS values to values between 0 and 65535
    normalized_values = [rms_to_value(rms, max_rms) for rms in rms_values]

    # Write to txt file
    with open('output.txt', 'w') as file:
        for value in normalized_values:
            file.write(f"{value}\n")

if __name__ == "__main__":
    main()
