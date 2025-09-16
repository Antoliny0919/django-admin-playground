from django.core.exceptions import ValidationError
from django.db import models


class BaseModel(models.Model):
    CHOICES = [
        ("one", "One"),
        ("two", "Two"),
        (
            "three",
            "very " + "long " * 20 + "choice",
        ),
    ]
    char = models.CharField(max_length=1000)
    text = models.TextField(max_length=128, null=True, blank=True)
    choice = models.CharField(choices=CHOICES, max_length=128, null=True, blank=True)
    slug = models.SlugField(max_length=128, null=True, blank=True)
    integer = models.IntegerField(null=True, blank=True)
    boolean = models.BooleanField(default=False)
    datetime = models.DateTimeField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    fk = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.char


class Common(BaseModel):
    pass


class Prepopulated(BaseModel):
    pass


class ReadOnly(BaseModel):
    pass


class VerboseName(BaseModel):
    class Meta:
        verbose_name = "Verbose Name"
        verbose_name_plural = "Verbose Name Plural"


class HelpText(BaseModel):
    pass


class CustomWidget(models.Model):
    char = models.CharField(max_length=128)
    file = models.FileField()
    not_required_file = models.FileField(null=True, blank=True)
    url = models.URLField()
    time = models.TimeField()
    date = models.DateField()
    datetime = models.DateTimeField()

    def __str__(self):
        return self.char


class Fieldset(models.Model):
    CHOICES = [
        ("one", "One"),
        ("two", "Two"),
        ("three", "Three"),
    ]
    char = models.CharField(max_length=128)
    choice = models.CharField(choices=CHOICES, max_length=10)
    not_required_file = models.FileField(null=True, blank=True)
    datetime = models.DateTimeField()
    m2m = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.char


class Related(models.Model):
    char = models.CharField(max_length=128)
    fk = models.ForeignKey(
        Common,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fk_common",
    )
    m2m = models.ManyToManyField(Common, blank=True, related_name="mtm_common")
    o2o = models.OneToOneField(Common, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.char


class RawID(Related):
    pass


class AutoComplete(Related):
    pass


class AllManyToMany(models.Model):
    char = models.CharField(max_length=128)
    m2m_1 = models.ManyToManyField(Common, blank=True, related_name="mtm1")
    m2m_2 = models.ManyToManyField(Common, blank=True, related_name="mtm2")
    m2m_3 = models.ManyToManyField(Common, blank=True, related_name="mtm3")

    class Meta:
        verbose_name = "All ManyToMany"


class FieldError(models.Model):
    char = models.CharField(max_length=128)
    datetime = models.DateTimeField()

    def __str__(self):
        return self.char

    def clean(self):
        raise ValidationError("Non Field Errors")
