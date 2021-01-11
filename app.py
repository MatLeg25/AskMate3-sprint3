from flask import Flask, render_template, request, redirect, url_for, session
import server, bcrypt

app = Flask(__name__)
app.secret_key = bcrypt.gensalt()


@app.route('/', methods=["POST", "GET"])
def index():  # display first site
    sorted = request.args.get("sorted")
    order = request.args.get("order")

    if 'user_name' in session:
        user = session['user_name']
        user_id = session['user_id']
    else:
        user = "default_user"
        user_id = "default_id"

    # import answer and question from CSV file via function in server.py
    user_questions, user_answers = server.get_user_data()
    if order == "desc":
        # sorted - value for sorting; True / False for reverse
        user_questions = server.sorting(user_questions, sorted, True)
    if order == "asc":
        user_questions = server.sorting(user_questions, sorted, False)

    tags = server.get_all_tags()

    question_to_search = request.args.get('search')
    if question_to_search:
        searched_questions = server.get_search_question(question_to_search)
        print(f"Searched question is {searched_questions}")
        return render_template("searched_question.html", questions=searched_questions,
                               question_to_search=question_to_search)

    return render_template("index.html", questions=user_questions, answers=user_answers,
                           headers=server.Qheaders, tags=tags, user=user,
                           user_id=user_id)  # send answer and question to index.html


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = server.hash_password(password)
        register_date = server.get_submission_time()
        if not server.is_user(email):
            server.add_user(email, hashed_password, register_date)
            return render_template("login.html", register="registered")
        print("There is such user")
        return render_template("login.html", register="is user")

    return render_template("login.html", register="register")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if server.is_user(email) != []:
            is_valid_password = server.is_password_valid(email, password)
            if is_valid_password:
                session['user_name'] = email
                session['user_id'] = server.get_user_id(email)
                return render_template("login.html", register="logged", user=session['user_name'])
            else:
                return render_template("login.html", register="wrong_data")
        return render_template("login.html", register="no_user")

    return render_template("login.html", register="login")


@app.route('/logout')
def logout():
    session.pop('user_name')
    session.pop('user_id')
    return redirect(url_for('index'))


# Qheaders: id,submission_time,view_number,vote_number,title,message,image

@app.route('/add_question')
def add_question():  # display site add question
    question_headers = server.Qheaders  # import headers from server.py
    question = server.get_default_question()  # import base dictionary to template for HTML
    print("Input to HTML", question)
    return render_template("add_question.html", question=question, headers=question_headers,
                           option="Add_question")  # send to html


@app.route('/add_question', methods=["POST"])  # take data from HTML
def add_new_question():
    new_question = dict(request.form)  # take data from HTML
    question_headers = server.Qheaders
    ##############dorobic przypisanie poniższych wartosci przez funkcje
    # new_question[question_headers[0]] = server.get_id("questions", None)  # id
    new_question[question_headers[1]] = server.get_submission_time()  # submission time
    new_question[question_headers[2]] = 0  # viev number
    new_question[question_headers[3]] = 0  # vote number
    print("Return from HTML:", new_question)
    server.add_new_question(new_question)  # send data [new_question] to python file
    last_id = server.get_last_question_id()
    user_id = session['user_id']
    server.update_user_question_table(user_id, last_id)
    return redirect(url_for("index"))


@app.route('/question_status/<question_id>_<view_add>')
def see_question(question_id, view_add):
    answer_status = server.get_answer_status(question_id)
    question_headers = server.Qheaders
    print("question_id", question_id, "V", view_add)
    question = server.get_user_question(question_id)
    tags = server.get_tags_names(question_id)

    # add view when user open site from main page(view_add=True)
    if view_add=="True":
        server.add_view(question["id"])
        print("View +1 for question ",question["id"])

    print("Question:", question)
    print("View add:", view_add)
    answers_to_question = server.get_answers_to_question(question_id)
    print("Answers:", answers_to_question)

    comment = request.args.get('comment')
    answer_id = request.args.get('answerID')

    # add coment if not empty and len more than 1
    if comment and len(comment) > 1:
        server.add_comments(comment, question_id, answer_id)
        last_id = server.get_last_comment_id()
        user_id = session['user_id']
        server.update_user_comment_table(user_id, last_id, question_id)
        print("NEW COMMENT", comment, "ID:", answer_id)

    authors = server.get_authors(question_id)  # AM3-get authors of [question,answers,comments]
    comments = server.get_comments(question_id)  # do after possibility of adding new comment (GET form)

    if 'user_name' in session:
        user = session['user_name']
    else:
        user = "default_user"

    return render_template("question_status.html", question=question, headers=question_headers,
                           answers=answers_to_question, tags=tags, comments=comments, user=user, authors=authors,
                           answer_status=answer_status)


@app.route('/question_status/<question_id>/new_answer')
def add_answer(question_id):
    answer_headers = server.Aheaders
    question = server.get_user_question(question_id)
    answer = server.get_default_answer()
    answer[answer_headers[0]] = server.get_id("answers", question_id)  # id
    answer[answer_headers[1]] = server.get_submission_time()  # submission time
    answer[answer_headers[2]] = "0"  # vote number
    answer[answer_headers[3]] = question_id
    return render_template("add_question.html", answer=answer, headers=answer_headers, option="Add_answer")


@app.route('/question_status/', methods=["POST"])  # take data from HTML
def add_new_answer():
    new_answer = dict(request.form)  # take data from HTML
    print("Return from HTML:", new_answer)
    server.add_new_answer_to_file(new_answer)  # send data [new_question] to python file
    id_of_question = new_answer["question_id"]
    last_id = server.get_last_answer_id()
    user_id = session['user_id']
    server.update_user_answer_table(user_id, last_id, id_of_question)
    return redirect(url_for("see_question", question_id=id_of_question, view_add=False))


# DELETE FUNCTION start in question_status.html
@app.route(
    '/question_status/delete/<question_id>')  # connect with page designed to remove the question (path to open render_template=>html)
def delete_question_start(question_id):
    question_headers = server.Qheaders
    question = server.get_user_question(question_id)
    return render_template("delete_question.html", question=question, headers=question_headers,
                           question_id=question_id)  # send to html


@app.route('/<question_id>')  # take data from HTML for REMOVE
def delete_question_end(question_id):
    server.delete_question(question_id)  # send data [del_question_id] to python file
    return index()


@app.route('/edit_question/<question_id>')
def edit_question_start(question_id):  # display site add question
    question_headers = server.Qheaders  # import headers from server.py
    question = server.get_question_to_edit(question_id)  # question as dictionary
    print("Input to HTML ->Question to edit", question)
    return render_template("add_question.html", question=question, headers=question_headers,
                           option="Edit_question")  # send to html


@app.route('/edit_question', methods=["POST"])  # take data from HTML
def edit_question_end():
    edited_question = dict(request.form)  # take data from HTML
    print("Return from HTML -> edited question:", edited_question)
    server.edit_question(edited_question)  # send data [new_question] to python file
    return index()


@app.route('/edit_answer/<answer_id>/<question_id>')
def edit_answer_start(answer_id, question_id):  # display site add question
    answer_headers = server.Aheaders  # import headers from server.py
    answer = server.get_answer_to_edit(answer_id, question_id)  # question as dictionary
    print("Input to HTML ->Answer to edit", answer)
    return render_template("add_question.html", answer=answer, headers=answer_headers,
                           option="Edit_answer")  # send to html


@app.route('/edit_answer', methods=["POST"])  # take data from HTML
def edit_answer_end():
    edited_answer = dict(request.form)  # take data from HTML
    print("Return from HTML -> edited answer:", edited_answer)
    server.edit_answer(edited_answer)  # send data [new_question] to python file
    return redirect(url_for("see_question", question_id=edited_answer["question_id"], view_add=False))


# DELETE FUNCTION start in question_status.html
# connect with page designed to remove the question (path to open render_template=>html)
@app.route('/question_status/delete_answer/<answer_id>/<question_id>')
def delete_answer_start(answer_id, question_id):
    answer_headers = server.Aheaders
    answer = server.get_user_answer(answer_id, question_id=question_id)
    return render_template("delete_answer.html", answer=answer, headers=answer_headers,
                           answer_id=answer_id)  # send to html


@app.route('/delete_answer/<answer_id>/<question_id>')  # take data from HTML for REMOVE
def delete_answer_end(answer_id, question_id):
    server.delete_answer(answer_id, question_id)
    return redirect(url_for("see_question", question_id=question_id, view_add=False))


@app.route('/question_status/add_tag/<question_id>')
def add_new_tag_start(question_id):
    tags = server.get_tag_labels()
    print(tags)
    return render_template("add_tag.html", question_id=question_id, tags=tags)


@app.route('/question_status/add_tag/<question_id>', methods=["POST"])
def add_new_tag_end(question_id):
    new_tag = dict(request.form)
    tags = server.get_question_tags(question_id)
    tag_labels_ids = server.get_tag_labels()
    tags_in_question = []
    tag_id = None
    for tag in tags:                                    #Making list with tags existing in question
        tags_in_question.append(tag["name"])
    for tag_label_id in tag_labels_ids:                 #Assigning tag_id for added tag by comparing tag names in DB
        if new_tag["tags"] == tag_label_id["name"]:
            tag_id = tag_label_id["id"]
    if tags is None or new_tag["tags"] not in tags_in_question:
        #Updating tags if there is no tag for question or of chosen tag isn't in list with tags for question yet
        tag_dict = {"question_id": question_id, "tag_id": tag_id}
        server.update_tag(tag_dict)

    return redirect(url_for("index"))


@app.route('/delete_answer/<question_id>/<answer_id>/<comment_id>')  # take data from HTML for REMOVE
def delete_comment(question_id, answer_id, comment_id):
    server.delete_comment(question_id, answer_id, comment_id)
    return redirect(url_for("see_question", question_id=question_id, view_add=False))


@app.route('/users')
def list_users():
    users_data = server.get_user_information()
    user_questions = server.get_users_question_amount()
    user_answers = server.get_users_answer_amount()
    user_comments = server.get_users_comment_amount()
    print(users_data)
    print(user_questions)
    print(user_answers)
    print(user_comments)
    return render_template("user_list.html", users_data=users_data, user_questions=user_questions,
                           user_answers=user_answers, user_comments=user_comments)


@app.route('/user/<user_id>')
def user_page(user_id):
    users_data = server.get_user_information()
    users_questions_amount = server.get_users_question_amount()
    users_answers_amount = server.get_users_answer_amount()
    users_comments_amount = server.get_users_comment_amount()
    # making variables with data for ONE user from variables with data for ALL users
    for i in range(len(users_data)):
        if users_data[i]["id"] == int(user_id):
            user_data = users_data[i]
            user_questions_amount = users_questions_amount[i]
            user_answers_amount = users_answers_amount[i]
            user_comments_amount = users_comments_amount[i]

            user_questions = server.get_questions_for_user(user_id)
            user_answers = server.get_answers_for_user(user_id)
            user_comments = server.get_comments_for_user(user_id)

            return render_template("user_page.html", user_data=user_data, user_question_amount=user_questions_amount,
                                   user_answer_amount=user_answers_amount, user_comment_amount=user_comments_amount,
                                   user_questions=user_questions, user_answers=user_answers,
                                   user_comments=user_comments)
    return


@app.route('/question_status/set_answer_status/<question_id>/<answer_id>/<answer_status>')
def set_answer_status(question_id, answer_id, answer_status):
    server.update_answer_status(question_id, answer_id, answer_status)
    return redirect(url_for("see_question", question_id=question_id, view_add=False))


@app.route('/question_status/answer_vote/<question_id>/<answer_id>/<answer_vote>')
def answer_vote(question_id,answer_id,answer_vote):
    server.update_user_reputation_by_answer(answer_id,answer_vote)
    server.update_answer_vote(answer_vote,answer_id)
    return redirect(url_for("see_question", question_id=question_id, view_add=False))


@app.route('/question_status/question_vote/<question_id>/<question_vote>')
def question_vote(question_id, question_vote):
    server.update_user_reputation_by_question(question_id,question_vote)
    server.update_question_vote(question_vote,question_id)
    return redirect(url_for("see_question", question_id=question_id, view_add=False))


@app.route('/index/display_by_tag/<tag_name>')
def display_by_tag(tag_name):
    print("DISPLAY by tag: ",tag_name)
    questions_by_tag=server.get_questions_by_tag(tag_name)

    user_questions, user_answers = server.get_user_data()

    return render_template("index_by_tag.html", questions=questions_by_tag, answers=user_answers,
                           headers=server.Qheaders, tag=tag_name)

if __name__ == '__main__':
    app.run()
