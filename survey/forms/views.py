from http.client import responses
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse ,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.mail import send_mail
from datetime import datetime
import xlwt

from .forms import surveyForm
from .models import (
    User,
    survey,
    questions,
    choices,
    response,
    response_sa,
    response_la,
    response_mcq,
    response_file
)

# Create your views here.


def index(request):

    # if user is logged in go to index page
    if request.user.is_authenticated:
        surveys = survey.objects.filter(created_by=request.user)
        return render(request, "forms/index.html", {"surveys": surveys})

    # if not go to login page
    else:
        return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "forms/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "forms/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "forms/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "forms/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "forms/register.html")


@login_required
def create_form(request):
    # create form object when method is post
    if request.method == "POST":
        #get data from the form
        user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        if 'is_active' in request.POST:
            is_active = True
        else:
            is_active = False
        if 'can_edit' in request.POST:
            can_edit = True
        else:
            can_edit = False
        if 'can_delete' in request.POST:
            can_delete = True
        else:
            can_delete = False

        #create and save form object
        try:
            survey_obj = survey(created_by = user, title = title, description = description, is_active = is_active, can_edit = can_edit, can_delete = can_delete)
            survey_obj.save()
        except IntegrityError:
            return render(
                request, "forms/create_form.html", {"message": "Please use another name"}
            )

        # go to the newly created form
        return HttpResponseRedirect(reverse("form_user", args=[title]))

    form = surveyForm()

    # render the create form page
    return render(request, "forms/create_form.html", {"form": form})


@login_required
def form_user(request, title):
    # get the form from the user and the title
    user = request.user
    try:
        form_obj = survey.objects.filter(created_by=user, title=title)[
            0
        ]  # returns a queryset with one value
    except IndexError:
        return render(request, "forms/message.html", {"message": "Form does not exist"})

    questions_obj = questions.objects.filter(survey=form_obj)

    # url for other users to access the form
    form_url = f"http://127.0.0.1:8000/form_response/{user.username}/{title}"
    return render(
        request,
        "forms/form_user.html",
        {"form_obj": form_obj, "questions_obj": questions_obj, "form_url": form_url},
    )


@login_required
def add_question(request, title):
    survey_obj = survey.objects.filter(created_by=request.user, title=title)[0]
    if request.method == "POST":
        # get data from the form
        question_text = request.POST["question_text"]
        question_type = request.POST["question_type"]
        if "is_required" in request.POST:
            is_required = True
        else:
            is_required = False
        # create and save question object
        question_obj = questions(
            survey=survey_obj,
            question_text=question_text,
            question_type=question_type,
            order=1,
            is_required=is_required,
        )
        question_obj.save()

        # if question type is multiple choice, create a choices object
        if question_type == "Multiple Choice":
            choices_list = request.POST["question_choices"]
            choices_obj = choices(question=question_obj, choice_text=choices_list)
            choices_obj.save()
        return HttpResponseRedirect(reverse("form_user", args=[title]))
    return render(request, "forms/add_question.html")


@login_required
def form_response(request, username, title):

    if request.method == "POST":
        submit_by = request.user
        user = User.objects.filter(username=username)[0]
        form_obj = survey.objects.filter(created_by=user, title=title)[0]
        questions_obj = questions.objects.filter(survey=form_obj)
        for question in questions_obj:
            response_obj = response.objects.create(
                    user=submit_by, survey=form_obj, question=question
                )
            if question.question_type == "Short Answer":
                answer = request.POST[f"question-{question.id}"]
                response_sa_obj = response_sa(response_to=response_obj, answer=answer)
                response_sa_obj.save()
            elif question.question_type == "Long Answer":
                answer = request.POST[f"question-{question.id}"]
                response_la_obj = response_la(response_to=response_obj, answer=answer)
                response_la_obj.save()
            elif question.question_type == "Multiple Choice":
                answer = request.POST[f"question-{question.id}"]
                response_mcq_obj = response_mcq(response_to=response_obj, answer=answer)
                response_mcq_obj.save()
            else:
                response_file_obj = response_file(response_to=response_obj, file=request.FILES[f"question-{question.id}"])
                response_file_obj.save()
        return render(
            request, "forms/message.html", {"message": "Form submitted successfully."}
        )

    # get the user from the username
    try:
        user = User.objects.filter(username=username)[0]
    except IndexError:
        return render(
            request,
            "forms/message.html",
            {"message": "The form you are trying to access does not exist."},
        )

    # if the user is the same as the user who created the form go to form_user
    if user == request.user:
        return HttpResponseRedirect(reverse("form_user", args=[title]))

    # get the form and questions from the database
    try:
        form_obj = survey.objects.filter(created_by=user, title=title)[0]
    except IndexError:
        # if the form does not exist show an error message
        return render(
            request,
            "forms/message.html",
            {"message": "The form you are trying to access does not exist."},
        )

    # if the form is not accepting response show error message
    if form_obj.is_active == False:
        return render(
            request,
            "forms/message.html",
            {"message": "This form is not currently accepting responses."},
        )

    if response.objects.filter(user=request.user, survey=form_obj):
        return render(
            request,
            "forms/message.html",
            {"message": "You have already submitted this form.",
            "can_edit": form_obj.can_edit,
            "can_delete": form_obj.can_delete,
            "username" : form_obj.created_by.username,
            "title" : form_obj.title
            }
        )

    questions_obj = questions.objects.filter(survey=form_obj)

    return render(request, "forms/form_response.html", {"questions_obj": questions_obj})


def edit_form(request, username, title):
    # get the user from the username
    try:
        user = User.objects.filter(username=username)[0]
        form_obj = survey.objects.filter(created_by=user, title=title)[0]
    except IndexError:
        return render(
            request, "forms/message.html", {"message": "There's something wrong"}
        )

    if request.method == "POST":
        form_obj.title = request.POST["title"]
        form_obj.description = request.POST["description"]
        if "is_active" in request.POST:
            form_obj.is_active = True
        else:
            form_obj.is_active = False
        if "can_edit" in request.POST:
            form_obj.can_edit = True
        else:
            form_obj.can_edit = False
        form_obj.save()
        return HttpResponseRedirect(reverse("form_user", args=[form_obj.title]))

    return render(request, "forms/create_form.html", {"form_obj": form_obj})


def edit_question(request, username, title, question_id):
    try:
        user = User.objects.filter(username=username)[0]
        question_obj = questions.objects.get(pk=question_id)
    except IndexError:
        return render(
            request, "forms/message.html", {"message": "There's something wrong"}
        )

    if request.method == "POST":
        question_obj.question_text = request.POST["question_text"]
        question_obj.question_type = request.POST["question_type"]
        if "is_required" in request.POST:
            question_obj.is_required = True
        else:
            question_obj.is_required = False
        question_obj.save()

        # if question type is multiple choice, create a choices object
        if question_obj.question_type == "Multiple Choice":
            question_obj.choices.choice_text = request.POST["question_choices"]
            question_obj.choices.save()
        return HttpResponseRedirect(reverse("form_user", args=[title]))

    return render(request, "forms/add_question.html", {"question_obj": question_obj})


def view_response(request, username, title):
    user = request.user
    try:
        form_obj = survey.objects.filter(created_by=user, title=title)[0]
    except IndexError:
        return render(
            request, "forms/message.html", {"message": "There's something wrong"}
        )
    questions_obj = questions.objects.filter(survey=form_obj)
    responses_obj = response.objects.filter(survey=form_obj)
    response_ls = [
        responses_obj.filter(question=q)
        for q in questions_obj
        if responses_obj.filter(question=q)
    ]
    return render(request, "forms/response.html", {"response_ls": response_ls, "title": form_obj.title})

def delete_form(request, title):
    user = request.user
    try:
        form_obj = survey.objects.filter(created_by=user, title=title)[0]
    except IndexError:
        return render(
            request, "forms/message.html", {"message": "This form does not exist"}
        )
    form_obj.delete()
    return HttpResponseRedirect(reverse("index"))

def delete_question(request, title, question_id):
    try:
        question_obj = questions.objects.get(pk=question_id)
    except IndexError:
        return render(
            request, "forms/message.html", {"message": "This question does not exist"}
        )
    question_obj.delete()
    return HttpResponseRedirect(reverse("form_user", args=[title]))

def edit_response(request, user, title):
    # gets the user and the form
    user = request.user
    try:
        created_by = User.objects.filter(username=user)[0]
        form_obj = survey.objects.filter(created_by=created_by, title=title)[0]
    except IndexError:
        return render(
            request, "forms/message.html", {"message": "There's something wrong"}
        )
    # gets the resposes
    response_obj = response.objects.filter(user=user, survey=form_obj)
    return render(request, "forms/edit_response.html", {"response_obj": response_obj})

def delete_response(request, username, title):
    user = request.user
    # gets the user and form
    try:
        created_by = User.objects.filter(username=username)[0]
        form_obj = survey.objects.filter(created_by=created_by, title=title)[0]
    except IndexError:
        return render(
            request, "forms/message.html", {"message": "There's something wrong"}
        )
    # gets the responses for each question
    response_obj = response.objects.filter(survey=form_obj)
    # deletes all the responses
    response_obj.delete()
    return HttpResponseRedirect(reverse("index"))

def export_excel(request, username, title):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="survey-response.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Survey Response')
    row_num = 0
    font_style = xlwt.XFStyle()

    columns = ['User', 'Question', 'Response']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    user = User.objects.filter(username=username)[0]
    form_obj = survey.objects.filter(created_by=user, title="Hello World")[0]
    response_obj = response.objects.filter(survey=form_obj)

    for single_response in response_obj:
        row_num += 1
        if response.question.question_type == "Multiple Choice":
            response_ls = [single_response.user.username, single_response.question.question_text, single_response.response_mcq.answer]
        elif response.question.question_type == "Short Answer":
            response_ls = [single_response.user.username, single_response.question.question_text, single_response.response_sa.answer]
        elif response.question.question_type == "Long Answer":
            response_ls = [single_response.user.username, single_response.question.question_text, single_response.response_la.answer]
        else:
            response_ls = [single_response.user.username, single_response.question.question_text, "file"]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, response_ls[col_num], font_style)

    wb.save(response)
    return response


# reference links
# https://www.youtube.com/watch?v=ekyCxgtW3Js
# https://moonbooks.org/Articles/How-to-create-a-list-of-items-from-a-string-in-a-Django-template-/#comment
# https://www.w3schools.com/howto/howto_js_copy_clipboard.asp
# https://stackoverflow.com/questions/6223149/django-post-checkbox-data
# https://stackoverflow.com/questions/2712682/how-to-select-a-record-and-update-it-with-a-single-queryset-in-django
# https://getbootstrap.com/docs/5.0/forms/validation/#browser-defaults
# https://stackoverflow.com/questions/1131232/form-validation-in-django
# https://getbootstrap.com/docs/4.1/content/tables/#striped-rows
# https://stackoverflow.com/questions/4651172/reference-list-item-by-index-within-django-template
# https://www.telerik.com/blogs/save-for-later-feature-in-forms-using-localstorage
# https://github.com/pinax/django-mailer
# https://stackoverflow.com/questions/57924398/how-to-export-excel-file-in-django
# https://stackoverflow.com/questions/7188145/call-a-javascript-function-every-5-seconds-continuously
# pip install django ckeditor
# https://www.youtube.com/watch?v=mF5jzSXb1dc&t=182s
# pip install xlwt
# https://www.youtube.com/watch?v=rmVHOg7fj7E