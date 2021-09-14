# AskMate (sprint 3)


## This is a forum where users can ask questions and answer them - similar to StackOverflow.


## Implemented:

1. The user have the possibility to register a new account into the system.
    - There is a `/registration` page
    - The page is linked from the front page
    - Theres is a form on the `/registration` page when a request is issued with `GET` method
    - The form ask for username (email address), password and issues a `POST` request to `/registration` on submit
    - After submitting you are redirected back to the main page and the new user account is saved in the database
    - For a user account we store the email as username a password hash and the date of the registration

2. The registered user, is able to login to the system with previously saved username and password.
    - There is a `/login` page
    - The page is linked from the front page
    - Theres is a form on the `/login` page when a request is issued with `GET` method
    - The form ask for username (email address), password and issues a `POST` request to `/login` on submit
    - After submitting you are redirected back to the main page and the given user is logged in
    - It is only possible to ask or answer a question if the user is logged in

3. There is a page where I can list all the registered users with all their attributes.
    - There is a `/users` page
    - The page is linked from the front page when I'm logged in
    - The page is not accessible when I'm not logged in
    - Theres is a `<table>` with user data in it. The table should have these details of a user:
  - User name (link to user page if implemented)
  - Registration date
  - Count of asked questions (if binding implemented)
  - Count of answers (if binding implemented)
  - Count of comments (if binding implemented)
  - Reputation (if implemented)

4. As a user when I add a new question I would like to be saved as the user who creates the new question.
    - The user id of the currently logged in user is saved when a new question is saved

5. As a user when I add a new answer I would like to be saved as the user who creates the new answer.
    - The user id of the currently logged in user is saved when a new answer is saved

6. As a user when I add a new comment I would like to be saved as the user who creates the new comment.
    - The user id of the currently logged in user is saved when a new comment is saved

7. There should be a page where we can see all details and activities of a user.
    - There is a `/user/<user_id>` page
    - The user page of a logged in user is linked from the front page
    - The page of every user is linked from the users list page
    - Theres is a list with these deatils about the user:
  - User id
  - User name (link to user page if implemented)
  - Registration date
  - Count of asked questions (if binding implemented)
  - Count of answers (if binding implemented)
  - Count of comments (if binding implemented)
  - Reputation (if implemented)
    - There is a separate table where every **question** is listed that the user created. The related question is linked in every line.
    - There is a separate table where every **answer** is listed that the user created. The related question is linked in every line.
    - There is a separate table where every **comment** is listed that the user created. The related question is linked in every line.

8. As a user I would like to have the possibility to mark an answer as accepted.
    - On a question's page for every answer there is a clickable element that can be used to mark an answer as accepted
    - When there is an accepted answer there is an option to remove the accepted state
    - Only the user who asked the question can change the accepted state of answers
    - An accpted answer has a visual distinction from other answers

9. As a user I would like to see a reputation system to strengthen the community. Reputation is a rough measurement
 of how much the community trusts a user.
    - **A user gains reputation when:**
- her/his question is voted up: +5
- her/his answer is voted up: +10
- her/his answer is marked "accepted": +15

10. As a user I would like to see a small drop in reputation when a user's question or answer is voted down.
    - **A user loses reputation when:**
- her/his question is voted down: −2
- her/his answer is voted down: −2

11. There should be a page where I can list all the existing tags and that how many questions are marked with the given tags
    - There is a `/tags` page
    - The page is linked from the front page and a question's page
    - The page is accessible when I'm not logged in



## Home page:
![askmate1](https://user-images.githubusercontent.com/70913892/133313473-0a91bb68-8ef4-4032-9665-9ef90a3b8c20.PNG)

## Question page:
![askmate2](https://user-images.githubusercontent.com/70913892/133313491-23e53be3-e1b4-498c-866c-6c17148c32b1.png)



## Technologies:
- Flask
- PostgreSQL
- Jinja2
- Bootstrap

