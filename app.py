from flask import Flask, render_template, request, redirect, url_for, session, make_response
import server, bcrypt

app = Flask(__name__)
app.secret_key = bcrypt.gensalt() #The secret key is needed to keep the client-side sessions secure


@app.route('/')
def index():  # display first site

    check_cookies() ##AM3 - cookies

    #####################AM3
    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = "!&*guest--"
        session['user_logged'] = "user_False"

    #########################AM3##
    sorted = request.args.get("sorted")
    order = request.args.get("order")

    # import answer and question from CSV file via function in server.py
    user_questions, user_answers = server.get_user_data()
    if order == "desc":
        # sorted - value for sorting; True / False for reverse
        user_questions = server.sorting(user_questions, sorted, True)
    if order == "asc":
        user_questions = server.sorting(user_questions, sorted, False)

    tags = server.get_all_tags()

    return render_template("index.html", questions=user_questions, answers=user_answers,
                           headers=server.Qheaders, tags=tags,user_name=user_name,user_state=session['user_logged'])  # send answer and question to index.html


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
    new_question[question_headers[0]] = server.get_id("questions", None)  # id
    new_question[question_headers[1]] = server.get_submission_time()  # submission time
    new_question[question_headers[2]] = 0  # viev number
    new_question[question_headers[3]] = "0"  # vote number
    print("Return from HTML:", new_question)
    server.add_new_question(new_question)  # send data [new_question] to python file
    server.add_new_question_user(session["user_name"],new_question[question_headers[0]]) #AM3 - save user and his question ID in DB
    return redirect(url_for("index"))


@app.route('/question_status/<question_id>_<view_add>')
def see_question(question_id, view_add):
    question_headers = server.Qheaders
    #print("question_id", question_id, "V", view_add)
    question = server.get_user_question(question_id)
    tags = server.get_tags_names(question_id)
    comments = server.get_comments(question_id)
    # if view_add=="True":
    #    question["view_number"] = server.add_view(question["view_number"])
    #    print("+1")
    # else:
    #    print("NIC")

    # NEED To BE UPDATE -> add view()
    # question["view_number"] = server.add_view(question["view_number"]) if (view_add == "True") else question[
    #   "view_number"]  # add view when user open site from main page(view_add=True)
    # server.edit_question(question)  # save new view number to CSV file
    print("Question:", question)
    print("View add:", view_add)
    answers_to_question = server.get_answers_to_question(question_id)
    #print("Answers:", answers_to_question)

    comment = request.args.get('comment')
    answer_id = request.args.get('answerID')
    if comment: #add only not empty comment
        server.add_comments(comment,question_id,answer_id,session["user_name"]) # AM3 - save user and his question ID in DB
        print("NEW COMMENT", comment,"for answer ID:",answer_id)

    comments = server.get_comments(question_id)

    return render_template("question_status.html", question=question, headers=question_headers,
                           answers=answers_to_question, tags=tags, comments=comments, user_state=session['user_logged'])


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
    server.add_new_answer_user(session["user_name"],new_answer["id"])  # AM3 - save user and his answer ID in DB
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
    tags = server.get_all_tags()
    tag_id = None
    for tag in tags:
        if new_tag["tags"] == tag["name"]:
            tag_id = tag["id"]
    tag_dict = {"question_id": question_id, "tag_id": tag_id}
    server.update_tag(tag_dict)
    return redirect(url_for("index"))


@app.route('/delete_answer/<question_id>/<answer_id>/<comment_id>')  # take data from HTML for REMOVE
def delete_comment(question_id,answer_id, comment_id):
    server.delete_comment(question_id,answer_id, comment_id)
    return redirect(url_for("see_question", question_id=question_id, view_add=False))


#########################AM3##

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        valid = server.check_user(email, password) #check given data with AskMate3_DB

        if valid:
            session['user_name'] = email
            session['user_logged'] = "user_True"
            return render_template("login.html", register="logged")
            #return redirect(url_for('index'))
        return render_template('login.html', register="login_bad")

    elif request.method == 'GET':
        return render_template("login.html", register="login")


@app.route('/logout')
def logout():
    session.pop('user_name')
    session.pop('user_logged')
    return redirect(url_for('index'))
   ###USUN  return cookie_insertion() ##AM3_cookies

###
@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if (len(password) < 3 ):
            return render_template("login.html", register="register_bad")

        if not server.is_user_in_db(email):
            server.add_new_user(email, password)
            return render_template("login.html", register="registered")
        print("There is such user")
        return render_template("login.html", register="is user")

    return render_template("login.html", register="register")


##AM3_cookies
@app.route('/set-cookie')
def cookie_insertion(): #podpiąć do logowania
    redirect_to_index = redirect('/')
    response = make_response(redirect_to_index)
    response.set_cookie('cookie-name', value='values', max_age=(10*24*60*60)) #utwórz cookie na 10 dni
#!!!!struktura cookies -> identyfikacja uzytkownika na podstawie szyfrowanego values porównanego z szyfrowanym values z BD
    print("Cookies has been created!")
    return response

def check_cookies(): #sprawdzanie czy użytkownik jest zalogowany - wywołane w index linia  11
    user_logged = request.cookies.get('cookie-name')
    print("Stan cookies: ", user_logged)
#
#    if user_logged:
#        session['user_name'] = email uzytkownika
#

@app.route('/del-cookie')
def cookie_delete(): # podpiąć do wylogowania
    redirect_to_index = redirect('/')
    response = make_response(redirect_to_index)
    response.set_cookie('cookie-name', value='!REMOVED!', expires=0)
    print("Cookies DELETED!")
    return response
#########################AM3##

if __name__ == '__main__':
    app.run()

