# ✈️ Airport Booking API

A Django-based RESTful API that allows users to browse available flights, book seats on airplanes, and manage airplane routes, crews, and airports.

## 🚀 Features

- Manage **airports** and link them to nearby cities.
- Define **routes** between airports with distances.
- Create and assign **airplanes** with types, seat rows, and layout.
- Manage **crews** and assign them to flights.
- Create and manage **flights** based on routes and airplanes.
- Allow users to create **orders** and **book tickets** for specific seats.
- **Seat validation** to prevent booking unavailable or out-of-range seats.
- Prevent **duplicate bookings** with unique constraints.

## 🛠️ Models Overview

### `Airport`
- `name`: Name of the airport.
- `closest_big_city`: Nearest large city.

### `Route`
- `source`: Departure airport.
- `destination`: Arrival airport.
- `distance`: Distance in kilometers or miles.

### `Crew`
- `first_name`, `last_name`: Crew member details.
- `full_name` property for easy access.

### `AirplaneType`
- `name`: Type or model of the airplane.

### `Airplane`
- `name`: Airplane identifier.
- `rows`: Number of seat rows.
- `seats_in_row`: Seats in a single row.
- `capacity` property for total number of seats.

### `Order`
- `created_at`: Timestamp of order creation.
- `user`: Linked user (custom user model from settings).

### `Flight`
- `route`: Foreign key to route.
- `airplane`: Foreign key to airplane.
- `crew`: Many-to-many relationship to crew.
- `departure_time` / `arrival_time`: Flight schedule.

### `Ticket`
- `row`, `seat`: Position in the airplane.
- `flight`: Linked flight.
- `order`: Linked order.
- Validation:
  - Ensures the row and seat numbers are within valid range of the airplane.
  - Prevents double booking with a unique constraint on `(row, seat, flight)`.

## ⚙️ Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd airport_api

2. Create and activate a virtual environment:
    ```bash
   python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. Install dependencies:
    ```bash
   pip install -r requirements.txt
4. Apply migrations:
    ```bash
   python manage.py makemigrations
    python manage.py migrate
5. Create a superuser:
    ```bash
   python manage.py createsuperuser
6. Run the development server:
    ```bash
   python manage.py runserver
7. Running with Docker (optional):
    ```bash
   docker-compose build
   docker-compose up
8. Test user:
- email: nazarchik@gmail.com
- password: 12345678

9. Create user:
- api/user/register/
10. Get user token:
- api/user/token/

## ⚙️ Environment Variables Setup

This project requires an `.env` file to securely store sensitive settings.

Create a file named `.env` in the project root directory with the following variables:

```env
# Django secret key (keep it secret!)
SECRET_KEY=your_django_secret_key_here

# Database configuration for PostgreSQL
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```
## 🔐 Admin Panel
- Access Django admin at http://localhost:8000/admin to manage airports, airplanes, routes, flights, and tickets.

## 📦 API Endpoints
### The API can be extended using Django REST Framework for:

- Listing flights
- Creating bookings
- Viewing available seats
- etc.

## ✅ Validation & Integrity
- Seats cannot be booked if already taken.
- Tickets with invalid seat/row combinations are rejected with a user-friendly message.

## 📚 API Documentation

The project includes **Swagger/OpenAPI documentation** for all available endpoints.

Once the server is running, you can access the interactive Swagger UI at:

http://localhost:8000/api/swagger/

## 🧑‍💻 Author
## Developed by Nazarii Khalimonov
## GitHub https://github.com/Carn1vor3