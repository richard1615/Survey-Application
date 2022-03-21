# IRIS_Rec22_201CS129_Django

## Setup and run this project

- [Install git](https://git-scm.com/downloads)
- [Install Python](https://www.python.org/downloads/)
- Open git bash and clone this repo
- Type out these commands
```
    pip install django
    pip install django-ckeditor
    pip install xlwt
    cd IRIS_Rec22_201CS129_Django
    cd survey
    python manage.py runserver
```
- Open a web browser and go to http://127.0.0.1:8000/

## List of implemented features

- Users can register using a username, email and password
- Only authenticated users can access forms
- Users can create a form and add questions (short answer, long answer, multiple choice, file upload)
- The user gets the form URL which can be shared with other users
- The creator of the form can access all the responses in a table form
- Can edit or delete questions in a form and the form itself
- The form is rendered with input fields based on the questions set
- Appropriate messages are displayed if the form is not accepting responses or if the form doesn’t exist
- The form shouldn’t get submitted without filling in the required (compulsory) fields
- Configurations related to questions must be rendered (if defined)
- Add File Uploads as a type of response
- Store the files locally
- Save drafts of responses using Local Storage

## List of features to be implemented

- Placeholders and description for questions
- Once the form is filled by the user, display the user’s response
- Allow editing of form based on form configuration
- Mail a copy of the responses to the user
- Export the responses to Excel Spreadsheets or CSVs
- Use rich text editors like QuillJS, TinyMCE or Textbox.io for accepting long answer questions
- Display uploaded files

## List of known bugs
- Clicking the export as excel button gives an error
- Better server side validation of forms
- Use Django forms

## References Used

https://www.youtube.com/watch?v=ekyCxgtW3Js
https://moonbooks.org/Articles/How-to-create-a-list-of-items-from-a-string-in-a-Django-template-/#comment
https://www.w3schools.com/howto/howto_js_copy_clipboard.asp
https://stackoverflow.com/questions/6223149/django-post-checkbox-data
https://stackoverflow.com/questions/2712682/how-to-select-a-record-and-update-it-with-a-single-queryset-in-django
https://getbootstrap.com/docs/5.0/forms/validation/#browser-defaults
https://stackoverflow.com/questions/1131232/form-validation-in-django
https://getbootstrap.com/docs/4.1/content/tables/#striped-rows
https://stackoverflow.com/questions/4651172/reference-list-item-by-index-within-django-template
https://www.telerik.com/blogs/save-for-later-feature-in-forms-using-localstorage
https://github.com/pinax/django-mailer
https://stackoverflow.com/questions/57924398/how-to-export-excel-file-in-django
https://stackoverflow.com/questions/7188145/call-a-javascript-function-every-5-seconds-continuously
https://www.youtube.com/watch?v=mF5jzSXb1dc&t=182s
https://www.youtube.com/watch?v=rmVHOg7fj7E

