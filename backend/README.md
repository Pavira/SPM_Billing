# SPM Billing Software - FastAPI Backend

FastAPI backend for the SPM Billing Software application with Firebase authentication and Firestore integration.

## Features

- **Firebase Authentication**: User authentication with Firebase
- **Firestore Integration**: Real-time database operations
- **Customer Management**: CRUD operations for customers
- **Item Management**: Manage items/products
- **Invoice Management**: Create and manage invoices
- **Dashboard**: Statistics and analytics
- **CORS Support**: Configured for React frontend

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # Application entry point
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   ├── firebase.py        # Firebase initialization
│   │   ├── security.py        # Authentication logic
│   │   └── logging.py         # Logging configuration
│   ├── api/
│   │   └── v1/
│   │       ├── api.py         # API router aggregator
│   │       ├── auth.py        # Authentication endpoints
│   │       ├── customers.py   # Customer endpoints
│   │       ├── items.py       # Item endpoints
│   │       ├── invoices.py    # Invoice endpoints
│   │       └── dashboard.py   # Dashboard endpoints
│   ├── schemas/               # Pydantic models
│   ├── services/              # Business logic
│   ├── dependencies/          # Dependency injection
│   └── utils/                 # Utility functions
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing one
3. Generate a service account key:
   - Project Settings → Service Accounts → Generate New Private Key
   - Save the JSON file as `firebase-credentials.json` in the backend folder

4. Enable required services:
   - Authentication (Email/Password)
   - Cloud Firestore
   - Cloud Storage (optional)

### 3. Environment Configuration

Create a `.env` file with your configuration:

```
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
SECRET_KEY=your-secret-key
LOG_LEVEL=INFO
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 4. Run the Application

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

## API Endpoints

### Authentication

- `POST /api/v1/auth/verify-token` - Verify Firebase token
- `POST /api/v1/auth/logout` - Logout user

### Customers

- `POST /api/v1/customers/` - Create customer
- `GET /api/v1/customers/` - List all customers
- `GET /api/v1/customers/{id}` - Get customer by ID
- `PUT /api/v1/customers/{id}` - Update customer
- `DELETE /api/v1/customers/{id}` - Delete customer

### Items

- `POST /api/v1/items/` - Create item
- `GET /api/v1/items/` - List all items
- `GET /api/v1/items/{id}` - Get item by ID
- `PUT /api/v1/items/{id}` - Update item
- `DELETE /api/v1/items/{id}` - Delete item

### Invoices

- `POST /api/v1/invoices/` - Create invoice
- `GET /api/v1/invoices/` - List all invoices
- `GET /api/v1/invoices/{id}` - Get invoice by ID
- `PUT /api/v1/invoices/{id}` - Update invoice
- `DELETE /api/v1/invoices/{id}` - Delete invoice

### Dashboard

- `GET /api/v1/dashboard/stats` - Get dashboard statistics
- `GET /api/v1/dashboard/recent-invoices` - Get recent invoices

## Next Steps

1. Implement service methods with Firestore operations
2. Add data validation with Pydantic schemas
3. Implement business logic for calculations
4. Add comprehensive error handling
5. Add logging and monitoring
6. Deploy to production
