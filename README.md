# 🏥 Clinic Appointment Management System

### API Gateway & Microservices Architecture (FastAPI)

## 📌 Project Overview

The **Clinic Appointment Management System** is a microservices‑based backend application designed to manage clinic operations such as patients, doctors, appointments, and schedules.  
An **API Gateway** is used as a single entry point to route client requests to the relevant backend services.

This system is built using **FastAPI**, follows **RESTful principles**, and supports **scalable, secure, and maintainable architecture**.

***

## 🛠 Technologies Used

*   **FastAPI** – Backend framework
*   **HTTPX** – Inter-service communication
*   **Docker & Docker Compose** – Containerization
*   **Python 3.10+**
*   **REST APIs**
*   **Microservices Architecture**

***

## 📂 Folder Structure

    CLINIC-APPOINTMENT-MANAGEMENT-SYSTEM/
    │
    ├── api-gateway/
    │   ├── app/
    │   │   ├── main.py
    │   │   ├── core/
    │   │   │   └── config.py
    │   │   ├── routes/
    │   │   │   ├── patient.py
    │   │   │   ├── doctor.py
    │   │   │   ├── appointment.py
    |   |   |   ├── medical-record.py
    │   │   │   └── schedule.py
    │   │   ├── schemas/
    │   │   │   ├── patient.py
    │   │   │   ├── doctor.py
    |   |   |   ├── schedule.py
    |   |   |   ├── medical-record.py
    │   │   │   └── appointment.py
    │   │   └── utils/
    │   ├── requirements.txt
    │   └── Dockerfile
    │
    ├── patient-service/
    ├── doctor-service/
    ├── appointment-service/
    ├── schedule-service/
    ├── medical-record-service/
    │
    ├── docker-compose.yml
    └── README.md

***

## 🚪 API Gateway Responsibilities

*   Single entry point for all clients
*   Routes requests to correct microservices
*   Centralized error handling
*   Improves security by hiding internal services
*   Reduces client-side complexity

***

## 📡 Service Communication

The API Gateway communicates with microservices using **HTTPX async clients**.

Example (Patient Service):

```python
async with httpx.AsyncClient() as client:
    response = await client.get(PATIENT_SERVICE_URL)
```

***

## ▶️ How to Run the Project

###  Prerequisites

*   Python 3.10+
*   Docker & Docker Compose

### Run using Docker Compose

```bash
docker-compose up --build
```

### Access API Gateway

    http://localhost:8000

***

## 🧪 Testing APIs

You can test APIs using:

*   Postman
*   FastAPI Swagger UI

Swagger URL:

    http://localhost:8000/docs

***

## 🎯 Advantages of This Architecture

*   Scalable and modular system
*   Easy to maintain and extend
*   Independent service deployment
*   Centralized API management
*   Industry‑standard architecture

***

## 📘 Use Cases

*   Register patients
*   Manage doctors
*   Book appointments
*   Schedule doctor availability
*   Route requests securely through API Gateway

***

## 🧑‍🎓 Academic Purpose

This project is developed for **educational and academic purposes**, demonstrating:

*   Microservices Architecture
*   API Gateway pattern
*   FastAPI best practices
*   Cloud‑ready system design

***