import moviepy.editor as mp
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os

def extract_audio(video_path, audio_path):
  video = mp.VideoFileClip(video_path)
  video.audio.write_audiofile(audio_path)

def detect_speech(audio_path, min_silence_len=1000, silence_thresh=-40):
  audio = AudioSegment.from_wav(audio_path)
  non_silent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
  return non_silent_ranges

def format_timestamp(ms):
  seconds = int(ms / 1000)
  minutes, seconds = divmod(seconds, 60)
  hours, minutes = divmod(minutes, 60)
  return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def write_timestamps(non_silent_ranges, output_file):
  with open(output_file, 'w') as f:
      for start, end in non_silent_ranges:
          f.write(f"{format_timestamp(start)} - {format_timestamp(end)}\n")

def main(video_path, output_file):
  audio_path = "temp_audio.wav"
  
  print("Extracting audio from video...")
  extract_audio(video_path, audio_path)
  
  print("Detecting non-silent periods...")
  non_silent_ranges = detect_speech(audio_path)
  
  print("Writing timestamps to file...")
  write_timestamps(non_silent_ranges, output_file)
  
  print("Cleaning up temporary files...")
  os.remove(audio_path)
  
  print(f"Timestamps have been written to {output_file}")

if __name__ == "__main__":
  video_path = "detect_silence.mp4"  # Replace with your video file path
  output_file = "speech_timestamps.txt"
  main(video_path, output_file)

# Created/Modified files during execution:
print("temp_audio.wav")
print("speech_timestamps.txt")