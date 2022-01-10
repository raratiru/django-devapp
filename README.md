# Django DevApp
Basic tools to manage a django application outside of a Django project

# Help
```
$ dev --help
Usage: dev [OPTIONS]

Options:
  -m       Make migrations  [default: makemigrations]
  -M       Migrate
  -s       Run Django shell
  -n TEXT  The name of the application or DEVAPP_NAME env variable.
           [required]
  --help   Show this message and exit.
```
# Example
```
$ tree
.
├── LICENSE
├── pyproject.toml
├── README.md
└── setup.cfg

$ export DEVAPP_NAME=app
$ dev -a

$ tree
.
├── db.sqlite3
├── LICENSE
├── pyproject.toml
├── app
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── README.md
└── setup.cfg
```
