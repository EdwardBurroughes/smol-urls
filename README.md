# Smol URL
Is a simple application for creating shortened URLs, appreciate this has been
done a thousand times before more of a learning experience w. Django!!

Like all URL shortener's the algorithm used is the Base62 encoder 

## How to

Please create an `.env` file with the following environment vars:
```shell
DEBUG=1
SECRET_KEY=<DJANGO_SECRET_KEY>
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=<YOUR_DB_NAME>
SQL_USER=<YOUR_USER>
SQL_PASSWORD=<YOUR_PASSWORD>
SQL_HOST=db
SQL_PORT=5432
```

**startup**
```shell
docker compose up 
```

**Creating a shortened URL** 
```shell
curl -X POST  http://localhost:8000 \
-H "Content-Type: application/json" \
-d '{"url": "<YOUR_VERY_LONG_URL"}')
```

**Accessing the original URL**
```shell
open <YOUR_SHORTENED_URL>
```

**Deleting a shortened URL**

Bit smelly have a separate end point for deleting, will fix at later date!
```shell
curl -X DELETE <YOUR_SHORTENED_URL>/delete
```