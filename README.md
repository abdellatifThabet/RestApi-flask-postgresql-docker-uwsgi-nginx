# Rest api template

This service was designed to be a model for rest api micro-service with relational db.

This service was implemented with the help of [flask](https://flask.palletsprojects.com/en/2.0.x/) framework and its
ecosystem:

* [flask-restx](https://flask-restx.readthedocs.io/en/latest/swagger.html) to auto-generate swagger definition from
  python code.
* [sqlalchemy](https://www.sqlalchemy.org/) ORM for the db connect, and it assists to compose sql queries.
* [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) to connect flask app with
* [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/) to auto-generate db migration file.

### Run the server

To run flask server you need docker and docker-compose in your machine, after running the below command try to access to
swagger UI via http://localhost:5000

```shell
make run
```
If you run the app the very first time you need to generate a db migration file

 
Note: it's recommended to stop all the running containers, sometime other services may take the same port number.

### Generate db migration file

To generate new migration file from the changes in `db_models` you need to run the below command line with a meaningful
message.

```shell
make db-migrate
```

[alembic](https://alembic.sqlalchemy.org/en/latest/) together
with [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/)
will auto-generate a migration file with the db changes, you will find it under `migrations/versions` prefixed with the
datetime of the generation.

