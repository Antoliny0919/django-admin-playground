from django.contrib import admin
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return True


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class QuestionAdmin07(Question):
    class Meta:
        proxy = True
        verbose_name = "question"


class QuestionAdmin08(Question):
    class Meta:
        proxy = True
        verbose_name = "question"


class QuestionAdmin10(Question):
    class Meta:
        proxy = True
        verbose_name = "question"


class QuestionAdmin11(Question):
    class Meta:
        proxy = True
        verbose_name = "question"


class QuestionAdmin12(Question):
    class Meta:
        proxy = True
        verbose_name = "question"


class QuestionAdmin13(Question):
    class Meta:
        proxy = True
        verbose_name = "question"

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        return True


class QuestionAdmin14(Question):
    class Meta:
        proxy = True
        verbose_name = "question"
