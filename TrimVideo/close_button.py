import os
import glob
import tkinter as tk
from tkinter import filedialog, ttk
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from moviepy.editor import VideoFileClip, concatenate_videoclips
import threading
import time


def format_duration(duration_seconds):
    hours, remainder = divmod(int(duration_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


class ProgressBar:
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Removing Silence from Video")
        self.window.geometry("500x300")
        self.progress = ttk.Progressbar(
            self.window, length=450, mode='determinate')
        self.progress.pack(pady=20)
        self.label = tk.Label(self.window, text="Starting...")
        self.label.pack()
        self.time_label = tk.Label(self.window, text="Time: 00:00:00")
        self.time_label.pack()
        self.info_label = tk.Label(
            self.window, text="", justify=tk.LEFT, wraplength=400)
        self.info_label.pack(pady=10)
        self.close_button = tk.Button(
            self.window, text="Close", command=self.close)
        self.close_button.pack(pady=10)
        self.close_button.pack_forget()  # Hide the button initially
        self.start_time = time.time()
        self.is_running = True
        self.update_time()

    def update(self, value, text):
        self.progress['value'] = value
        self.label.config(text=text)
        self.window.update()

    def update_time(self):
        if self.is_running:
            elapsed_time = int(time.time() - self.start_time)
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}"
            self.time_label.config(text=time_str)
            self.window.after(1000, self.update_time)

    def stop_timer(self):
        self.is_running = False

    def show_info(self, input_path, output_path, input_duration, output_duration, process_time):
        self.stop_timer()
  # def show_info(self, input_path, output_path, input_duration, output_duration, process_time):
      # info_text = f"Original video: {input_path}\n"
      # info_text += f"Output video: {output_path}\n"
      # info_text = f"Original duration: {input_duration:.2f} seconds\n"
      # info_text += f"Output duration: {output_duration:.2f} seconds\n"
      # info_text += f"Processing time: {process_time:.2f} seconds"
        info_text = f"Original duration: {format_duration(input_duration)}\n"
        info_text += f"Output duration: {format_duration(output_duration)}\n"
        info_text += f"Processing time: {format_duration(process_time)}"
        self.info_label.config(text=info_text)
        self.close_button.pack()  # Show the close button

    def close(self):
        self.window.destroy()
        self.master.quit()

# ... (keep all other functions as they are)


def main():
    video_path = select_input_file()
    if not video_path:
        print("No input file selected. Exiting.")
        return

    final_output = select_output_file()
    if not final_output:
        print("No output file selected. Exiting.")
        return

    root = tk.Tk()
    root.withdraw()
    progress_bar = ProgressBar(root)

    def process_video():
        start_time = time.time()
        output_folder = os.path.join(
            os.path.dirname(final_output), "output_clips")
        audio_path = os.path.join(
            os.path.dirname(final_output), "temp_audio.wav")
        timestamps_file = os.path.join(os.path.dirname(
            final_output), "speech_timestamps.txt")

        progress_bar.update(10, "Extracting audio from video...")
        extract_audio(video_path, audio_path)

        progress_bar.update(20, "Detecting non-silent periods...")
        non_silent_ranges = detect_speech(audio_path)

        progress_bar.update(30, "Writing timestamps to file...")
        write_timestamps(non_silent_ranges, timestamps_file)

        progress_bar.update(40, "Creating video clips...")
        create_video_clips(video_path, timestamps_file, output_folder)

        progress_bar.update(80, "Concatenating video clips...")
        concatenate_videos(output_folder, final_output)

        progress_bar.update(90, "Cleaning up temporary files...")
        os.remove(audio_path)
        os.remove(timestamps_file)

        progress_bar.update(100, "Process completed!")

        # Get video durations
        input_video = VideoFileClip(video_path)
        output_video = VideoFileClip(final_output)
        input_duration = input_video.duration
        output_duration = output_video.duration
        input_video.close()
        output_video.close()

        # Calculate process time
        process_time = time.time() - start_time - 1

        # Show info on GUI
        progress_bar.show_info(video_path, final_output,
                               input_duration, output_duration, process_time)
        # progress_bar.show_info(video_path, final_output, input_duration, output_duration, process_time)

    processing_thread = threading.Thread(target=process_video)
    processing_thread.start()
    root.mainloop()
    processing_thread.join()  # Wait for the processing thread to finish

# ... (keep all other functions as they are)


def select_input_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    return file_path


def select_output_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    return file_path


def extract_audio(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)


def detect_speech(audio_path, min_silence_len=1000, silence_thresh=-40):
    audio = AudioSegment.from_wav(audio_path)
    non_silent_ranges = detect_nonsilent(
        audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
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
            output_file = os.path.join(output_folder, f"clip_{i+1:05d}.mp4")
            subclip.write_videofile(
                output_file, codec="libx264", audio_codec="aac")
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


if __name__ == "__main__":
    main()
