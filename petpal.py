from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from PetPalsDAO import PetPalsDAO
from PetPalsServices import PetPalsServices
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

pet_pals_services = PetPalsServices()
pet_pals_dao = PetPalsDAO()


@app.route('/')
def home():
    username = session.get('username')
    return render_template('home.html', username=username)

@app.route('/index')
def index():
    username = session.get('username')
    return render_template('index.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = pet_pals_dao.login(username)

        if user and check_password_hash(user['password'], password):
            session['username'] = username  # Store username in session
            return redirect(url_for('index'))  # Redirect to index after successful login
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('index'))  # Redirect to index after logout

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        pet_pals_dao.signup(username, hashed_password)

        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/services')
def services():
    username = session.get('username')
    return render_template('services.html', username=username)

@app.route('/admin')
def admin():
    return render_template('admin.html', message=None)

@app.route('/show_services')
def show_services():
    username = session.get('username')
    return render_template('services.html', username=username)

@app.route('/contactus')
def contactus():
    username = session.get('username')
    return render_template('contactus.html', username=username)





@app.route('/schedule_appointment', methods=['POST'])
def schedule_appointment():
    if 'username' in session:
        data = request.get_json()
        pet_owner = data['pet_owner']
        pet_name = data['pet_name']
        appointment_time = data['appointment_time']
        address = data['address']
        appointment_type = data['appointment_type']

        response = pet_pals_services.schedule_appointment(pet_owner, pet_name, appointment_time, address,
                                                          appointment_type,session['username'])
        return jsonify({"message": response})

    else:
        return jsonify({"error": "User not logged in"})



@app.route('/cancel_appointment', methods=['POST'])
def cancel_appointment():
    data = request.get_json()
    appointment_id = data['appointment_id']
    response = pet_pals_services.cancel_appointment(appointment_id)
    return jsonify({"message": response})


@app.route('/display_schedule', methods=['GET'])
def display_schedule():
    if 'username' in session:
        appointments = pet_pals_services.display_schedule(session['username'])

        if isinstance(appointments, list) and not appointments:  # Check if lst is an empty list
            return jsonify({"message": "Currently, no appointments scheduled!"})
        else:
            return jsonify({"appointments": appointments})
    else:
        return jsonify({"error": "User not logged in"})



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
