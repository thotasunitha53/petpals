from datetime import datetime
from flask import Flask, request, jsonify, render_template
from PetPalsServices import PetPalsServices

app = Flask(__name__)

pet_pals_services = PetPalsServices()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/schedule_appointment', methods=['POST'])
def schedule_appointment():
    data = request.get_json()
    pet_owner = data['pet_owner']
    pet_name = data['pet_name']
    appointment_time = data['appointment_time']
    address = data['address']
    appointment_type = data['appointment_type']
    response = pet_pals_services.schedule_appointment(pet_owner, pet_name, appointment_time, address,
                                                      appointment_type)
    return jsonify({"message": response})


@app.route('/cancel_appointment', methods=['POST'])
def cancel_appointment():
    data = request.get_json()
    appointment_id = data['appointment_id']
    response = pet_pals_services.cancel_appointment(appointment_id)
    return jsonify({"message": response})


@app.route('/display_schedule', methods=['GET'])
def display_schedule():
    appointments = pet_pals_services.display_schedule()
    return jsonify({"appointments": appointments})


# @app.route('/submit_form', methods=['POST'])
# def submit_form():
#     data = request.get_json()
#     firstname = data['firstname']
#     lastname = data['lastname']
#     email = data['email']
#     subject = data['subject']
#     message = data['message']
#
#     response = pet_pals_services.submit_form(firstname, lastname, email, subject, message)
#       return render_template('index.html', message=response)
#

@app.route('/submit_form', methods=['POST'])
def submit_form():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    response = pet_pals_services.submit_form(firstname, lastname, email, subject, message)
    return render_template('index.html', message=response)



if __name__ == '__main__':
    app.run(debug=True)
