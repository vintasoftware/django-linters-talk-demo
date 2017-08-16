from django.db import models


class PersonQuerySet(models.QuerySet):
    def authors(self) -> 'PersonQuerySet':
        return self.filter(role='A')

    def admin_authors(self) -> 'PersonQuerySet':
        self.authors().filter(is_admin=True)
