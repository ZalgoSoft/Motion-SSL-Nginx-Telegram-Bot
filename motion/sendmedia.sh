#!/bin/bash
chatId=yourid
botToken=yourbotToken
fname=$1
tempname=`tempfile`
mv $fname $tempname
nice -n 1 ffmpeg -i $tempname -c:v libx264  -f mp4 -y $fname
if [[ $fname == *.mpg ]]
then
new_name=${fname%.*}.mp4;
mv $fname $new_name
fname=$new_name
fi
nice -n 1 curl -F chat_id=$chatId -F video=@$fname https://api.telegram.org/bot$botToken/sendVideo -F supports_streaming=TRUE -F caption=$2\ $3\ $4\ $5\ $6
#rm $fname
rm $tempname