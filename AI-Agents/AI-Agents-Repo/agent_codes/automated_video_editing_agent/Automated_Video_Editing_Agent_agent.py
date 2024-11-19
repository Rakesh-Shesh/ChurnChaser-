from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx import fadein, fadeout, colorx
from moviepy.audio.fx import audio_normalize


class ComplexAutomatedVideoEditingAgent:
    def __init__(self, video_files):
        self.video_files = video_files
        self.clips = [VideoFileClip(video) for video in video_files]
        self.audio_clips = []
        self.text_clips = []

    def trim_clips(self, start_times, end_times):
        if len(start_times) != len(end_times):
            raise ValueError('Start times and end times must be of the same length')
        self.clips = [clip.subclip(start, end) for clip, start, end in zip(self.clips, start_times, end_times)]

    def add_text(self, texts, durations, fontsize=24, color='white', font='Arial'):
        text_clips = [
            TextClip(txt, fontsize=fontsize, color=color, font=font).set_duration(duration).set_position('center') for
            txt, duration in zip(texts, durations)]
        self.text_clips.extend(text_clips)

    def add_audio(self, audio_files):
        """Add background music or audio to the video."""
        for audio_file in audio_files:
            audio_clip = AudioFileClip(audio_file)
            self.audio_clips.append(audio_clip)

    def apply_transitions(self, fade_duration=1):
        """Apply fade transitions between clips."""
        self.clips = [fadein(clip, fade_duration) for clip in self.clips]
        self.clips = [fadeout(clip, fade_duration) for clip in self.clips]

    def apply_visual_effects(self, brightness_factor=1.2, contrast_factor=1.0):
        """Apply visual effects such as color correction."""
        self.clips = [colorx(clip, brightness_factor) for clip in self.clips]
        self.clips = [clip.fx("colorx", contrast_factor) for clip in self.clips]

    def concatenate_clips(self):
        """Concatenate all video clips together."""
        final_clip = concatenate_videoclips(self.clips)
        if self.text_clips:
            final_clip = CompositeVideoClip([final_clip] + self.text_clips)
        if self.audio_clips:
            final_audio = concatenate_videoclips(self.audio_clips).volumex(0.5)  # Reduce audio volume if needed
            final_clip = final_clip.set_audio(final_audio)
        return final_clip

    def write_video(self, output_file, fps=24):
        """Export the final video to a file."""
        final_clip = self.concatenate_clips()
        final_clip.write_videofile(output_file, fps=fps)


if __name__ == "__main__":
    # Initialize agent with video files
    agent = ComplexAutomatedVideoEditingAgent(['video1.mp4', 'video2.mp4'])

    # Trim clips
    agent.trim_clips([0, 5], [10, 15])

    # Add text overlay
    agent.add_text(['First clip', 'Second clip'], [10, 10])

    # Add audio to the video
    agent.add_audio(['background_audio.mp3'])

    # Apply fade transitions between clips
    agent.apply_transitions(fade_duration=2)

    # Apply visual effects
    agent.apply_visual_effects(brightness_factor=1.5, contrast_factor=1.2)

    # Write the final video to file
    agent.write_video('final_output.mp4')
