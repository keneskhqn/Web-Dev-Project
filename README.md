# Web-Dev-Project
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
