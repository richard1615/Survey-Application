# Survey Application

#### A django web application to create and fill forms for the purpose of surveys and quizzes

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
