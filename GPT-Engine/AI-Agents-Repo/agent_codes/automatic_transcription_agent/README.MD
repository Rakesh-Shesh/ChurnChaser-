# Automatic Transcription Agent

## Overview

The **Automatic Transcription Agent** is a Python-based tool designed to transcribe audio files or live audio input from the microphone into text using speech recognition. This agent utilizes the powerful **Google Speech-to-Text API** via the `speech_recognition` library to transcribe audio in real-time and from pre-recorded audio files.

It supports automatic transcription from a variety of audio sources and can be customized to handle different languages.

### Key Features:
- Transcribe audio from a file (`.wav`, `.flac`, `.mp3`, etc.).
- Transcribe live audio directly from the microphone.
- Support for multiple languages, including English, Spanish, French, and many others.
- Easy integration with other systems for automated transcription workflows.
- Customizable language options.

## Requirements

To use the **Automatic Transcription Agent**, you need to have the following libraries installed:

- `speech_recognition`: This library provides access to the Google Speech API, allowing for accurate transcription of audio.
- `pyaudio`: A required dependency for microphone input (if you want to transcribe live audio).

You can install the required libraries using `pip`:

```bash
pip install SpeechRecognition pyaudio
