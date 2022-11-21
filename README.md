![Build Status](https://github.com/phisher13/django_rest_ecommerce/actions/workflows/django.yml/badge.svg?branch=master)

# Django Ecommerce 

### App stack:
- Python
- Django Rest Framework
- PostgreSQL
- Redis
- Elasticsearch


### Start App:
<p>in .env need to change DB_HOST (for docker-compose)</p>

```
DB_HOST=postgres
```

#### 1. Build docker container
```
docker-compose up -d --build 
```

#### 2. Enter http://localhost:8080
#### 3. Swagger: http://localhost:8080/swagger/
#### 4. For testing
```
make tests
```



