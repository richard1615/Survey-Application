from dataclasses import fields
import imp
from turtle import title
from django.forms import ModelForm

from .models import survey


class surveyForm(ModelForm):
    class Meta:
        model = survey
        fields = ['title', 'description', 'is_active', 'can_edit', 'can_delete']
        labels = {
        "title": "Title",
        "description": "Description",
        "is_active": "Is the form currently accepting responses?",
        "can_edit": "Can the user edit their response?",
        "can_delete": "Can the user delete their response?",
    }
