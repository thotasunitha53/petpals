# from datetime import datetime
# import mysql.connector
#
# class PetPals:
#
#     def __init__(self):
#             self.connection = mysql.connector.connect(
#                 host="localhost",
#                 user="root",
#                 password="Mani@123",
#                 database="employee_management_system"
#             )
#             self.cursor = self.connection.cursor()
#             self.create_table()
#
#     def create_table(self):
#         self.cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
#                                 id INT AUTO_INCREMENT PRIMARY KEY,
#                                 pet_owner VARCHAR(255),
#                                 pet_name VARCHAR(255),
#                                 appointment_time DATETIME
#                             )''')
#         self.connection.commit()
#
#     def schedule_appointment(self, pet_owner, pet_name, appointment_time):
#         current_time = datetime.now()
#         try:
#             appointment_datetime = datetime.strptime(appointment_time, '%Y-%m-%d %I:%M %p')
#             if appointment_datetime > current_time:
#                 if appointment_time not in self.appointments:
#                     self.appointments[appointment_time] = [(pet_owner, pet_name)]
#                     print("Appointment scheduled successfully!")
#                 else:
#                     print("Sorry, appointment time already booked. Please choose another time.")
#             else:
#                 print("Sorry, you cannot schedule appointments for past dates.")
#         except ValueError:
#             print("Invalid date format. Please enter the date in 'YYYY-MM-DD HH:MM AM/PM' format.")
#
#     def cancel_appointment(self, appointment_time):
#         if appointment_time in self.appointments:
#             del self.appointments[appointment_time]
#
#     def display_schedule(self):
#         print("PetPals Appointment Schedule:")
#         for appointment_time, pets in self.appointments.items():
#             print(f"Time: {appointment_time}")
#             for pet_owner, pet_name in pets:
#                 print(f"- Pet Owner: {pet_owner}, Pet Name: {pet_name}")
#
#     def __del__(self):
#         self.connection.close()
#
#
# def main():
#     # Instantiate objects of different classes
#     pet_pals = PetPals()
#
#     while True:
#         print("\n1. Schedule Appointment")
#         print("2. Cancel Appointment")
#         print("3. Display Schedule")
#         print("4. Exit")
#         choice = input("Enter your choice: ")
#
#         if choice == '1':
#             pet_owner = input("Enter pet owner's name: ")
#             pet_name = input("Enter pet's name: ")
#             appointment_time = input("Enter appointment time (e.g., '2024-03-29 10:00 AM'): ")
#             pet_pals.schedule_appointment(pet_owner, pet_name, appointment_time)
#
#         elif choice == '2':
#             appointment_time = input("Enter appointment time to cancel: ")
#             pet_pals.cancel_appointment(appointment_time)
#             print("Appointment cancelled successfully!")
#
#         elif choice == '3':
#             pet_pals.display_schedule()
#
#         elif choice == '4':
#             print("Exiting...")
#             break
#
#         else:
#             print("Invalid choice! Please choose again.")
#
#
# if __name__ == "__main__":
#     main()