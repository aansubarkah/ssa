import os, glob
import tkinter as tk
from tkinter import filedialog
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from moviepy.editor import VideoFileClip, concatenate_videoclips

def select_input_file():
  root = tk.Tk()
  root.withdraw()  # Hide the main window
  file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
  return file_path

def select_output_file():
  root = tk.Tk()
  root.withdraw()  # Hide the main window
  file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
  return file_path

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

def read_timestamps(file_path):
  timestamps = []
  with open(file_path, 'r') as f:
      for line in f:
          start, end = line.strip().split(' - ')
          timestamps.append((start, end))
  return timestamps

def timestamp_to_seconds(timestamp):
  h, m, s = map(int, timestamp.split(':'))
  return h * 3600 + m * 60 + s

def seconds_to_timestamp(seconds):
  seconds = int(seconds)
  h, r = divmod(seconds, 3600)
  m, s = divmod(r, 60)
  return f"{h:02d}:{m:02d}:{s:02d}"

def clean_output_folder(output_folder):
    files = glob.glob(os.path.join(output_folder, '*.mp4'))
    for file in files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error deleting file: {e}")

def create_video_clips(input_video, timestamps_file, output_folder):
  os.makedirs(output_folder, exist_ok=True)
  clean_output_folder(output_folder)

  timestamps = read_timestamps(timestamps_file)
  
  try:
      video = VideoFileClip(input_video)
  except Exception as e:
      print(f"Error loading video file: {e}")
      return

  video_duration = video.duration

  for i, (start, end) in enumerate(timestamps):
      start_sec = timestamp_to_seconds(start)
      end_sec = timestamp_to_seconds(end)

      if start_sec > 0:
          start_sec -= 1
          start = seconds_to_timestamp(start_sec)
          print(f"Adjusted start time for clip {i+1}: {start}")
      
      if end_sec < video_duration:
          end_sec += 1
          end = seconds_to_timestamp(end_sec)
          print(f"Adjusted end time for clip {i+1}: {end}")
      
      if start_sec == end_sec:
          end_sec += 1
          end = seconds_to_timestamp(end_sec)
          print(f"Adjusted end time for clip {i+1}: {end}")
      
      if end_sec <= start_sec or start_sec >= video_duration:
          print(f"Skipping invalid timestamp: {start} - {end}")
          continue
      
      if end_sec > video_duration:
          print(f"Adjusting end time from {end} to video end")
          end_sec = video_duration
          end = seconds_to_timestamp(end_sec)

      try:
          subclip = video.subclip(start_sec, end_sec)
          output_file = os.path.join(output_folder, f"clip_{i+1:03d}.mp4")
          subclip.write_videofile(output_file, codec="libx264", audio_codec="aac")
          print(f"Created: {output_file}")
      except Exception as e:
          print(f"Error creating clip {i+1}: {e}")

  video.close()

def concatenate_videos(input_folder, output_file):
  video_files = [f for f in os.listdir(input_folder) if f.endswith('.mp4')]
  video_files.sort()

  clips = []
  for video_file in video_files:
      file_path = os.path.join(input_folder, video_file)
      clip = VideoFileClip(file_path)
      clips.append(clip)

  final_clip = concatenate_videoclips(clips)
  final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

  final_clip.close()
  for clip in clips:
      clip.close()

  print(f"Concatenated video saved as: {output_file}")

def main():
  video_path = select_input_file()
  if not video_path:
      print("No input file selected. Exiting.")
      return

  final_output = select_output_file()
  if not final_output:
      print("No output file selected. Exiting.")
      return

  output_folder = os.path.join(os.path.dirname(final_output), "output_clips")
  audio_path = os.path.join(os.path.dirname(final_output), "temp_audio.wav")
  timestamps_file = os.path.join(os.path.dirname(final_output), "speech_timestamps.txt")
  
  print("Extracting audio from video...")
  extract_audio(video_path, audio_path)
  
  print("Detecting non-silent periods...")
  non_silent_ranges = detect_speech(audio_path)
  
  print("Writing timestamps to file...")
  write_timestamps(non_silent_ranges, timestamps_file)
  
  print("Creating video clips...")
  create_video_clips(video_path, timestamps_file, output_folder)
  
  print("Concatenating video clips...")
  concatenate_videos(output_folder, final_output)
  
  print("Cleaning up temporary files...")
  os.remove(audio_path)
  os.remove(timestamps_file)
  
  print(f"Process completed. Final video: {final_output}")

  # Print created/modified files
  print("\nCreated/Modified files:")
  print(audio_path)
  print(timestamps_file)
  print("\nOutput clips:")
  for file in os.listdir(output_folder):
      print(os.path.join(output_folder, file))
  print("\nFinal output:")
  print(final_output)

if __name__ == "__main__":
  main()