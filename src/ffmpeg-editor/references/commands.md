# FFmpeg Command Reference

## Inspect Input
```bash
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4
```

---

## ✂️ Cutting & Timing

### Trim (start to end)
```bash
ffmpeg -y -ss 00:00:30 -to 00:01:45 -i input.mp4 -c copy output.mp4
# For frame-accurate (re-encode):
ffmpeg -y -i input.mp4 -ss 00:00:30 -to 00:01:45 -c:v libx264 -c:a aac output.mp4
```

### Cut out middle section
```bash
# Keep 0–30s and 60s–end, remove 30–60s
ffmpeg -y -i input.mp4 -vf "select='not(between(t,30,60))',setpts=N/FRAME_RATE/TB" \
  -af "aselect='not(between(t,30,60))',asetpts=N/SR/TB" output.mp4
```

### Speed up / slow down
```bash
# 2x faster (video + audio)
ffmpeg -y -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" \
  -map "[v]" -map "[a]" output.mp4
# 0.5x slower
ffmpeg -y -i input.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" \
  -map "[v]" -map "[a]" output.mp4
```

### Loop N times
```bash
ffmpeg -y -stream_loop 3 -i input.mp4 -c copy output.mp4
```

### Extend with freeze frame at end
```bash
# Freeze last frame for 3 extra seconds (total)
ffmpeg -y -i input.mp4 -vf "tpad=stop_mode=clone:stop_duration=3" -c:a copy output.mp4
```

---

## 📝 Text & Titles

### Text overlay (basic)
```bash
ffmpeg -y -i input.mp4 -vf \
  "drawtext=text='My Title':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:\
box=1:boxcolor=black@0.5:boxborderw=10" \
  -c:a copy output.mp4
```

### Text overlay with timing (appears 2s–5s)
```bash
ffmpeg -y -i input.mp4 -vf \
  "drawtext=text='Hello World':fontsize=48:fontcolor=yellow:\
x=50:y=50:enable='between(t,2,5)'" \
  -c:a copy output.mp4
```

### Fade-in title card (black bg + centered text, 3 seconds)
```bash
ffmpeg -y -f lavfi -i color=c=black:s=1920x1080:d=3 \
  -vf "drawtext=text='My Film':fontsize=80:fontcolor=white:\
x=(w-text_w)/2:y=(h-text_h)/2,fade=t=in:d=0.5,fade=t=out:st=2.5:d=0.5" \
  -c:v libx264 title.mp4
```

### Concat title card + main video
```bash
echo "file 'title.mp4'" > /tmp/filelist.txt
echo "file 'main.mp4'" >> /tmp/filelist.txt
ffmpeg -y -f concat -safe 0 -i /tmp/filelist.txt -c copy output.mp4
```

### Burned-in SRT subtitles
```bash
ffmpeg -y -i input.mp4 -vf "subtitles=subtitles.srt:force_style='FontSize=24,PrimaryColour=&HFFFFFF'" \
  -c:a copy output.mp4
```

### Lower-third strip
```bash
ffmpeg -y -i input.mp4 -vf \
  "drawbox=x=0:y=ih-80:w=iw:h=80:color=black@0.7:t=fill,\
drawtext=text='Hemi Michaeli':fontsize=32:fontcolor=white:x=20:y=h-55" \
  -c:a copy output.mp4
```

---

## 🔊 Audio

### Remove audio (mute)
```bash
ffmpeg -y -i input.mp4 -c:v copy -an output.mp4
```

### Replace audio track
```bash
ffmpeg -y -i input.mp4 -i new_audio.mp3 -c:v copy -map 0:v -map 1:a \
  -shortest output.mp4
```

### Mix original audio + background music
```bash
ffmpeg -y -i input.mp4 -i music.mp3 \
  -filter_complex "[0:a]volume=1.0[orig];[1:a]volume=0.3[music];[orig][music]amix=inputs=2[a]" \
  -map 0:v -map "[a]" -c:v copy -shortest output.mp4
```

### Fade audio in/out
```bash
# Fade in 2s, fade out last 2s of a 30s video
ffmpeg -y -i input.mp4 -af "afade=t=in:d=2,afade=t=out:st=28:d=2" -c:v copy output.mp4
```

### Extract audio only
```bash
ffmpeg -y -i input.mp4 -vn -c:a libmp3lame -q:a 2 output.mp3
```

### Adjust volume
```bash
ffmpeg -y -i input.mp4 -af "volume=1.5" -c:v copy output.mp4
```

---

## 🎬 Effects & Motion

### Fade in / fade out video
```bash
# Fade in 1s, fade out last 1s of 30s video
ffmpeg -y -i input.mp4 \
  -vf "fade=t=in:d=1,fade=t=out:st=29:d=1" \
  -af "afade=t=in:d=1,afade=t=out:st=29:d=1" output.mp4
```

### Ken Burns zoom effect
```bash
ffmpeg -y -i input.mp4 \
  -vf "zoompan=z='min(zoom+0.002,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=1920x1080" \
  -c:a copy output.mp4
```

### Flip horizontal
```bash
ffmpeg -y -i input.mp4 -vf hflip -c:a copy output.mp4
```

### Rotate 90° clockwise
```bash
ffmpeg -y -i input.mp4 -vf "transpose=1" -c:a copy output.mp4
```

### Picture-in-picture (overlay small video on main)
```bash
ffmpeg -y -i main.mp4 -i overlay.mp4 \
  -filter_complex "[1:v]scale=320:180[pip];[0:v][pip]overlay=W-320-10:H-180-10" \
  -c:a copy output.mp4
```

### Side by side
```bash
ffmpeg -y -i left.mp4 -i right.mp4 \
  -filter_complex "[0:v][1:v]hstack=inputs=2[v]" \
  -map "[v]" -c:v libx264 output.mp4
```

---

## 🔗 Merging

### Concatenate clips (same codec)
```bash
printf "file '%s'\n" clip1.mp4 clip2.mp4 clip3.mp4 > /tmp/filelist.txt
ffmpeg -y -f concat -safe 0 -i /tmp/filelist.txt -c copy output.mp4
```

### Concatenate clips (different codecs — re-encode)
```bash
ffmpeg -y -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" output.mp4
```

---

## 🖼️ Format & Export

### Convert to MP4
```bash
ffmpeg -y -i input.mov -c:v libx264 -c:a aac -movflags +faststart output.mp4
```

### Export as GIF (optimized)
```bash
ffmpeg -y -i input.mp4 -vf "fps=15,scale=640:-1:flags=lanczos,split[s0][s1];\
[s0]palettegen[p];[s1][p]paletteuse" output.gif
```

### Extract thumbnail at 5s
```bash
ffmpeg -y -ss 5 -i input.mp4 -frames:v 1 thumbnail.jpg
```

### Compress to ~10MB target
```bash
# Calculate bitrate: (target_size_bytes * 8) / duration_seconds
ffmpeg -y -i input.mp4 -b:v 800k -maxrate 800k -bufsize 1600k -c:a aac -b:a 128k output.mp4
```

### Add image watermark (bottom-right)
```bash
ffmpeg -y -i input.mp4 -i logo.png \
  -filter_complex "[1:v]scale=100:-1[logo];[0:v][logo]overlay=W-w-10:H-h-10" \
  -c:a copy output.mp4
```

---

## 📦 Batch Processing

### Apply trim to all MP4s in folder
```bash
for f in /path/to/folder/*.mp4; do
  name=$(basename "$f" .mp4)
  ffmpeg -y -ss 0 -to 30 -i "$f" -c copy "/mnt/user-data/outputs/${name}_trimmed.mp4"
done
```

---

## Font Check (for Hebrew text)
```bash
fc-list | grep -i hebrew
fc-list | grep -i noto
# Use found path in drawtext: fontfile='/path/to/font.ttf'
```
