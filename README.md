# Web-Dev-Project
# 🐾 PawMatch

PawMatch is a platform that connects animals from shelters with loving families through a Tinder-like swiping interface. The system helps users discover animals available for adoption and provides a comprehensive health tracker for their adopted pets.

---

## 👥 Group Members

| Name | Role |
|------|------|
| Malika | Backend Developer (Django + DRF) |
| Tanzilya | Frontend Developer (Angular) |
| Alkhaidar | Integrator / Full-stack Support |

---

## 🚀 Project Overview

PawMatch is a full-stack web application built with Angular (frontend) and Django REST Framework (backend). It allows users to:

- 🐕 Discover animals through a Tinder-like swiping interface
- ❤️ Like animals and get notified when there's a mutual match
- 📝 Submit adoption requests and connect with shelters
- 💊 Track health records (vaccinations, medications, vet visits)
- ⏰ Set reminders for medications and vet appointments

---

## 📊 Models

### Core Models

| Model | Description |
|-------|-------------|
| User | Built-in Django user model (authentication) |
| UserProfile | Extended user profile with phone, address, rating |
| Shelter | Animal shelter information (name, address, contact) |
| Animal | Animals available for adoption (name, species, age, photo, medical status) |

### Swipe & Match System

| Model | Description |
|-------|-------------|
| Swipe | Records user likes/dislikes on animals |
| Match | Mutual likes between user and shelter/animal |

### Adoption & Health Tracking

| Model | Description |
|-------|-------------|
| AdoptionRequest | Adoption applications with status tracking |
| Pet | Adopted pets linked to users (health tracker) |
| HealthRecord | Medical records (vaccinations, checkups, medications) |
| Reminder | Custom reminders for medications, vet appointments |

---

