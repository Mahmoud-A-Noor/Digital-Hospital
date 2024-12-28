# Digital-Hospital

A comprehensive digital healthcare platform designed to streamline communication between patients, doctors, and pharmacists. This application enables patients to book appointments (online or offline), share medical histories, and integrate prescription fulfillment. The platform also automates the delivery of post-appointment reports to pharmacies for prescription processing.

---

## Key Features
- **Appointment Scheduling**: Book appointments for both online and offline consultations.
- **Medical History Sharing**: Patients can share their medical history with healthcare professionals for better treatment planning.
- **Prescription Fulfillment Integration**: Seamlessly integrates with pharmacies to handle prescription orders.
- **Secure Authentication**: Users can register and log in using secure email/password and OTP (One-Time Password) for authentication.
- **Real-time Communication**: Instant communication between patients, doctors, and pharmacists via chat and notifications.
- **Dockerized Deployment**: Use Docker for containerization and seamless deployment.
---

## Technologies Used

### Frontend
- **HTML**: Markup language for structuring the content.
- **CSS**: Styling the user interface for a responsive and interactive experience.
- **JavaScript**: Enhancing interactivity and managing asynchronous actions in the UI.
- 
### Backend
- **Django**: Python-based web framework for building robust and scalable applications.
- **Django Channels**: For handling real-time communication and WebSockets.
- **Redis**: In-memory data structure store used for caching and session management.
- **MySQL**: Relational database for storing user data, appointments, and medical records.
- **OTP**: One-Time Password implementation for secure user authentication.
  
### Tools
- **Docker**: Containerization tool used to manage and deploy the application.
- **Django SMTP SSL**: Secure email sending via SMTP using SSL encryption for appointment reminders and notifications.

---

## Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/digital-hospital.git
cd digital-hospital
```

2. Install dependencies:
```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies (if any)
cd frontend
npm install
```

3. Create a `.env` file in the backend directory and configure the following variables:

```backend env
DJANGO_SECRET_KEY=<your_django_secret_key>
DB_NAME=<your_mysql_database_name>
DB_USER=<your_mysql_username>
DB_PASSWORD=<your_mysql_password>
OTP_SECRET_KEY=<your_otp_secret_key>
EMAIL_HOST=<your_smtp_host>
EMAIL_PORT=<your_smtp_port>
EMAIL_USE_TLS=True
EMAIL_HOST_USER=<your_email_address>
EMAIL_HOST_PASSWORD=<your_email_password>
```

4. Set up Docker:

```bash
# Build the Docker containers
docker-compose build

# Start the containers
docker-compose up
Open your browser and visit http://localhost:8000 to access the platform.
```

***Note =>*** To be able to use AI models download the ai models Folders from [here](https://drive.google.com/drive/folders/1mmO1keo0Xo924Y4GBg9BzlMcsrASpyyn?usp=sharing) and put them in Models folder inside the ai app

## Initial Credentials
#### Manager/Admin
**email** : superadmin@mail.com <br />
**password** : 0000<br /><br />
#### Doctor
**email** : doctor@mail.com <br />
**password** : 0000<br /><br />
#### Pharmacist
**email** : pharmacist@mail.com <br />
**password** : 0000<br /><br />
#### Patient
**email** : patient@mail.com <br />
**password** : 0000<br /><br />


## Project Preview
![1](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/f16d0b6c-fbbc-4cb9-a2a3-407df72531a5)
![2](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/f6796855-787d-453d-8aa2-8a59013d7deb)
![3](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/755577b0-a661-45b2-9da8-018ccbfa8153)
![4](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/22714399-7223-4397-a83e-d210da91bf97)
![5](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/04c9af68-4fe4-45f0-a65f-c81971ba3c69)

### Manager/Admin Dashboard
![manager_1](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/1ddffb86-74f5-4384-8359-5bfafc99f6e1)
![manager_2](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/c30f10cc-8894-4883-9d46-b5dc33b34f03)
![manager_3](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/f9012a70-6c59-42fe-a1f4-8f5c7ec641db)
![manager_4](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/155e71d2-8ce1-46b0-a986-ae57d7cd9d14)

### Doctor Dashboard
![doctor_1](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/2c4a9512-9a0e-4624-aa87-f818569d1e30)
![doctor_2](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/7680614e-3e81-4d8a-b60a-8b033437cf3c)
![doctor_3](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/73a23bc4-12da-44bd-b994-f0e98acd84a2)

### Pharmacist Dashboard
![pharmacist_1](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/7ca1ab39-3a29-4cab-b9d5-3978628dc379)

### Patient
![patient_1](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/eaf76249-5001-4eae-b83f-2842e8e5e84d)
![patient_2](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/5acfeae7-98aa-4cd6-91e8-77550f522108)
![patient_3](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/b1f6530f-9896-4b3d-81d5-1b65e269d14f)
![patient_4](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/c540b293-ae49-4485-a868-890810a15b95)
![patient_5](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/7d5aad5f-ed0c-4bf9-ac7d-e02ff844026f)
![patient_6](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/766582a8-561a-42c2-86d5-a337dd902b04)
![patient_7](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/ce2bce4f-da5c-4ce1-af37-f81c28837500)
![patient_8](https://github.com/Mahmoud-A-Noor/Digital-Hospital/assets/59361888/312b0cdc-1f92-458a-a368-c3b02ccb39ad)
---


## Folder Structure
```
digital-hospital/
├── backend/            # Django backend
├── frontend/           # React frontend (if applicable)
├── docker-compose.yml  # Docker setup for containerized deployment
├── .env                # Environment variables
├── requirements.txt    # Backend dependencies
├── package.json        # Frontend dependencies
├── README.md           # Project documentation
```
---

## Contributing

Contributions are welcome! Please create an issue or submit a pull request with your changes.

---

## Contact

For questions or feedback, please reach out to mahmoudnoor917@gmail.com.

