from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_form", views.create_form, name="create_form"),
    path("form_user/<str:title>", views.form_user, name="form_user"),
    path("add_question/<str:title>", views.add_question, name="add_question"),
    path("form_response/<str:username>/<str:title>", views.form_response, name="form_response"),
    path("edit_form/<str:username>/<str:title>", views.edit_form, name="edit_form"),
    path("edit_question/<str:username>/<str:title>/<int:question_id>", views.edit_question, name="edit_question"),
    path("view_response/<str:username>/<str:title>", views.view_response, name="view_response"),
    path("delete_question/<str:title>/<int:question_id>", views.delete_question, name="delete_question"),
    path("delete_form/<str:title>", views.delete_form, name="delete_form"),
    path("delete_response/<str:username>/<str:title>", views.delete_response, name="delete_response"),
    path("export_excel/<str:username>/<str:title>", views.export_excel, name="export_excel")
]