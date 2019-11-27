#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.db.models.fields import Field

from django.db.models import Lookup


class modEqual(Lookup):
    lookup_name = 'modEqual'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        print(lhs, lhs_params)
        print(rhs, rhs_params)
        return '%s mod %s = 0' % (lhs, rhs), params


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainproject.settings')
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

    Field.register_lookup(modEqual)
    print('registed')
    main()

