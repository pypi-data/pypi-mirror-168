#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


# import project path to `PYTHONPATH` so that can be found by the Django project,
# but NOT the path of `drf_admin` package!
#
# Ref:
#   - https://stackoverflow.com/questions/3108285/in-python-script-how-do-i-set-pythonpath/3108301

project_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.path.index(project_path)
except ValueError:
    sys.path.append(project_path)


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

