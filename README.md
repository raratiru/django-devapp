# Django DevApp
Basic tools to manage a django application outside of a Django project

# Help
```
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
$ export DEVAPP_NAME=app
$ dev -s
>>> 
```
