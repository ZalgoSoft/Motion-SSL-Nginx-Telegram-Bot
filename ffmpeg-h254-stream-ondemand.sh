#watch -n 1
ffmpeg -i http://127.0.0.1:8081/0/stream -preset ultrafast -threads 2  -tune zerolatency -b:v 100k -listen 1 -f mp4 -movflags frag_keyframe+empty_moov http://127.0.0.1:1234