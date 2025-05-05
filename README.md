# Booking System API

A FastAPI-based booking system that allows users to manage resources and make bookings.

## Features

- User authentication (register/login)
- Resource management (create, read)
- Booking management (create, read, delete)
- Conflict detection for overlapping bookings
- SQLite database
- Pydantic models for data validation
- Comprehensive test coverage

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Pydantic
- Python-jose (JWT tokens)
- Passlib (password hashing)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/booking-system.git
cd booking-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following variables:
```env
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the Application

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token

### Resources
- `POST /resources/` - Create a new resource
- `GET /resources/` - List all resources
- `GET /resources/{resource_id}` - Get a specific resource

### Bookings
- `POST /bookings/` - Create a new booking
- `GET /bookings/` - List all bookings
- `DELETE /bookings/{booking_id}` - Delete a booking

## Testing

Run the test suite:
```bash
pytest
```

View test coverage:
```bash
pytest --cov=app
```

## Project Structure

```
booking-system/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models/
│   ├── schemas/
│   ├── crud/
│   └── routers/
├── tests/
│   └── test_business_logic.py
├── requirements.txt
├── setup.py
├── setup.cfg
├── .gitignore
└── README.md
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 