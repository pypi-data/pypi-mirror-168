
# Django Perm Filter
A simple app that can be included in Django projects which hides app specific permissions from any type of User.  Easily add entire apps, specific permissions or models and it will take care of the rest.  Non-destructive (Does **not** delete permissions).

For example, typically we have **no reason**, in any Django project, to expose the following permissions for Users or Groups:

| App          | Model        | Permission                              |
|--------------|--------------|-----------------------------------------|
| admin        | log entry    | Can view/add/change/delete log entry    |
| auth         | permission   | Can view/add/change/delete permission   |
| contenttypes | content type | Can view/add/change/delete content type |
| sessions     | session      | Can view/add/change/delete session      |


## Features
- Hide all permissions for an App
- Hide permissions using app and codename (more granular)
- Hide models from the Django Admin

## Requirements
Django 3 or 4
Python 3

## Quickstart

Install Django Perm Filter::

```bash
pip install django-perm-filter
```

Add it to your `INSTALLED_APPS` at the bottom:

```python
INSTALLED_APPS = (
    ...
    'django_perm_filter',
)
```

In your `settings.py` add a entry for `PERM_FILTER`:
```
PERM_FILTER = {
    "HIDE_PERMS": [
        # Use app name only to hide all app related permissions
        "admin",
        "contenttypes",
        "sessions",
        "sites",
        # Use app.codename to get more granular
        "auth.view_permission",
        "auth.add_permission",
        "auth.change_permission",
        "auth.delete_permission",
    ],
    "UNREGISTER_MODELS": [
        "django.contrib.sites.models.Site",
    ],
}
```

## Optional
By default `django_perm_filter` will register a new `UserAdmin` and `GroupAdmin` which extend `django.contrib.auth.admin.UserAdmin` and `django.contrib.auth.admin.GroupAdmin` that simply adds permissions filtering.  If you would like it to extend your own custom `UserAdmin` or `GroupAdmin` classes, then set the class path in the `PERM_FILTER` settings.

```
PERM_FILTER = {
  ...
  "USER_ADMIN": "myapp.user.admin.UserAdmin",
  "GROUP_ADMIN": "myapp.user.admin.GroupAdmin",
}

```

## Development
Assumes you have `pyenv` and `make` installed (you should!).
```
make scratch
```


## Running Tests

Does the code actually work?

```bash
source <YOURVIRTUALENV>/bin/activate
(myenv) $ pip install tox
(myenv) $ tox
```

## Development commands

```bash
pip install -r requirements_dev.txt
invoke -l
```
