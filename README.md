django-api-practices
====================

Sample source code for my talk (title: "Django REST Framework におけるAPI実装プラクティス" in Japanese) at [PyConJP 2018](https://pycon.jp/2018/).

Requirements

* Python 3.7
* Django 2.1
* And others listed in requirements.txt

# How to run

## Using Docker compose

```console
$ docker-compose build
$ docker-compose up -d
$ docker-compose run backend python manage.py migrate
```

Other commands:

* bash: docker-compose exec backend /bin/bash
* logs: docker-compose logs -f backend
* mysql: docker-compose exec mysql /bin/bash and mysql -u root


## Setup databases using Docker and Run application on local machine

```sh
# django
export SECRET_KEY=secretkey

# database
export REDIS_PASSWORD=redispass
export MYSQL_PASSWORD=mysqlpass

# social
export SOCIAL_AUTH_GITHUB_KEY=key
export SOCIAL_AUTH_GITHUB_SECRET=secret
```

Running:

```console
$ docker-compose up -d mysql redis
$ pip -c requirements/constraints.txt install -r requirements/develop.txt
$ python src/manage.py migrate
$ python manage.py
```

# License

This software is released under the MIT License, see LICENSE.txt.

