# Media Recipes

All outputs go to `media/out/` unless told otherwise.

## PDF (poppler)

```sh
pdftotext -layout lecture.pdf media/out/lecture.txt        # whole file
pdftotext -layout -f 3 -l 10 lecture.pdf out.txt           # page range
pdftoppm -png -r 150 -f 4 -l 4 lecture.pdf media/out/p     # one page → PNG
```

Empty or garbled pages are usually scanned images. Render them to PNG and flag them.

## ffmpeg one-liners

```sh
ffmpeg -i in.mp4 -vn -c:a libmp3lame -q:a 2 out.mp3          # video → audio
ffmpeg -i in.mkv -c copy out.mp4                             # container swap, no re-encode
ffmpeg -i in.mov -c:v libx264 -crf 22 -preset medium -c:a aac out.mp4
ffmpeg -ss 00:01:30 -to 00:05:00 -i in.mp4 -c copy clip.mp4  # trim
ffmpeg -i in.m4a -ar 16000 -ac 1 out.wav                     # 16 kHz mono for transcription
ffmpeg -i in.mp4 -vf fps=1/5 frame-%03d.png                  # a frame every 5 s
ffprobe -v error -show_format -show_streams in.mp4           # inspect
```

## Batch loop (fish)

```fish
for f in media/my-env/*.pdf
    pdftotext -layout $f media/out/(basename $f .pdf).txt
end
```

Quote paths with spaces.
