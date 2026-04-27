---
name: ffmpeg-editor
description: >
  Professional video editing automation using FFmpeg via bash. Use this skill whenever
  the user wants to cut, trim, shorten, extend, merge, or split video clips; add text
  overlays, titles, or subtitles (SRT/ASS); mix, replace, or remove audio tracks;
  apply fade in/out, speed changes, or basic motion effects; convert between formats
  (MP4, MOV, MKV, WebM, GIF); extract frames or thumbnails; add watermarks or logos;
  or batch-process multiple video files. Trigger even if the user says things like
  "cut the video", "add a title", "remove the audio", "make it faster", "loop it",
  "merge these clips", or "export as GIF". Always use this skill for any video
  manipulation task — never improvise FFmpeg commands without it.
---

# FFmpeg Video Editor Skill

Automated video editing via FFmpeg bash commands. Handles the full editing pipeline:
cutting, text, audio, effects, format conversion, and batch processing.

## Workflow

1. **Identify the task** — determine which operation(s) are needed (see categories below)
2. **Check the input file** — verify it exists at the given path, inspect metadata
3. **Read the relevant reference** — load `references/commands.md` for the exact FFmpeg syntax
4. **Build and run the command** — execute via bash_tool, capture stderr for errors
5. **Verify output** — check file was created, inspect duration/resolution if relevant
6. **Present the file** — use present_files to deliver the result to the user

## Operation Categories

### ✂️ Cutting & Timing
- Trim (start → end), cut middle section out, split into segments
- Speed up / slow down (setpts, atempo)
- Loop N times, freeze last frame, extend with black/white padding
- Add silent/blank intro or outro

### 📝 Text & Titles
- Text overlay at any position, size, color, font, with timing (drawtext)
- Fade-in / fade-out title card (solid background + text)
- Burned-in subtitles from SRT file (subtitles filter)
- ASS/SSA styled subtitles
- Lower-third graphic strip with text

### 🔊 Audio
- Replace audio track entirely
- Mix two audio tracks (video audio + background music)
- Remove audio (mute)
- Adjust volume, fade audio in/out
- Extract audio only (MP3/AAC output)
- Add audio to silent video

### 🎬 Effects & Motion
- Fade in / fade out video (fades filter)
- Zoom in / Ken Burns effect (zoompan)
- Horizontal/vertical flip, rotate
- Blur, sharpen, brightness/contrast adjustments
- Picture-in-picture (overlay)
- Side-by-side / stacked layout (hstack, vstack)

### 🔗 Merging & Splitting
- Concatenate multiple clips in order (concat demuxer)
- Split one video into N equal parts
- Stack or tile multiple videos

### 🖼️ Format & Export
- Convert MP4 ↔ MOV ↔ MKV ↔ WebM
- Export as animated GIF (with palette optimization)
- Extract thumbnail / frame at timestamp
- Compress to target file size or bitrate
- Add watermark / logo image overlay

### 📦 Batch Processing
- Apply same operation to all files in a folder
- Rename outputs systematically

## Reference Files

- `references/commands.md` — exact FFmpeg filter syntax for every operation above
  Read this before building any command.

## Key Rules

- Always use `-y` flag to overwrite output without prompt
- Use `-c:v libx264 -c:a aac` for MP4 output unless user specifies otherwise
- For drawtext: escape special characters (`:` → `\:`, `'` → `\'`)
- For concat: build a temp `filelist.txt`, use `concat demuxer` not filter for lossless
- Font path for Hebrew/RTL text: check available fonts first with `fc-list | grep -i hebrew`
- Always output to `/mnt/user-data/outputs/` and present_files at the end
- On error: show stderr to user and suggest fix

## Input Handling

- Files uploaded by user are at `/mnt/user-data/uploads/`
- Always run `ffprobe` first to get duration, resolution, codec, audio info
- If user gives a timestamp like "from 0:30 to 1:45" → convert to seconds for -ss/-to
