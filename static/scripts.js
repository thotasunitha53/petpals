function scheduleAppointment() {
    const petOwner = document.getElementById('pet-owner').value;
    const petName = document.getElementById('pet-name').value;
    const appointmentTime = document.getElementById('appointment-time').value;
    const address = document.getElementById('address').value; // Get address value
    const appointmentType = document.getElementById('appointment-type').value; // Get appointment type value

    fetch('/schedule_appointment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            pet_owner: petOwner,
            pet_name: petName,
            appointment_time: appointmentTime,
            address: address, // Include address in the request
            appointment_type: appointmentType // Include appointment type in the request
        })
    })
    .then(response => response.json())
    .then(data => alert(data.message|| data.error))
    .catch(error => console.error('Error:', error));



}
function cancelAppointment() {
    const appointmentId = document.getElementById('appointment-id').value;

    fetch('/cancel_appointment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            appointment_id: appointmentId
        })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
}



function displaySchedule() {
    fetch('/display_schedule')
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Network response was not ok.');
        }
    })
    .then(data => {
        const appointmentsList = document.getElementById('appointments');
        appointmentsList.innerHTML = '';

        if (data.hasOwnProperty('appointments')) {
            data.appointments.forEach(appointment => {
                const listItem = document.createElement('li');
                listItem.textContent = `ID: ${appointment[0]}, Pet Owner: ${appointment[1]}, Pet Name: ${appointment[2]}, Time: ${appointment[3]} , Address : ${appointment[4]} , Service : ${appointment[5]}`;
                appointmentsList.appendChild(listItem);
            });
        } else if (data.hasOwnProperty('message')) {
            const messageItem = document.createElement('li');
            messageItem.textContent = data.message;
            appointmentsList.appendChild(messageItem);
        } else if (data.hasOwnProperty('error')) {
            const errorItem = document.createElement('li');
            errorItem.textContent = `Error: ${data.error}`;
            appointmentsList.appendChild(errorItem);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        const errorMessage = document.createElement('li');
        errorMessage.textContent = 'An error occurred while fetching the schedule.';
        document.getElementById('appointments').appendChild(errorMessage);
    });
}

function displayLoginLogout() {
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    if (sessionStorage.getItem('username')) {
        // User is logged in
        loginLink.style.display = 'none';
        logoutLink.style.display = 'inline'; // Adjust style to display as inline element
    } else {
        // User is not logged in
        loginLink.style.display = 'inline'; // Adjust style to display as inline element
        logoutLink.style.display = 'none';
    }
}

function logout() {
    sessionStorage.removeItem('username');
    displayLoginLogout();
}


function showMessage() {
    alert("Form submitted successfully!");
}