from django.db import models


class Location(models.Model):
    url = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.url


class Bookmark(models.Model):
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)

    date_added = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)

    type = models.IntegerField(default=1)  # 1 - bookmark, 2 - directory
    location = models.ForeignKey(Location, null=True, blank=True)

    @staticmethod
    def recount_positions(parent=None):
        objects = Bookmark.objects.filter(parent=parent).order_by('position')
        k = 0
        for o in objects:
            o.position = k
            o.save()
            k += 1
        return k

    @staticmethod
    def get_last_position(parent=None):
        return Bookmark.recount_positions(parent)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.position is None:
            self.position = self.get_last_position(self.parent)

        super().save(force_insert=force_insert,
                     force_update=force_update,
                     using=using,
                     update_fields=update_fields
                     )

    def __str__(self):
        if self.title:
            return self.title

        if self.location:
            return self.location.url

        if self.description:
            return self.description

        return super().__str__()


class Param(models.Model):
    key = models.TextField(primary_key=True)
    value = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.key


class Page(models.Model):
    title = models.TextField(null=True, blank=True)
    type = models.TextField()

    def __str__(self):
        return self.title


class Tab(models.Model):
    title = models.TextField(null=True, blank=True)
    page = models.ForeignKey(Page)


class Pane(models.Model):
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE)

    width = models.IntegerField(default=100)
    height = models.IntegerField(default=100)

    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    tab = models.ForeignKey(Tab)
