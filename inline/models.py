from django.db import models
from django.core.exceptions import  ValidationError


class Inline(models.Model):
    char = models.CharField(max_length=1000)
    fk = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.char

    def get_absolute_url(self):
        return "/inline/"


class LongInline(models.Model):
    char = models.CharField(max_length=128)
    text = models.TextField()
    integer = models.IntegerField()
    boolean = models.BooleanField()
    email = models.EmailField()
    decimal = models.DecimalField(max_digits=10, decimal_places=2)
    float = models.FloatField()
    fk = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.char


class FieldsetInline(models.Model):
    CHOICES = [
        ("one", "One"),
        ("two", "Two"),
        ("three", "Three"),
    ]
    not_required_file = models.FileField(null=True, blank=True)
    choice = models.CharField(choices=CHOICES, max_length=10)
    mtom = models.ManyToManyField("self", blank=True)
    datetime = models.DateTimeField()
    fk = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)


class CustomWidgetInline(models.Model):
    file = models.FileField()
    not_required_file = models.FileField(null=True, blank=True)
    url = models.URLField()
    time = models.TimeField()
    date = models.DateField()
    datetime = models.DateTimeField()
    fk = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)


class ManyToManyInline(models.Model):
    char = models.CharField(max_length=128)
    mtom1 = models.ManyToManyField("self", blank=True)
    mtom2 = models.ManyToManyField("self", blank=True)
    mtom3 = models.ManyToManyField("self", blank=True)
    fk = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)


class HelpTextInline(models.Model):
    char = models.CharField(max_length=128, help_text="char field help text..")
    boolean= models.BooleanField(help_text="boolean field help text..")
    integer = models.IntegerField(help_text="integer field help text..")
    float = models.FloatField(help_text="float field help text..")
    datetime = models.DateTimeField(help_text="datetime field help text..")
    fk = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)


class ErrorInline(models.Model):
    char = models.CharField(max_length=128)
    date = models.DateField()
    time = models.TimeField()
    fk = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        raise ValidationError("Non Field Errors")
