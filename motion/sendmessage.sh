#!/bin/sh
chatId=yourchatId
botToken=yourbotToken
nice -n 1 curl -F chat_id=$chatId -F "text=$1" https://api.telegram.org/bot$botToken/sendMessage
