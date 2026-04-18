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

=======
Group Members: Kayerzhan Tanzilya, Imekeshova Malika, Keneskhan Alkhaidar
## Project: PawMatch

PawMatch is a platform that connects animal shelters with users who want to adopt pets. The system allows users to browse animals available for adoption and submit adoption requests. It simplifies the adoption process by providing a clear and structured way for users to apply for animals from shelters


## Models:
  * User (built-in Django model)
  * Shelter (animal shelter information such as name, address, contact)
  * Animal (animals available for adoption with details like name, species, age, and medical status)
  * AdoptionRequest (user applications to adopt animals with status tracking)

## Relationships:
  * Animal references Shelter to indicate which shelter the animal belongs to
  * AdoptionRequest references User to indicate who is applying for adoption
  * AdoptionRequest references Animal to indicate which animal is requested
  * Shelter references User to indicate that each shelter is managed by a registered user
>>>>>>> f3f6483defcfbb65f8823222203603700a77859d
