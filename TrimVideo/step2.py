import os
from moviepy.editor import VideoFileClip

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
  h, r = divmod(seconds, 3600)
  m, s = divmod(r, 60)
  return f"{h:02d}:{m:02d}:{s:02d}"

def create_video_clips(input_video, timestamps_file, output_folder):
  os.makedirs(output_folder, exist_ok=True)
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

      # Always remove 1 second from the start time
      if start_sec > 0:
            start_sec -= 1
            start = seconds_to_timestamp(start_sec)
            print(f"Adjusted start time for clip {i+1}: {start}")
        
      # Always add 1 second to the end time
      if end_sec < video_duration:
            end_sec += 1
            end = seconds_to_timestamp(end_sec)
            print(f"Adjusted end time for clip {i+1}: {end}")
      
      # If start and end are the same, add 1 second to the end
      if start_sec == end_sec:
          end_sec += 1
          end = seconds_to_timestamp(end_sec)
          print(f"Adjusted end time for clip {i+1}: {end}")
      
      # Ensure the end time is after the start time and within video duration
      if end_sec <= start_sec or start_sec >= video_duration:
          print(f"Skipping invalid timestamp: {start} - {end}")
          continue
      
      # Adjust end time if it exceeds video duration
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

if __name__ == "__main__":
  input_video = "detect_silence.mp4"
  timestamps_file = "speech_timestamps.txt"
  output_folder = "output_clips"

  create_video_clips(input_video, timestamps_file, output_folder)

# Created/Modified files during execution:
print("\nOutput files:")
for file in os.listdir(output_folder):
  print(os.path.join(output_folder, file))