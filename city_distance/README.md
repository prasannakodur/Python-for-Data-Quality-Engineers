# City Distance Calculator

A tool to calculate straight-line distances between cities using their geographic coordinates. The tool uses the Haversine formula to account for Earth's spherical shape.

## Features

- **Accurate Distance Calculation**: Uses Haversine formula that accounts for Earth being a sphere
- **Persistent Storage**: Stores city coordinates in SQLite database for future use
- **Interactive Console**: User-friendly interface for inputting cities and coordinates
- **Automatic Prompting**: Asks for coordinates if city is not in database

## How It Works

1. User provides two city names via console
2. Tool checks if coordinates exist in database
3. If not found, prompts user to input coordinates (latitude/longitude)
4. Stores new coordinates in SQLite for future use
5. Calculates and displays distance in kilometers using Haversine formula

## Haversine Formula

The tool uses the Haversine formula to calculate great-circle distance between two points on a sphere. This is important because Earth is spherical, meaning:
- One degree of latitude ≈ 111 km everywhere
- One degree of longitude varies: 111 km at equator, 0 km at poles

The formula accounts for this variation and provides accurate straight-line distances.

## Usage

```bash
python city_distance_tool.py
```

### Example Session

```
============================================================
🌍 City Distance Calculator
============================================================
Calculate straight-line distance between cities
(Using Haversine formula for spherical Earth)
============================================================

Enter first city name: London
❌ City 'London' not found in database.
Please provide coordinates for London:
  Latitude (-90 to 90): 51.5074
  Longitude (-180 to 180): -0.1278
✓ Saved London to database

Enter second city name: Paris

❌ City 'Paris' not found in database.
Please provide coordinates for Paris:
  Latitude (-90 to 90): 48.8566
  Longitude (-180 to 180): 2.3522
✓ Saved Paris to database

============================================================
Calculating distance: London ↔ Paris
============================================================
✓ Found London in database: 51.5074°, -0.1278°
✓ Found Paris in database: 48.8566°, 2.3522°

============================================================
📏 RESULT
============================================================
Distance: 343.55 km
============================================================

Calculate another distance? (y/n):
```

## Database Schema

The tool creates a `cities.db` SQLite database with the following structure:

```sql
CREATE TABLE cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Coordinate Format

- **Latitude**: -90 (South Pole) to 90 (North Pole)
  - Positive = North, Negative = South
- **Longitude**: -180 to 180
  - Positive = East, Negative = West

## Files

- `city_distance_tool.py` - Main console interface
- `city_database.py` - SQLite database management
- `distance_calculator.py` - Haversine formula implementation
- `cities.db` - SQLite database (created on first run)

## Technical Details

- **Earth Radius**: 6371 km (mean radius)
- **Distance Type**: Great-circle distance (shortest path on sphere)
- **Accuracy**: Suitable for most practical purposes (±0.5%)

## Sample Cities for Testing

| City | Latitude | Longitude |
|------|----------|-----------|
| New York | 40.7128 | -74.0060 |
| London | 51.5074 | -0.1278 |
| Tokyo | 35.6762 | 139.6503 |
| Sydney | -33.8688 | 151.2093 |
| Mumbai | 19.0760 | 72.8777 |
| São Paulo | -23.5505 | -46.6333 |
