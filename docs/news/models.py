from django.db import models

STATUS_CHOICES = {
    "d": "Draft",
    "p": "Published",
    "w": "Withdrawn",
}


class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title


class NewsPaper(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class RawIDFields(models.Model):
    newspaper = models.ManyToManyField(NewsPaper)
