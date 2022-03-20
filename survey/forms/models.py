from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

SA = "Short Answer"
LA = "Long Answer"
MC = "Multiple Choice"
F = "File"

question_types = (
    (SA, "Short Answer"),
    (LA, "Long Answer"),
    (MC, "Multiple Choice"),
    (F, "File"),
)

# User model - Inherits from AbstractUser
class User(AbstractUser):
    pass


class survey(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = RichTextField(max_length=1000)
    is_active = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        unique_together = ("created_by", "title")


class questions(models.Model):
    survey = models.ForeignKey(survey, on_delete=models.CASCADE)
    order = models.IntegerField()
    question_type = models.CharField(choices=question_types, max_length=20)
    description = models.CharField(max_length=1000)
    question_text = models.TextField(max_length=200)
    placeHolder = models.CharField(max_length=200, default="Enter your answer here")
    is_required = models.BooleanField(default=False)


class choices(models.Model):
    question = models.OneToOneField(
        questions, on_delete=models.CASCADE, related_name="choices"
    )
    choice_text = models.TextField(max_length=50)


class response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(survey, on_delete=models.CASCADE)
    question = models.ForeignKey(
        questions, on_delete=models.CASCADE, related_name="response"
    )

    class Meta:
        unique_together = ("user", "survey", "question")


class response_sa(models.Model):
    response_to = models.OneToOneField(
        response, on_delete=models.CASCADE, related_name="response_sa"
    )
    answer = models.CharField(max_length=200)


class response_la(models.Model):
    response_to = models.OneToOneField(
        response, on_delete=models.CASCADE, related_name="response_la"
    )
    answer = models.CharField(max_length=1000)

class response_mcq(models.Model):
    response_to = models.OneToOneField(
        response, on_delete=models.CASCADE, related_name="response_mcq"
    )
    answer = models.CharField(max_length=20)


class response_file(models.Model):
    response_to = models.OneToOneField(
        response, on_delete=models.CASCADE, related_name="response_file"
    )
    file = models.FileField(upload_to="uploads/")
