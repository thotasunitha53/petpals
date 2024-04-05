from datetime import datetime
import mysql.connector


class PetPalsDAO:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Mani@123",
            database="employee_management_system"
        )
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                pet_owner VARCHAR(255),
                                pet_name VARCHAR(255),
                                appointment_time DATETIME,
                                address VARCHAR(255),
                                appointment_type VARCHAR(255)
                            )''')
        self.connection.commit()

    def schedule_appointment(self, pet_owner, pet_name, appointment_time, address, appointment_type):
        self.cursor.execute('''SELECT COUNT(*) FROM appointments WHERE appointment_time = %s''',
                            (appointment_time,))
        count = self.cursor.fetchone()[0]
        if count > 0:
            return "Another appointment is already scheduled at this time. Please choose another time."
        else:
            # Insert the new appointment
            query = '''INSERT INTO appointments (pet_owner, pet_name, appointment_time, address, appointment_type)
                       VALUES (%s, %s, %s, %s,%s)'''
            values = (pet_owner, pet_name, appointment_time, address, appointment_type)
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.lastrowid

    def cancel_appointment(self, appointment_id):
        query = '''DELETE FROM appointments WHERE id = %s'''
        values = (appointment_id,)
        self.cursor.execute(query, values)
        self.connection.commit()

    def display_schedule(self):
        self.cursor.execute('''SELECT * FROM appointments''')

        return self.cursor.fetchall()
