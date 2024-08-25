# Dev

### Создать env:
> В директории: `docker` нужно создать файл `.dev.env`

`NETWORK=DEV` \
`DOMAIN=https://app.x-pictures.io/` \
`NGROK_DOMAIN=`

### Собрать образ
```shell
docker build -t x-pictures-backend:latest -f docker/Dockerfile .
```

### Запустить:
```shell
docker-compose -f docker/dev-docker-compose.yaml up -d --build
```

### Миграция:
```shell
docker exec -it x-pictures-backend bash -c 'python manage.py migrate'
```

### Создать суперюзера:
```shell
docker exec -it x-pictures-backend bash -c 'python manage.py createsuperuser'
```

> `http://localhost:8800/api/admin/` - админка \
> `http://localhost:8800/api/schema/docs/` - свагер 