from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
         ORDER BY id;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM answer
        ORDER BY id;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_question(cursor: RealDictCursor, add_question) -> list:
    # SQL query
    query = """
    INSERT INTO question(submission_time,view_number,vote_number,title,message,image)
    VALUES (%s,%s,%s,%s,%s,%s);
        """
    # Python data
    query_values = (
        add_question["submission_time"],
        add_question["view_number"],
        add_question["vote_number"],
        add_question["title"],
        add_question["message"],
        add_question["image"]
    )
    # insert into SQL database by SQL query filled with Python data
    cursor.execute(query, query_values)


@database_common.connection_handler
def last_question_id(cursor: RealDictCursor):
    query = """
    SELECT id FROM question
    ORDER BY id DESC LIMIT 1
    """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def update_user_question(cursor: RealDictCursor, user_id, question_id):
    query = """
    INSERT INTO user_question(user_id, question_id)
    VALUES (%s, %s)
    """
    cursor.execute(query, (user_id, question_id))


@database_common.connection_handler
def update_question(cursor: RealDictCursor, edit_question) -> list:
    # SQL query
    query = """
    UPDATE question
    SET title= %s,message= %s, image= %s
    WHERE id = %s;
        """
    # Python data
    query_values = (
        edit_question["title"],
        edit_question["message"],
        edit_question["image"],
        edit_question["id"]
    )
    # insert into SQL database by SQL query filled with Python data
    cursor.execute(query, query_values)


@database_common.connection_handler
def delete_question(cursor: RealDictCursor, question_id):
    # print("Qtype", type(question_id), question_id.isnumeric())

    if (question_id.isnumeric()):  # to avoid start with empty input (HTML get_method)
        # SQL query
        query = """
        DELETE FROM question_tag
        WHERE question_id = %s;
        DELETE FROM user_question
        WHERE question_id = %s;
        DELETE FROM user_answer
        WHERE question_id = %s;
        DELETE FROM user_comment
        WHERE question_id = %s;
        DELETE FROM comment 
        WHERE question_id = %s;
        DELETE FROM answer 
        WHERE question_id = %s;
        DELETE FROM question 
        WHERE id = %s;
            """
        # Python data => question_id
        # insert into SQL database by SQL query filled with Python data
        cursor.execute(query, (question_id, question_id, question_id, question_id, question_id, question_id, question_id))


@database_common.connection_handler
def add_answer(cursor: RealDictCursor, add_answer) -> list:
    # SQL query
    query = """
    INSERT INTO answer(submission_time,vote_number,question_id,message,image)
    VALUES (%s,%s,%s,%s,%s);
        """
    # Python data
    query_values = (
        add_answer["submission_time"],
        add_answer["vote_number"],
        add_answer["question_id"],
        add_answer["message"],
        add_answer["image"]
    )
    # insert into SQL database by SQL query filled with Python data
    cursor.execute(query, query_values)


@database_common.connection_handler
def last_answer_id(cursor: RealDictCursor):
    query = """
    SELECT id FROM answer
    ORDER BY id DESC LIMIT 1
    """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def update_user_answer(cursor: RealDictCursor, user_id, answer_id, question_id):
    query = """
    INSERT INTO user_answer(user_id, answer_id, question_id)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (user_id, answer_id, question_id))


@database_common.connection_handler
def update_answer(cursor: RealDictCursor, edited_answer) -> list:
    # SQL query
    query = """
    UPDATE answer
    SET message= %s, image= %s
    WHERE id = %s;
        """
    # Python data
    query_values = (
        edited_answer["message"],
        edited_answer["image"],
        edited_answer["id"]
    )
    # insert into SQL database by SQL query filled with Python data
    cursor.execute(query, query_values)


@database_common.connection_handler
def delete_answer(cursor: RealDictCursor, answer_id):
    print("DATA_MANAGER|SQL-delete_answer")
    # SQL query
    query = """
    DELETE FROM comment 
    WHERE answer_id = %s;
    DELETE FROM user_answer
    WHERE answer_id = %s;
    DELETE FROM answer 
    WHERE id = %s;
        """
    # Python data => question_id
    # insert into SQL database by SQL query filled with Python data
    cursor.execute(query, (answer_id, answer_id, answer_id))


@database_common.connection_handler
def get_tag_labels(cursor: RealDictCursor) -> list:
    # SQLE query
    query = """
    SELECT name, id 
    FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_tags(cursor: RealDictCursor) -> list:
    # SQL query
    query = """
    SELECT question_id, id, name
    FROM question_tag
    RIGHT JOIN tag ON question_tag.tag_id = tag.id;
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_tags_for_question(cursor: RealDictCursor, question_id) -> list:
    # SQL query
    query = """
    SELECT question_id, id, name
    FROM question_tag
    RIGHT JOIN tag ON question_tag.tag_id = tag.id
    WHERE question_id = %s;
    """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@database_common.connection_handler
def update_tags(cursor: RealDictCursor, tag) -> list:
    # SQL query
    query = """
    INSERT INTO question_tag(question_id, tag_id)
    VALUES (%s, %s)
    """
    query_values = (
        tag["question_id"],
        tag["tag_id"]
    )
    cursor.execute(query, query_values)


@database_common.connection_handler
def add_comment(cursor: RealDictCursor, new_comment) -> list:
    # SQL query
    query = """
    INSERT INTO comment (question_id,answer_id,message,submission_time)
    VALUES (%s,%s,%s,%s);
        """
    # Python data
    query_values = (
        new_comment[0],
        new_comment[1],
        new_comment[2],
        new_comment[3],
    )
    # insert into SQL database by SQL query filled with Python data
    cursor.execute(query, query_values)


@database_common.connection_handler
def last_comment_id(cursor: RealDictCursor):
    query = """
    SELECT id FROM comment
    ORDER BY id DESC LIMIT 1
    """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def update_user_comment(cursor: RealDictCursor, user_id, comment_id, question_id):
    query = """
    INSERT INTO user_comment(user_id, comment_id, question_id)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (user_id, comment_id, question_id))


@database_common.connection_handler
def get_comments(cursor: RealDictCursor) -> list:
    # SQL query
    query = """
    SELECT *
    FROM comment
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_comment(cursor: RealDictCursor, comment_id):
    print("DATA_MANAGER|SQL-delete_comment")
    # SQL query
    query = """
    DELETE FROM user_comment
    WHERE comment_id = %s;
    DELETE FROM comment 
    WHERE id = %s;
        """
    # Python data => question_id
    # insert into SQL database by SQL query filled with Python data
    cursor.execute(query, (comment_id, comment_id))


@database_common.connection_handler
def add_user(cursor: RealDictCursor, email, password, register_date):
    # SQL query
    query = """
    INSERT INTO users(login, password, registered)
    VALUES (%s,%s,%s)
    """
    cursor.execute(query, (email, password, register_date))


@database_common.connection_handler
def is_user(cursor: RealDictCursor, email):
    # SQL query
    query = """
    SELECT login, password from users 
    WHERE login = %s
    """
    cursor.execute(query, (email,))
    return cursor.fetchall()


@database_common.connection_handler
def user_id(cursor: RealDictCursor, email):
    # SQL query
    query = """
    SELECT id from users
    WHERE login = %s
    """
    cursor.execute(query, (email,))
    return cursor.fetchone()


@database_common.connection_handler
def user_data(cursor: RealDictCursor):
    query = """
    SELECT *
    FROM users 
    ORDER BY id
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def count_questions(cursor: RealDictCursor):
    query = """
    SELECT id, COUNT(user_id)
    FROM users LEFT JOIN user_question 
    ON users.id = user_question.user_id
    GROUP BY users.id
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@database_common.connection_handler
def count_answers(cursor: RealDictCursor):
    query = """
    SELECT id, COUNT(user_id)
    FROM users LEFT JOIN user_answer 
    ON users.id = user_answer.user_id
    GROUP BY users.id
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@database_common.connection_handler
def count_comments(cursor: RealDictCursor):
    query = """
    SELECT id, COUNT(user_id)
    FROM users LEFT JOIN user_comment
    ON users.id = user_comment.user_id
    GROUP BY users.id
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@database_common.connection_handler
def search_question(cursor: RealDictCursor, question):
    concat_quest = "%" + question + "%"
    query = """
    SELECT id, message 
    FROM question
    WHERE message LIKE %s """
    cursor.execute(query, (concat_quest,))
    return cursor.fetchall()


# RETURN: question_id | author_email related with given question_id
@database_common.connection_handler
def get_question_author(cursor: RealDictCursor, question_id):
    query = """
        SELECT question.id as question_id, users.login as author_email FROM question
        LEFT JOIN user_question ON question.id = user_question.question_id
        LEFT JOIN users ON user_question.user_id = users.id 
        WHERE question_id = %s """
    cursor.execute(query, (question_id,))
    return cursor.fetchone()


# RETURN: answer_id | author_email related with given question_id
@database_common.connection_handler
def get_answer_author(cursor: RealDictCursor, question_id):
    query = """
        SELECT answer.id as answer_id, users.login as author_email FROM answer
        LEFT JOIN user_answer ON answer.id = user_answer.answer_id
        LEFT JOIN users ON user_answer.user_id = users.id
        WHERE answer.question_id = %s """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


# RETURN: comment_id | author_email related with given question_id
@database_common.connection_handler
def get_comment_author(cursor: RealDictCursor, question_id):
    query = """
        SELECT comment.id as comment_id, users.login as author_email FROM comment
        LEFT JOIN user_comment ON comment.id = user_comment.comment_id
        LEFT JOIN users ON user_comment.user_id = users.id
        WHERE comment.question_id = %s"""
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


# RETURN: answer_id | answer_status
@database_common.connection_handler
def get_answers_status(cursor: RealDictCursor, question_id):
    query = """
        SELECT id as answer_id, answer_status FROM answer
        LEFT JOIN user_answer ON answer.id = user_answer.answer_id
        WHERE answer.question_id = %s"""
    cursor.execute(query, (question_id,))
    return cursor.fetchall()



@database_common.connection_handler
def set_answers_status(cursor: RealDictCursor, question_id, answer_id, answer_status):
    query = """
        UPDATE user_answer
        SET answer_status = %s
        WHERE answer_id = %s;"""
    # Python data
    query_values = (
        answer_status,
        answer_id)
    # SQL query with Python data
    cursor.execute(query, query_values)


@database_common.connection_handler
def questions_for_user(cursor: RealDictCursor, user_id):
    query = """
        SELECT question_id, title, message
        FROM user_question
        LEFT JOIN question
        ON question_id = id
        WHERE user_id = %s"""
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@database_common.connection_handler
def answers_for_user(cursor: RealDictCursor, user_id):
    query = """
        SELECT answer_id, message, answer.question_id
        FROM user_answer
        LEFT JOIN answer
        ON answer_id = id
        WHERE user_id = %s"""
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@database_common.connection_handler
def comments_for_user(cursor: RealDictCursor, user_id):
    query = """
        SELECT comment_id, comment.question_id, message
        FROM user_comment
        LEFT JOIN comment
        ON comment_id = id
        WHERE user_id = %s"""
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_user_id_by_answer_id(cursor: RealDictCursor, answer_id):
    query = """
        --get user id 
        SELECT user_id FROM users
        LEFT JOIN user_answer ON users.id = user_answer.user_id
        WHERE answer_id = %s; """
    # Python data
    cursor.execute(query, (answer_id,))
    return cursor.fetchone()


@database_common.connection_handler
def set_user_reputation(cursor: RealDictCursor, reputation, user_id):
    query = """
        UPDATE users
        SET reputation = reputation + %s
        WHERE id = %s;"""
    # Python data
    cursor.execute(query, (reputation, user_id))


@database_common.connection_handler
def set_user_reputation_1querry(cursor: RealDictCursor, reputation, answer_id):
    query = """
        UPDATE users
        SET reputation = reputation + %s
        WHERE id = (
            --get user id 
            SELECT user_id FROM users
            LEFT JOIN user_answer ON users.id = user_answer.user_id
            WHERE answer_id = %s
        );"""
    # Python data
    cursor.execute(query, (reputation, answer_id))


@database_common.connection_handler
def set_answer_vote(cursor: RealDictCursor, answer_vote, answer_id):
    query = """
        UPDATE answer
        SET vote_number = vote_number + %s
        WHERE id = %s;"""
    # Python data
    cursor.execute(query, (answer_vote, answer_id))


@database_common.connection_handler
def set_user_reputation_1querry_question(cursor: RealDictCursor, reputation, question_id):
    query = """
        UPDATE users
        SET reputation = reputation + %s
        WHERE id = (
            --get user id 
            SELECT user_id FROM users
            LEFT JOIN user_question ON users.id = user_question.user_id
            WHERE question_id = %s
        );"""
    # Python data
    cursor.execute(query, (reputation, question_id))


@database_common.connection_handler
def set_question_vote(cursor: RealDictCursor, question_vote, question_id):
    query = """
        UPDATE question
        SET vote_number = vote_number + %s
        WHERE id = %s;"""
    # Python data
    cursor.execute(query, (question_vote, question_id))


@database_common.connection_handler
def get_questions_by_tag(cursor: RealDictCursor,tag_name):
    query = """
        SELECT * FROM question
        LEFT JOIN question_tag ON question.id = question_tag.question_id
        LEFT JOIN tag ON question_tag.tag_id = tag.id
        WHERE name = %s;"""
    # Python data
    cursor.execute(query,(tag_name,))
    return cursor.fetchall()


@database_common.connection_handler
def update_view_number(cursor: RealDictCursor,question_id):
    query = """
        UPDATE question
        SET view_number = view_number+1
        WHERE id = %s;"""
    # Python data
    cursor.execute(query,(question_id,))
