from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common

@database_common.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM answer"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_question(cursor: RealDictCursor,add_question) -> list:
    #SQL query
    query = """
    INSERT INTO question(submission_time,view_number,vote_number,title,message,image)
    VALUES (%s,%s,%s,%s,%s,%s);
        """
    #Python data
    query_values = (
    add_question["submission_time"],
    add_question["view_number"],
    add_question["vote_number"],
    add_question["title"],
    add_question["message"],
    add_question["image"]
    )
    #insert into SQL database by SQL query filled with Python data
    cursor.execute(query, query_values)


@database_common.connection_handler
def update_question(cursor: RealDictCursor, edit_question) -> list:
    #SQL query
    query = """
    UPDATE question
    SET title= %s,message= %s, image= %s
    WHERE id = %s;
        """
    #Python data
    query_values = (
    edit_question["title"],
    edit_question["message"],
    edit_question["image"],
    edit_question["id"]
    )
    #insert into SQL database by SQL query filled with Python data
    cursor.execute(query,query_values)


@database_common.connection_handler
def delete_question(cursor: RealDictCursor, question_id):
    print("Qtype", type(question_id),question_id.isnumeric())

    if (question_id.isnumeric()):
        #SQL query
        query = """
        DELETE FROM question_tag
        WHERE question_id = %s;
        DELETE FROM comment 
        WHERE question_id = %s;
        DELETE FROM answer 
        WHERE question_id = %s;
        DELETE FROM question 
        WHERE id = %s;
            """
        #Python data => question_id
        #insert into SQL database by SQL query filled with Python data
        cursor.execute(query,(question_id, question_id, question_id,question_id))


@database_common.connection_handler
def add_answer(cursor: RealDictCursor,add_answer) -> list:
    #SQL query
    query = """
    INSERT INTO answer(submission_time,vote_number,question_id,message,image)
    VALUES (%s,%s,%s,%s,%s);
        """
    #Python data
    query_values = (
    add_answer["submission_time"],
    add_answer["vote_number"],
    add_answer["question_id"],
    add_answer["message"],
    add_answer["image"]
    )
    #insert into SQL database by SQL query filled with Python data
    cursor.execute(query, query_values)


@database_common.connection_handler
def update_answer(cursor: RealDictCursor, edited_answer) -> list:
    #SQL query
    query = """
    UPDATE answer
    SET message= %s, image= %s
    WHERE id = %s;
        """
    #Python data
    query_values = (
    edited_answer["message"],
    edited_answer["image"],
    edited_answer["id"]
    )
    #insert into SQL database by SQL query filled with Python data
    cursor.execute(query,query_values)


@database_common.connection_handler
def delete_answer(cursor: RealDictCursor, answer_id):
    print("DATA_MANAGER|SQL-delete_answer")
    #SQL query
    query = """
    DELETE FROM comment 
    WHERE answer_id = %s;
    DELETE FROM answer 
    WHERE id = %s;
        """
    #Python data => question_id
    #insert into SQL database by SQL query filled with Python data
    cursor.execute(query,(answer_id,answer_id))

@database_common.connection_handler
def get_tag_labels(cursor: RealDictCursor) -> list:
    #SQLE query
    query = """
    SELECT name 
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
def update_tags(cursor: RealDictCursor, tag) -> list:
    #SQL query
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
    #SQL query
    query = """
    INSERT INTO comment (question_id,answer_id,message,submission_time)
    VALUES (%s,%s,%s,%s);
        """
    #Python data
    query_values = (
    new_comment[0],
    new_comment[1],
    new_comment[2],
    new_comment[3],
    )
    #insert into SQL database by SQL query filled with Python data
    cursor.execute(query, query_values)


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
def delete_comment(cursor: RealDictCursor,comment_id):
    print("DATA_MANAGER|SQL-delete_comment")
    #SQL query
    query = """
    DELETE FROM comment 
    WHERE id = %s;
        """
    #Python data => question_id
    #insert into SQL database by SQL query filled with Python data
    cursor.execute(query,(comment_id,))


####AM3
@database_common.connection_handler
def get_user_by_email(cursor: RealDictCursor, user_email) -> str:
    #SQL query
    query = """
    SELECT * FROM users
    WHERE email = %s;
        """
    #Python data
    query_values = (user_email,)
    #insert into SQL database by SQL query filled with Python data
    cursor.execute(query,query_values)
    return cursor.fetchall() #fetchall() -> fetchone()

@database_common.connection_handler
def add_user_to_db(cursor: RealDictCursor,add_user) -> list:
    #SQL query
    query = """
    INSERT INTO users(email,password)
    VALUES (%s,%s);
        """
    #Python data
    query_values = (
    add_user["email"],
    add_user["password"],
    )
    #insert into SQL database by SQL query filled with Python data
    cursor.execute(query, query_values)

@database_common.connection_handler
def add_user_question(cursor: RealDictCursor,user_id,question_id) -> int:
    #SQL query
    query = """
    INSERT INTO user_question(user_id,question_id)
    VALUES (%s,%s);
        """
    #Python data
    query_values = (
    user_id,
    question_id,
    )
    #insert into SQL database by SQL query filled with Python data
    cursor.execute(query, query_values)

@database_common.connection_handler
def add_user_answer(cursor: RealDictCursor,user_id,answer_id) -> int:
    #SQL query
    query = """
    INSERT INTO user_answer(user_id,answer_id)
    VALUES (%s,%s);
        """
    #Python data
    query_values = (
    user_id,
    answer_id,
    )
    #insert into SQL database by SQL query filled with Python data
    cursor.execute(query, query_values)

@database_common.connection_handler
def add_user_comment(cursor: RealDictCursor,user_id,comment_id) -> int:
    #SQL query
    query = """
    INSERT INTO user_comment(user_id,comment_id)
    VALUES (%s,%s);
        """
    #Python data
    query_values = (
    user_id,
    comment_id,
    )
    print(user_id,comment_id)
    #insert into SQL database by SQL query filled with Python data
    cursor.execute(query, query_values)