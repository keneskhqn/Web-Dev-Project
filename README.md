Group Members: Kayerzhan Tanzilya, Imekeshova Malika, Keneskhan Alkhaidar

## Project: PawMatch

PawMatch is a pet adoption platform that connects shelters with people who want to adopt. Users can browse animals, swipe/like profiles, and manage matched pets through a structured Django + Angular application.

## Backend Models

- User (built-in Django auth model)
- Shelter (name, address, phone, location, social links, website)
- Animal (adoptable pet profile: species, breed, age, vaccination/neutering, adoption status)
- Swipe (user like/dislike action for an animal)
- Match (successful user-animal match)
- Pet (a user-owned pet record linked to an animal)

## Model Relationships

- Animal -> Shelter (many-to-one): each animal belongs to one shelter
- Animal -> User as submitted_by (many-to-one, optional): tracks who submitted the animal
- Swipe -> User and Animal (many-to-one on both sides, unique per user-animal pair)
- Match -> User and Animal (many-to-one on both sides, unique per user-animal pair)
- Pet -> User (many-to-one): one user can have multiple pets
- Pet -> Animal (one-to-one): one animal can become one pet record
