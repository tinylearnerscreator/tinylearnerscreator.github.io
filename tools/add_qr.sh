#!/usr/bin/env bash
# Put the home-page QR card on the last seconds of a finished video.
# Usage: add_qr.sh IN.mp4 OUT.mp4 [SECONDS=4]
# 16:9 (wide): card at 36% of the height, bottom right corner.
# 9:16 (tall): card at 24% of the width, left side, bottom edge at 78% of the
#   height, so it stays out of TikTok's bottom 22% and right-hand buttons, and
#   below the PLAY AGAIN? bar (9 to 21.5%).
# The card fades in over 0.4 s. Audio is copied unchanged.
# Override the spot with QR_POS: QR_POS=topleft puts it beside a centered
# cover (top left, level with the upper third, used for gift ads), or
# QR_POS=X,Y sets the top-left pixel of the card.
set -euo pipefail
in=$1; out=$2; sec=${3:-4}
here=$(cd "$(dirname "$0")" && pwd)
card="$here/../img/qr/home-card.png"
if [ ! -f "$card" ]; then
  card=$(mktemp --suffix=.png)
  curl -fsSL https://tinylearnerscreator.github.io/img/qr/home-card.png -o "$card"
fi
read -r w h < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$in" | tr x ' ')
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")
start=$(python3 -c "print(max(0.0, $dur - $sec))")
if [ "$w" -ge "$h" ]; then
  ch=$(( h * 36 / 100 )); cw=$(( ch * 1000 / 1290 ))
  x=$(( w - cw - w * 3 / 100 )); y=$(( h - ch - h * 5 / 100 ))
else
  cw=$(( w * 24 / 100 )); ch=$(( cw * 1290 / 1000 ))
  x=$(( w * 5 / 100 )); y=$(( h * 78 / 100 - ch ))
fi
case "${QR_POS:-}" in
  "") ;;
  topleft) x=$(( (w * 30 / 100 - cw) / 2 )); [ "$x" -lt 10 ] && x=10; y=$(( h * 15 / 100 )) ;;
  *,*) x=${QR_POS%,*}; y=${QR_POS#*,} ;;
esac
ffmpeg -y -v error -i "$in" -loop 1 -i "$card" -filter_complex \
 "[1:v]scale=${cw}:-1:flags=lanczos,format=rgba,fade=in:st=${start}:d=0.4:alpha=1[q];[0:v][q]overlay=${x}:${y}:enable='gte(t,${start})':shortest=1[v]" \
 -map "[v]" -map 0:a? -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -c:a copy -movflags +faststart "$out"
echo "QR card on $out from ${start}s at ${cw}x${ch}+${x}+${y}"
