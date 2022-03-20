from django.contrib import admin
from forms.models import User, survey, questions, choices, response, response_sa, response_la, response_mcq, response_file

# Register your models here.
admin.site.register(User)
admin.site.register(survey)
admin.site.register(questions)
admin.site.register(choices)
admin.site.register(response)
admin.site.register(response_sa)
admin.site.register(response_la)
admin.site.register(response_mcq)
admin.site.register(response_file)
