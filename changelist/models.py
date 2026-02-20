from django.db import models


class BaseModel(models.Model):
    char = models.CharField(max_length=128, help_text="char help text..")
    boolean = models.BooleanField(
        default=False,
        verbose_name=(
            "very long long long long long long long longlong long long verbose name."
        ),
    )
    integer = models.IntegerField(null=True, blank=True)
    file = models.FileField(null=True, blank=True, help_text="file help text..")
    url = models.URLField(null=True, blank=True, help_text="url help text..")
    date = models.DateField(auto_now_add=True)
    datetime = models.DateTimeField(help_text="datetime help text..")
    fk = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.char


class Pagination(BaseModel):
    pass


class ListFilter(BaseModel):
    pass


class AllLink(BaseModel):
    pass


class ColumnSort(BaseModel):
    pass


class DateHierarchy(BaseModel):
    pass


class ListEditAble(BaseModel):
    pass


class ReadOnly(BaseModel):
    pass


class Search(BaseModel):
    pass


class Action(BaseModel):
    pass


class FullFilter(BaseModel):
    pass


class ForOneToOneField(models.Model):
    char = models.CharField(max_length=128)

    def __str__(self):
        return self.char


class ForFk2Field(models.Model):
    char = models.CharField(max_length=128, verbose_name="for fk2 verbose name")


class ForFkField(models.Model):
    char = models.CharField(max_length=128, verbose_name="for fk verbose name")
    fk = models.ForeignKey(
        ForFk2Field,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


class ForManyToManyField(models.Model):
    char = models.CharField(max_length=128, verbose_name="for m2m verbose name")


class Related(models.Model):
    char = models.CharField(max_length=128)
    o2o = models.OneToOneField(
        ForOneToOneField,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    fk = models.ForeignKey(ForFkField, on_delete=models.CASCADE, null=True, blank=True)
    m2m = models.ManyToManyField(ForManyToManyField, blank=True)

    def __str__(self):
        return self.char


class VerboseName(models.Model):
    char = models.CharField(max_length=128, verbose_name="char verbose name")
    boolean = models.BooleanField(default=False, verbose_name="boolean verbose name")
    time = models.TimeField(auto_now=True)
    datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name="datetime verbose name",
    )

    class Meta:
        verbose_name = "very" + "long " * 40 + "verbose_name"
        verbose_name_plural = "changelist verbose name plural"
