#Motion-Nginx-Telegram-Bot
SSL Motion Nginx Telegram Bot

Works for 
* Ubuntu 20.04.5 LTS (Focal Fossa) Raspberry Pi 
* 5.4.0-1077-raspi #88-Ubuntu SMP PREEMPT Mon Nov 28 14:31:37 UTC 2022 aarch64 aarch64 aarch64 GNU/Linux
* python-telegram-bot v13.15 https://github.com/python-telegram-bot/python-telegram-bot/tree/v13.x
* nginx version: nginx/1.18.0 (Ubuntu)
* motion Version 4.5.0+git20221119-ec03434, Copyright 2000-2021 Jeroen Vreeken/Folkert van Heusden/Kenneth Lavrsen/Motion-Project maintainers

Capabilities:
* Telegram realtime notification about Motion triggered evens and timelapse.
* Video files transparently recompressed via FFMPEG before send to save bandwidth and space. Advantage up to 10 times. Telegram engine accepts only MP4 format for preview and instant play.
* NGINX works as reverse proxy, provides SSL support with valid certs and HTTP BASIC AITH for complete access restricton.
* Password authentication does on Nginx side, not Motion. I tested latest builds of Motion and there is capability for SSL and even BASIC AUTH but it still lame and does not work together on different ports, ex. 8080 and 8081. Most browsers decide it is cross-site.
* Telegram Bot Scripts for Motion are able to directly privately to you: send instant text alert, send instant snapshot picture, send recompressed video MP4 wich can natively play in Telegram client. Time lapse and event videos both supported.
* Standalone Python Telegram Bot has capability:
** start and stop Motion,Nginx
** Dump some system statistics like disk usage, CPU load, network connections, process list.
** Negotiage only with you, by sender check.

Lazy installation guide.

Prerequisites, Installation:

Install python3, pip3, pipy and other for python-telegram-bot.
Install python-telegram-bot. For full instruction follow official manual. Focal 20.04 has 13.15 version. Kinda like a command:
#pip install python-telegram-bot --upgrade
Install ffmpeg for converion on a fly and saving bandwidth.
Install certbot python3-certbot python3-certbot-nginx
Install nginx for reverse proxy
Reconfigure your router to forward only 443/ssl port to your server. NAT Loopback is highly recommended.

Configure NGINX.

Write A record to your domain zone accoring to your IP address you owning.
Get Lets Encrypt SSL certificates for your DNS A record by running ex. #certbot -d tg.example.com
Put virtual host config file tg.example.com /etc/nginx/sites-available/ and rename accoding to your DNS. Change paths to your SSL certs and other naming stuff. Enable config by symlinking to /etc/nginx/sites-enabled/tg.example.com
Generate http auth file with pair login:password. Example:
#htpasswd /etc/nginx/tg.example.com.auth jsmith 

Customize Motion.

Change event actions "on_xxxx" accoring to provided snippet Motion.conf.
Put scripts sendmessage.sh sendmediajpg.sh sendmedia.sh bot.sh Motion_tgbot.py to /etc/Motion/, make them executable.
Get your chatId and botToken accoring to official Telegram Bot manual. Write these setting all over these .py .sh scripts.
Do remember keep only localhost access for Motion, we will access to it via Nginx SSL and HTTP BASIC AUTH wich is highly safe for public operations.

Run all at once.
Run Motion, run Nginx. run bot.sh
Find your bot in Telegram. Send /start or /help /status commands. Enjoy menu.
Open URL your Nginx site, ex. https://tg.example.com, , check is all connections are SSL and HTML has no http://127.0.0.1 references.
Open URL ex. https://tg.example.com/str and watch video stream.

Finally.
Check access permissions for all config files with IDs, tokens, user-password pairs. Nginx and Motion must able to access them freely but not other users.
Check all logs if there logged any sensitive data, like CURL requests, cookies, usernames and hashes.
Do remember HTTP BASIC AUTH has no official logout capability or session timout. You may write your own auth mechanism according your fantasy.
Pay attension to "rm" directives in scripts, you may remove or put them back to delete already sended media and save disk space.

