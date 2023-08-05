# daner

[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)

## install

```bash
pip install daner
```

## example

### simple usage

```python
from daner import dong

# command
# python manage.py hi --name milisp
@dong()
async def hi(name: str):
	print(name)


# command
# python manage.py hi -u milisp
# alias u=username
@dong(alias={"u": "username"})
async def create(username: str):
	print(username)


# command
# python manage.py greet --name milisp
# if you want to run a sync function
@dong(sync=True)
def greet(name):
	print(name)
```

### create superuser

```python
# manage.py
# createsuperuser
# $ python manage.py createsuperuser -u username -e email
from daner import dong
import databases
import getpass
import ormar
import sqlalchemy
import uvicorn

DB_URI = "sqlite:///fast.db"
database = databases.Database(DB_URI)
engine = sqlalchemy.create_engine(DB_URI)
metadata = sqlalchemy.MetaData()
metadata.create_all(engine)


class User(ormar.Model):
	class Meta(ormar.ModelMeta):
		metadata = metadata
		database = database

    id = ormar.Integer(primary_key=True)
    username = ormar.String(max_length=60, unique=True)
    password = ormar.String(max_length=2048)
    email = ormar.String(max_length=80, nullable=True, unique=True)

@dong(alias={"u": "username", "e": "email"})
async def createsuperuser(username: str, email: str = None):
    await database.connect()
	password = getpass.getpass("password: ")
    password = "hashed" + password
    await User(
        username=username,
        password=password,
        email=email,
        is_superuser=True,
    ).save()
    await database.disconnect()

```
