from datetime import datetime
from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)


# main class

@app.route('/')
def index():
    return render_template('index.html')


class PetPals:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Mani@123",
            database="employee_management_system"
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                                        id INT AUTO_INCREMENT PRIMARY KEY,
                                        pet_owner VARCHAR(255),
                                        pet_name VARCHAR(255),
                                        appointment_time DATETIME,
                                        address VARCHAR(255),  -- New column
                                        appointment_type VARCHAR(50)
                                    )''')
        self.connection.commit()

    def schedule_appointment(self, pet_owner, pet_name, appointment_time, address, appointment_type):
        current_time = datetime.now()
        print(current_time)
        print(appointment_time)

        # Parse the first datetime string into a datetime object
        #current_time = datetime.strptime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')

        # Parse the second datetime string into a datetime object
        appointment_time = datetime.strptime(appointment_time, '%Y-%m-%dT%H:%M')


        # Check if appointment time is in the past
        if appointment_time < current_time:
            return "Cannot schedule appointment for past dates."

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
            return "Appointment scheduled successfully!"

    def cancel_appointment(self, appointment_id):
        query = '''DELETE FROM appointments WHERE id = %s'''
        values = (appointment_id,)
        self.cursor.execute(query, values)
        self.connection.commit()
        return "Appointment cancelled successfully!"

    def display_schedule(self):
        self.cursor.execute('''SELECT * FROM appointments''')
        appointments = self.cursor.fetchall()
        return appointments


@app.route('/schedule_appointment', methods=['POST'])
def schedule_appointment():
    data = request.get_json()
    pet_owner = data['pet_owner']
    pet_name = data['pet_name']
    appointment_time = data['appointment_time']
    address = data['address']
    appointment_type = data['appointment_type']
    response = pet_pals.schedule_appointment(pet_owner, pet_name, appointment_time, address, appointment_type)
    return jsonify({"message": response})


@app.route('/cancel_appointment', methods=['POST'])
def cancel_appointment():
    data = request.get_json()
    appointment_id = data['appointment_id']
    response = pet_pals.cancel_appointment(appointment_id)
    return jsonify({"message": response})


@app.route('/display_schedule', methods=['GET'])
def display_schedule():
    appointments = pet_pals.display_schedule()
    return jsonify({"appointments": appointments})


if __name__ == '__main__':
    pet_pals = PetPals()
    app.run(debug=True)
