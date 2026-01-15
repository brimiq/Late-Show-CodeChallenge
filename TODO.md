# Late Show API - Implementation Plan

## Project Structure
```
late-show/
├── README.md                    # Documentation
├── TODO.md                      # This file
├── app.py                       # Main Flask application
├── config.py                    # Configuration settings
├── models.py                    # Database models
├── routes.py                    # API routes
├── seed.py                      # Database seeding script
├── requirements.txt             # Dependencies
├── migrations/                  # Flask-Migrate directory
├── data/                        # Data files directory
│   └── guest_data.csv          # CSV file for seeding
└── instance/                    # SQLite database
```

## Tasks Completed ✅

### 1. Setup Project Structure ✅
- [x] Created requirements.txt with dependencies
- [x] Created config.py for Flask configuration
- [x] Created app.py with Flask app initialization

### 2. Create Database Models ✅
- [x] Created Episode model (id, date, number)
- [x] Created Guest model (id, name, occupation)
- [x] Created Appearance model (id, rating, guest_id, episode_id)
- [x] Set up relationships (Episode has many Guests through Appearance)
- [x] Set up cascade deletes for Appearance
- [x] Added rating validation (1-5 inclusive)
- [x] Implemented serialization methods with recursion limiting

### 3. Implement API Routes ✅
- [x] GET /episodes - List all episodes
- [x] GET /episodes/:id - Get episode with appearances
- [x] GET /guests - List all guests
- [x] POST /appearances - Create new appearance

### 4. Database Seeding ✅
- [x] Created seed.py script
- [x] Implemented CSV reading for guest data
- [x] Created sample episodes and appearances

### 5. Testing & Documentation ✅
- [x] Wrote comprehensive README.md
- [x] Verified Postman collection compatibility

## Models Design
- Episode: id (Integer, PK), date (String), number (Integer)
- Guest: id (Integer, PK), name (String), occupation (String)
- Appearance: id (Integer, PK), rating (Integer), guest_id (FK), episode_id (FK)

## Relationships
- Episode 1 -> * Appearance * -> 1 Guest
- Guest 1 -> * Appearance * -> 1 Episode

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Initialize database:
   ```bash
   mkdir instance
   flask --app app db init
   flask --app app db migrate -m "Initial migration"
   flask --app app db upgrade
   ```

3. Seed the database:
   ```bash
   python seed.py
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Testing Endpoints

Once the server is running, test these endpoints:

- `GET http://localhost:5000/episodes`
- `GET http://localhost:5000/episodes/1`
- `GET http://localhost:5000/guests`
- `POST http://localhost:5000/appearances` (with JSON body)

