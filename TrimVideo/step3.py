import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def concatenate_videos(input_folder, output_file):
  # Get all mp4 files in the input folder
  video_files = [f for f in os.listdir(input_folder) if f.endswith('.mp4')]
  
  # Sort the files to ensure they're in the correct order
  video_files.sort()

  # Create VideoFileClip objects for each video file
  clips = []
  for video_file in video_files:
      file_path = os.path.join(input_folder, video_file)
      clip = VideoFileClip(file_path)
      clips.append(clip)

  # Concatenate all clips
  final_clip = concatenate_videoclips(clips)

  # Write the result to a file
  final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

  # Close all clips to free up system resources
  final_clip.close()
  for clip in clips:
      clip.close()

  print(f"Concatenated video saved as: {output_file}")

if __name__ == "__main__":
  input_folder = "output_clips"
  output_file = "concatenated_video.mp4"

  concatenate_videos(input_folder, output_file)

# Created/Modified files during execution:
print("\nCreated file:")
print(output_file)