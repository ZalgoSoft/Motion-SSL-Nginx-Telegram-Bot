#!/bin/sh
chatId=yourid
botToken=yourbotToken
nice -n 1 curl -F chat_id=$chatId -F photo=@$1  -F caption="Snapshot" https://api.telegram.org/bot$botToken/sendPhoto
rm $1