# Demo Audio Setup for Landing Page

The landing page includes a demo section that showcases audio separation. To enable this feature, you need to provide sample audio files.

## Required Files

Place the following audio files in the `frontend/demo/` directory:

1. **original.mp3** - The original mixed audio track (30-60 seconds recommended)
2. **vocals.mp3** - The isolated vocals stem
3. **drums.mp3** - The isolated drums stem
4. **bass.mp3** - The isolated bass stem
5. **other.mp3** - The isolated other instruments stem

## Directory Structure

```
frontend/
├── demo/
│   ├── original.mp3
│   ├── vocals.mp3
│   ├── drums.mp3
│   ├── bass.mp3
│   └── other.mp3
├── index.html
├── app.js
└── styles.css
```

## Obtaining Demo Files

### Option 1: Use Your Own Processed Audio
1. Upload a song through the application
2. Download the separated stems
3. Copy the files to `frontend/demo/` with the names above

### Option 2: Use Free Sample Audio
1. Find royalty-free music from sites like:
   - Free Music Archive (freemusicarchive.org)
   - ccMixter (ccmixter.org)
   - Incompetech (incompetech.com)
2. Process the audio through Demucs
3. Place the results in `frontend/demo/`

### Option 3: Generate Test Files
For testing purposes, you can create silent audio files:
```bash
# Using ffmpeg to create 30-second silent MP3 files
ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 30 -q:a 9 -acodec libmp3lame original.mp3
ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 30 -q:a 9 -acodec libmp3lame vocals.mp3
ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 30 -q:a 9 -acodec libmp3lame drums.mp3
ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 30 -q:a 9 -acodec libmp3lame bass.mp3
ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 30 -q:a 9 -acodec libmp3lame other.mp3
```

## File Size Recommendations

- Keep files under 2MB each for fast loading
- Use 30-60 seconds of audio (longer files increase page load time)
- Use 128-192 kbps MP3 encoding for good quality at reasonable size

## Important Notes

- The landing page will still function without demo files, but the audio players will show errors
- Make sure audio files are publicly accessible (don't require authentication)
- Consider using a CDN or object storage for production deployments
- Ensure you have proper rights/licenses for any audio used in the demo
