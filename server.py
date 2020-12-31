import csv, data_manager
from datetime import datetime
import bcrypt

QUESTION_LABEL_FOR_ID = "id"
QUESTION_LABEL_FOR_ANSWERS = "question_id"
ANSWER_LABEL_FOR_ID = "id"


# AM2 - updated to SQL
def get_user_data():
    # OLD based on CSV files - to be removed
    # with open("./sample_data/testowe.csv") as quest:
    #    questions = []
    #    for line in csv.DictReader(quest):
    #        questions.append(line)

    # with open("./sample_data/testowe_odpowiedzi.csv") as answ:
    #    answers = []
    #    for line in csv.DictReader(answ):
    #        answers.append(line)

    # NEW based od SQL database
    questions_from_SQL = data_manager.get_questions()
    # print("Imported questions from SQL database=>", questions_from_SQL)

    answers_from_SQL = data_manager.get_answers()
    # print("Imported answers from SQL database=>", answers_from_SQL)

    return questions_from_SQL, answers_from_SQL


def export_data(questions, fieldnames, filename='./sample_data/testowe.csv', mode='w'):
    if mode in ["a", "w"]:
        with open(filename, mode) as file:
            print(questions)
            csv_writer = csv.DictWriter(file, fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(questions)
    else:
        raise ValueError("Wrong write mode")


# QUESTIONS, ANSWERS = get_user_data()  # no reccomended, nie aktualizuje na bieżąco zmiany w plikach i danych
Qheaders = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image", "tag"]  # QUESTIONS[0]
Aheaders = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


# AM2 - updated to SQL
def get_user_question(story_id):
    questions, answers = get_user_data()
    for question in questions:
        print(question)
        if int(story_id) == question["id"]:
            return question
    return None


# AM2 - updated to SQL - nie sprawdzone czy działa
def get_user_answer(answer_id, question_id):
    questions, answers = get_user_data()
    for answer in answers:
        if int(answer_id) == answer["id"] and answer["question_id"] == int(question_id):
            return answer
    return None


def get_submission_time():
    return datetime.today().strftime('%Y-%m-%d %H:%M:%S')


def get_default_question():
    return {"id": None, "submission_time": "00-00-00", "view_number": 0, "vote_number": 0, "title": "title",
            "message": "message", "image": None, "tag": None}


def get_default_answer():
    return {"id": None, "submission_time": "00-00-00", "vote_number": 0, "question_id": 0, "message": "message",
            "image": None}


# AM2 - updated to SQL
def add_new_question(question):
    questions, answers = get_user_data()
    questions.append(question)  # zwraca wartości, .keys() zwraca klucze
    print(questions)
    # export_data(questions, fieldnames=Qheaders)  # zapis do pliku CSV

    data_manager.add_question(question)


# AM2 -SQL UPDATED
def add_new_answer_to_file(answer):
    questions, answers = get_user_data()
    answers.append(answer)
    print("Added answer: ", answer)
    # export_data(answers, fieldnames=Aheaders, filename='./sample_data/testowe_odpowiedzi.csv')
    data_manager.add_answer(answer)


# AM2 - updated to SQL
def get_answers_to_question(question_id):
    questions, answers = get_user_data()
    list_of_answers = []
    for answer in answers:
        if answer[QUESTION_LABEL_FOR_ANSWERS] == int(question_id):
            list_of_answers.append(answer)
    return list_of_answers


# AM2 -SQL UPDATED
def delete_question(question_id):
    questions, answers = get_user_data()
    list_of_questions = []
    for question in questions:
        if not question[QUESTION_LABEL_FOR_ID] == question_id:
            list_of_questions.append(question)
    # export_data(list_of_questions, fieldnames=Qheaders)  # zapis do pliku
    data_manager.delete_question(question_id)

    # delete answers to deleted question
    list_of_answers = []
    for answer in answers:
        if not answer[QUESTION_LABEL_FOR_ANSWERS] == question_id:
            list_of_answers.append(answer)
    # export_data(list_of_answers, fieldnames=Aheaders, filename='./sample_data/testowe_odpowiedzi.csv')


# AM2 - updated to SQL
def get_question_to_edit(question_id):
    questions, answers = get_user_data()
    for question in questions:
        if question[QUESTION_LABEL_FOR_ID] == int(question_id):
            edit_question = question
    return {"id": edit_question["id"], "submission_time": edit_question["submission_time"],
            "view_number": edit_question["view_number"], "vote_number": edit_question["vote_number"],
            "title": edit_question["title"], "message": edit_question["message"]}


# AM2 - updated to SQL
def edit_question(edited_question):
    questions, answers = get_user_data()
    list_of_questions = []
    print("EDIT FUNCTION_END")
    for question in questions:
        if question[QUESTION_LABEL_FOR_ID] == int(edited_question[Qheaders[0]]):
            print("Question edit:\n\t", question, "\n\tVS\n\t", edited_question)
            question = edited_question  # replaces question for edited question
        list_of_questions.append(question)
    # print("BEFORE\n", questions)
    # print("AFTER\n",list_of_questions)
    # export_data(list_of_questions, fieldnames=Qheaders)  # zapis do pliku
    data_manager.update_question(edited_question)


def get_id(type_of_data, question_id):
    questions, answers = get_user_data()
    if type_of_data == "questions":
        return int(questions[len(questions) - 1][QUESTION_LABEL_FOR_ID]) + 1
    if type_of_data == "answers":
        answers = get_answers_to_question(question_id)
        if answers != []:
            return int(answers[len(answers) - 1][ANSWER_LABEL_FOR_ID]) + 1
        else:
            return 1


# AM2 -SQL UPDATED
def sorting(questions, value, order):
    # print("VALUE:",questions[1][value],"type:",type(questions[1][value]))
    return sorted(questions, key=lambda question: (question[value]),
                  reverse=order)  # convert value to str -> in SQL some type are defined as int


# AM2 -SQL UPDATED
def get_answer_to_edit(answer_id, question_id):
    questions, answers = get_user_data()
    for answer in answers:
        if (answer[QUESTION_LABEL_FOR_ID] == int(answer_id) and answer[
            "question_id"] == int(question_id)):  # edit answer with def ID only for selected question
            edit_answer = answer
    return {"id": edit_answer["id"], "submission_time": edit_answer["submission_time"],
            "vote_number": edit_answer["vote_number"], "question_id": edit_answer["question_id"],
            "message": edit_answer["message"], "image": edit_answer["image"]}


# AM2 -SQL UPDATED
def edit_answer(edited_answer):
    questions, answers = get_user_data()
    list_of_answers = []
    print("EDIT answer FUNCTION_END")
    for answer in answers:
        if (answer[ANSWER_LABEL_FOR_ID] == edited_answer[Aheaders[0]] and int(answer["question_id"]) == int(
                edited_answer[
                    "question_id"])):
            print(answer, "VS\n", edited_answer)
            answer = edited_answer  # replaces answer to edited answer
        list_of_answers.append(answer)
    # export_data(list_of_answers, fieldnames=Aheaders, filename='./sample_data/testowe_odpowiedzi.csv')
    data_manager.update_answer(edited_answer)


# AM2 -SQL UPDATED
def delete_answer(answer_id, question_id):
    questions, answers = get_user_data()
    list_of_answers = []
    for answer in answers:
        if not (answer[ANSWER_LABEL_FOR_ID] == int(answer_id) and answer["question_id"] == int(question_id)):
            list_of_answers.append(answer)
    # export_data(list_of_answers, fieldnames=Aheaders, filename='./sample_data/testowe_odpowiedzi.csv')
    data_manager.delete_answer(answer_id)


def add_view(view):
    return int(view) + 1


# AM2 - updated to SQL
def get_all_tags():
    return data_manager.get_tags()


def get_tag_labels():
    return data_manager.get_tag_labels()


def get_tags_names(question_id):
    all_tags = data_manager.get_tags()
    for tag in all_tags:
        if int(question_id) == tag["question_id"]:
            return tag["name"]
    return None

def update_tag(tag):
    data_manager.update_tags(tag)


def add_comments(comment,question_id,answer_id):  # to be updated for user data
    new_comment = [(question_id), (answer_id), comment, get_submission_time()]
    #print("NOWYY komentarz",new_comment)
    data_manager.add_comment(new_comment)


def get_comments(question_id):
    all_comments = data_manager.get_comments()
    comments_for_question = []
    for comment in all_comments:
        if int(question_id) == comment["question_id"]:
            comments_for_question.append(comment)
    return comments_for_question

def delete_comment(question_id,answer_id, comment_id):
    data_manager.delete_comment(comment_id)
    print("Comment with id ",comment_id, "for answer",answer_id,"in question",question_id,"has been removed")

###########AM3
def is_user_in_db(email):
    user_data = data_manager.get_user_by_email(email)
    if user_data:
        return True
    return False

def check_user(login_email, given_password):
    print("USER Verification => ",login_email)

    user_data = data_manager.get_user_by_email(login_email) #check if user with given email is in DB
    #zapytanie SQL zwraca listę słowników - unikatowy email powoduje, że jest to lista z jednym elementem index= 0]
    #print(user_data)
    #print(type(user_data))

    if user_data: #given user email exist in DataBase
        user_password = user_data[0]['password']
        valid = bcrypt.checkpw(given_password.encode(), user_password.encode()) #check given password - in DB passwrod not encode

        if valid:
            print("Haslo OK")
            return user_data
        else:
            print("Haslo NOK")
            return False

    return False #given user email NOT exist in DataBase

def add_new_user(email, password):
    add_user = {
        "email": email,
        "password":hash_password(password),
        "questions":"{}",
        "answers":"{}",
        "comments":"{}",
        "permission_level":1
    }

    data_manager.add_user_to_db(add_user)
    print("New user:",add_user["email"]," has been added")

def hash_password(password):
    password = password.encode()  # b'password'
    salt = bcrypt.gensalt()  # generate salt - provide unique passwords for each user
    user_password = bcrypt.hashpw(password, salt)  # generate unique passwords
    return user_password.decode() #decode -  do DB encode password
