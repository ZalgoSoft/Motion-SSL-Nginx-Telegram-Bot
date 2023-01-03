server {
    listen 443 ssl http2;
    server_name tg.example.com;
    ssl_certificate /etc/letsencrypt/live/tg.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tg.example.com/privkey.pem;

    auth_basic "tg.example.com";
    auth_basic_user_file tg.example.com.auth;

    location /str {
        rewrite /str/(.*) /$1 break;
        proxy_pass http://127.0.0.1:8081/;
    }

    location /video {
        rewrite /video/(.*) /$1 break;
        proxy_pass http://127.0.0.1:1234/;
    }

     location / {
         sub_filter_once off;
         sub_filter "http://127.0.0.1:8081" "https://$host/str";
         sub_filter "http://127.0.0.1:8080" "https://$host";
         proxy_pass http://127.0.0.1:8080/;
    }
}