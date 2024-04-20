from datetime import datetime
import mysql.connector
from flask import render_template, redirect, url_for, session

from werkzeug.security import check_password_hash
#hello


class PetPalsDAO:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="HARSHAsonu@6",
            database="vet_appointment"
        )
        self.cursor = self.connection.cursor()
        self.create_users_table()
        self.create_table()  # <-- create_table() method is called here
        self.create_form_table()


    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                pet_owner VARCHAR(255),
                                pet_name VARCHAR(255),
                                appointment_time DATETIME,
                                address VARCHAR(255),
                                appointment_type VARCHAR(255),
                                user_id INT,
                                FOREIGN KEY (user_id) REFERENCES users(id)
                            )''')
        self.connection.commit()

    def create_form_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS form (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            first_name VARCHAR(255) NOT NULL,
                            last_name VARCHAR(255) NOT NULL,
                            email VARCHAR(255) NOT NULL,
                            subject VARCHAR(255) NOT NULL,
                            message TEXT NOT NULL
                               )''')
        self.connection.commit()

    def create_users_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                       id INT AUTO_INCREMENT PRIMARY KEY,
                                       username VARCHAR(255) NOT NULL,
                                       password VARCHAR(255) NOT NULL,
                                       UNIQUE KEY username (username)
                                   )''')
        self.connection.commit()


    def signup(self, username, hashed_password):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        self.connection.commit()

    def login(self, username):

        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        return cursor.fetchone()

    def schedule_appointment(self, pet_owner, pet_name, appointment_time, address, appointment_type ,user_name):
        self.cursor.execute('''SELECT COUNT(*) FROM appointments WHERE appointment_time = %s''',
                            (appointment_time,))
        count = self.cursor.fetchone()[0]
        if count > 0:
            return "Another appointment is already scheduled at this time. Please choose another time."
        else:

            # Insert the new appointment
            query = '''INSERT INTO appointments (pet_owner, pet_name, appointment_time, address, appointment_type, user_id)
            SELECT %s, %s, %s, %s, %s, id FROM users WHERE username = %s'''
            values = (pet_owner, pet_name, appointment_time, address, appointment_type,user_name)
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.lastrowid

    def cancel_appointment(self, appointment_id):
        query = '''DELETE FROM appointments WHERE id = %s'''
        values = (appointment_id,)
        self.cursor.execute(query, values)
        self.connection.commit()

    def display_schedule(self , username) :
        query = '''SELECT * FROM appointments WHERE user_id in
         (select id FROM users WHERE username = %s)'''
        self.cursor.execute(query, (username,))
        # print(self.cursor.fetchall())
        return self.cursor.fetchall()

    def submit_form(self, firstname, lastname, email, subject, message):
        # Insert form data into MySQL database
        sql = "INSERT INTO form (first_name, last_name, email, subject, message) VALUES (%s, %s, %s, %s, %s)"
        val = (firstname, lastname, email, subject, message)
        self.cursor.execute(sql, val)
        self.connection.commit()
