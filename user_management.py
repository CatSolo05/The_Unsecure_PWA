"""
Imports sqlite for database handling
"""

import sqlite3 as sql
from markupsafe import escape
import bcrypt


def insert_user(username, password, dob):
    """
    Inserts users into database
    """
    # 'salt' adds random noise to the password to make it harder to crack
    salt = bcrypt.gensalt()
    # 'hashpw' scrambles the password into a long string of random-looking characters
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), salt)
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    # We save the scrambled 'hashed_pw' instead of the real readable password
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, hashed_pw.decode("utf-8"), dob),
    )
    con.commit()
    con.close()


def retrieve_users(username, password):
    """
    function for retrieving users
    """
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    # We ask the database for the scrambled password belonging to this username
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cur.fetchone()
    con.close()
    # 'checkpw' compares what you typed with the scramble in the database
    if result and bcrypt.checkpw(password.encode("utf-8"), result[0].encode("utf-8")):
        return True
    return False


def insert_feedback(feedback):
    """Function for user submission of feedback"""
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO feedback (feedback) VALUES ('{feedback}')")
    con.commit()
    con.close()


def list_feedback():
    """Displays submitted user feedback on homepage"""
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w", encoding="utf-8")
    for row in data:
        f.write("<p>\n")
        f.write(f"{escape(row[1])}\n")
        f.write("</p>\n")
    f.close()
