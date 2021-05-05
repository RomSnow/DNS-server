# DNS-server
Реализация кэширующего DNS сервера на Python

Автор: Ивашкин Роман

## Требования
Для корректной работы программы необходим выход в интернет или к forward DNS серверу (указывается в параметрах)

Интерпретатор Python 3

## Параметры
  ```
  server.py [-h] [--forward FORFARD] [--ttl TTL] [--address ADDRESS]

  -h, --help         справка
  
  --forward FORFARD  IP Forward DNS сервера (default: Open Google sever)
  
  --ttl TTL          ttl записей в кэше
  
  --address ADDRESS  аддресс, по которому можно обратится к серверу
```

## Пример работы
Вывод утилиты `dig`:
```
exampleUSER:~$ dig google.com @127.0.0.1

; <<>> DiG 9.16.6-Ubuntu <<>> google.com @127.0.0.1
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 40978
;; flags: qr rd ra; QUERY: 1, ANSWER: 6, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;google.com.			IN	A

;; ANSWER SECTION:
google.com.		299	IN	A	209.85.233.102
google.com.		299	IN	A	209.85.233.138
google.com.		299	IN	A	209.85.233.139
google.com.		299	IN	A	209.85.233.100
google.com.		299	IN	A	209.85.233.113
google.com.		299	IN	A	209.85.233.101

;; Query time: 48 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Ср мая 05 17:47:10 +05 2021
;; MSG SIZE  rcvd: 124
```

