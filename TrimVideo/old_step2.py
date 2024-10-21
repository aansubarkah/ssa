from moviepy.editor import VideoFileClip
import os

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

def create_video_clips(input_video, timestamps_file, output_folder):
  os.makedirs(output_folder, exist_ok=True)
  timestamps = read_timestamps(timestamps_file)
  video = VideoFileClip(input_video)

  for i, (start, end) in enumerate(timestamps):
      start_sec = timestamp_to_seconds(start)
      end_sec = timestamp_to_seconds(end)
      subclip = video.subclip(start_sec, end_sec)
      output_file = os.path.join(output_folder, f"clip_{i+1:03d}.mp4")
      subclip.write_videofile(output_file, codec="libx264", audio_codec="aac")
      print(f"Created: {output_file}")

  video.close()

if __name__ == "__main__":
  input_video = "detect_silence.mp4"
  timestamps_file = "speech_timestamps.txt"
  output_folder = "output_clips"

  create_video_clips(input_video, timestamps_file, output_folder)

# Created/Modified files during execution:
print("Output files:")
for file in os.listdir(output_folder):
  print(os.path.join(output_folder, file))