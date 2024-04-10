from datetime import datetime

from PetPalsDAO import PetPalsDAO


class PetPalsServices:

    def __init__(self):
        self.pet_pals_dao = PetPalsDAO()

    def schedule_appointment(self, pet_owner, pet_name, appointment_time, address,
                                                          appointment_type,user_name):

        # Check if all input fields are provided
        if not all([pet_owner, pet_name, appointment_time, address, appointment_type]):
            return "All input fields are mandatory. Please provide values for all fields."

        current_time = datetime.now()

        # Parse the second datetime string into a datetime object
        appointment_time = datetime.strptime(appointment_time, '%Y-%m-%dT%H:%M')

        # Check if appointment time is in the past
        if appointment_time < current_time:
            return "Cannot schedule appointment for past dates."

        appointment_id = self.pet_pals_dao.schedule_appointment(pet_owner, pet_name, appointment_time, address,
                                                                    appointment_type, user_name)
        return f"Appointment scheduled successfully! Appointment ID: {appointment_id}"

    def cancel_appointment(self, appointment_id):
        self.pet_pals_dao.cancel_appointment(appointment_id)
        return "Appointment cancelled successfully!"

    def display_schedule(self, username):
        appointments = self.pet_pals_dao.display_schedule(username)
        return appointments

    def submit_form(self, firstname, lastname, email, subject, message):
        self.pet_pals_dao.submit_form(firstname, lastname, email, subject, message)
        return "Form submitted successfully!"
