from django.db.models.query import QuerySet


class PersonQuerySet(QuerySet):
    def authors(self) -> 'PersonQuerySet':
        return self.filter(role='A')

    def admin_authors(self) -> 'PersonQuerySet':
        self.authors().filter(is_admin=True)
