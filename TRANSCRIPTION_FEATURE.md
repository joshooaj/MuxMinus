# Whisper Transcription Feature Implementation Summary

This document summarizes the implementation of OpenAI Whisper speech-to-text transcription support in Mux Minus.

## Overview

The Mux Minus service has been extended to support audio and video transcription using OpenAI's Whisper model. This includes:

1. Basic text transcription
2. Timestamped transcription (JSON format)
3. Subtitle generation (SRT/VTT formats)
4. Lyrics extraction (LRC format)

## Backend Changes

### New Dependencies
- `openai-whisper>=20231117` added to `backend/requirements.txt`

### New Files
- **`backend/app/transcriber.py`**: Core transcription service using Whisper
  - Implements `TranscriptionService` class
  - Supports multiple output formats: TXT, JSON, SRT, VTT, LRC
  - Includes timestamp formatting utilities
  - Auto-detects language or accepts language code parameter

### Modified Files

**`backend/app/models.py`**:
- Added `JobType` enum: `SEPARATION`, `TRANSCRIPTION`
- Added `TranscriptionType` enum: `BASIC`, `TIMESTAMPED`, `SUBTITLES`, `LYRICS`
- Added `TranscriptionFormat` enum: `TEXT`, `JSON`, `SRT`, `VTT`, `LRC`
- Added `TranscriptionRequest` Pydantic model

**`backend/app/queue.py`**:
- Extended `Job` dataclass to support all job types with transcription fields
- Added `_process_transcription()` method for handling transcription jobs
- Updated `submit()` method to accept job type and transcription parameters

**`backend/app/main.py`**:
- Added `/transcribe` endpoint for submitting transcription jobs
- Enforces 5GB file size limit for transcription
- Existing `/jobs` endpoint continues to handle separation jobs

## Frontend Changes

### Modified Files

**`app/core/models.py`**:
- Added `JobType`, `TranscriptionType`, and `TranscriptionFormat` choices
- Extended `Job` model with new fields:
  - `job_type`: Type of processing job
  - `transcription_type`: Type of transcription (if applicable)
  - `transcription_format`: Output format (if applicable)
  - `language`: Language code for transcription
- Made `model` field nullable (only required for separation jobs)

**`app/core/migrations/0004_add_transcription_support.py`**:
- Migration to add new fields to Job model

**`app/core/forms.py`**:
- Extended `JobCreateForm` to support transcription job types
- Added job type selection (separation, transcription)
- Added transcription-specific fields (type, format, language)
- Updated file validation:
  - 100MB limit for separation jobs
  - 5GB limit for transcription jobs
  - Added video format support (.mp4, .mkv, .avi, etc.)

**`app/core/backend_client.py`**:
- Added `submit_transcription_job()` method

**`app/core/views.py`**:
- Updated `create_job()` view:
  - Routes to appropriate backend endpoint based on job type
  - Creates job with appropriate fields based on type
- Updated `job_detail()` view:
  - Displays transcription output files
  - Shows text preview for transcription results
  - Handles both audio stems and transcription files

**`app/templates/core/landing.html`**:
- Updated hero section to mention transcription
- Added new "Speech-to-Text Transcription" section showcasing:
  - Basic transcription
  - Timestamped text
  - Subtitle generation
  - Lyrics (LRC)

## Features Implemented

### 1. Basic Transcription (1 credit)
- Converts speech from audio/video to plain text
- Auto-detects language or accepts language code
- Output: `.txt` file

### 2. Timestamped Transcription (1 credit)
- Provides transcription with timestamps for each segment
- Useful for video chapters or navigation
- Output: `.json` file with segments array

### 3. Subtitle Generation (1 credit)
- Creates subtitle files ready for video players
- Supports both SRT and WebVTT formats
- Output: `.srt` or `.vtt` file

### 4. Lyrics Generation (1 credit)
- Generates timestamped lyrics in LRC format
- Whisper transcribes directly from audio
- Output: `.lrc` lyrics file

## Credit System

- **Separation jobs**: 1 credit
- **Transcription jobs**: 1 credit

## File Size Limits

- **Separation jobs**: 100MB (unchanged)
- **Transcription jobs**: 5GB (to accommodate video files)

## Supported File Formats

### Audio Formats (all job types)
- MP3, WAV, FLAC, OGG, M4A, AAC, WMA, AIFF

### Video Formats (transcription only)
- MP4, MKV, AVI, MOV, WebM

## API Endpoints

### New Endpoints

**POST /transcribe**
```json
{
  "job_id": "uuid",
  "input_path": "user_id/filename.mp3",
  "transcription_type": "basic|timestamped|subtitles|lyrics",
  "transcription_format": "txt|json|srt|vtt|lrc",
  "language": "en" // optional, null for auto-detect
}
```

### Existing Endpoint (unchanged)

**POST /jobs**
```json
{
  "job_id": "uuid",
  "input_path": "user_id/audio.mp3",
  "model": "htdemucs",
  "two_stem": "vocals",
  "output_format": "mp3"
}
```

## Output File Structure

### Separation Jobs
```
outputs/
  {job_id}/
    vocals.mp3
    drums.mp3
    bass.mp3
    other.mp3
```

### Transcription Jobs
```
outputs/
  {job_id}/
    transcription.txt  (or .json, .srt, .vtt)
```

### Lyrics Pipeline Jobs
```
outputs/
  {job_id}/
    vocals/
      vocals.wav        # Isolated vocals
      no_vocals.wav     # Instrumental
    lyrics.lrc          # Timestamped lyrics
```

## What's Left to Do

### High Priority
1. **Update job_detail.html template**: Add UI for displaying transcription results (text preview, download buttons)
2. **Testing**: Test all transcription types end-to-end
3. **Demo page**: Add example transcription outputs to the demo page

### Medium Priority
4. **Error handling**: Improve error messages for failed transcription jobs
5. **Progress indicators**: Better progress reporting during the two-step lyrics pipeline
6. **Documentation**: Update README.md with transcription feature documentation

### Low Priority
7. **Optimization**: Consider caching Whisper model in memory for faster processing
8. **Language selection UI**: Provide dropdown of supported languages instead of text input
9. **Preview limits**: Limit text preview to first 1000 characters for very long transcriptions

## Known Limitations

1. **Model size**: Currently uses Whisper "base" model (faster but less accurate). Can be changed to "medium" or "large" for better quality.
2. **GPU support**: Transcription will be much faster with GPU support (CUDA)
3. **Very long files**: Processing time increases linearly with audio duration
4. **Music lyrics accuracy**: Results depend on vocal clarity in the mix

## Testing Recommendations

1. Test basic transcription with a short speech audio file
2. Test subtitle generation with a video file
3. Test lyrics pipeline with a music file
4. Verify credit deduction (1 vs 2 credits)
5. Verify file size limits (reject files over 5GB for transcription)
6. Test with various languages to verify auto-detection
7. Check output file formats are correct

## Performance Notes

- Whisper "base" model: ~8x faster than realtime on CPU
- Lyrics pipeline: Processing time = Demucs time + Whisper time
- 5GB file limit allows ~8 hours of high-quality audio
- Consider implementing queue limits to prevent overwhelming the system
