"""Test the city distance calculator functionality."""
from city_database import CityDatabase
from distance_calculator import DistanceCalculator
import os


def test_distance_calculator():
    """Test the distance calculator with known cities."""
    print("="*60)
    print("Testing City Distance Calculator")
    print("="*60)
    
    # Initialize components
    db_path = "test_cities.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    db = CityDatabase(db_path)
    calculator = DistanceCalculator()
    
    # Test 1: Add cities to database
    print("\n📝 Test 1: Adding cities to database")
    cities = [
        ("London", 51.5074, -0.1278),
        ("Paris", 48.8566, 2.3522),
        ("New York", 40.7128, -74.0060),
        ("Tokyo", 35.6762, 139.6503),
    ]
    
    for name, lat, lon in cities:
        result = db.add_city(name, lat, lon)
        print(f"  {'✓' if result else '✗'} Added {name}: ({lat}°, {lon}°)")
    
    # Test 2: Retrieve coordinates
    print("\n📍 Test 2: Retrieving coordinates")
    for name, expected_lat, expected_lon in cities:
        coords = db.get_city_coordinates(name)
        if coords and coords[0] == expected_lat and coords[1] == expected_lon:
            print(f"  ✓ {name}: {coords}")
        else:
            print(f"  ✗ {name}: Expected ({expected_lat}, {expected_lon}), got {coords}")
    
    # Test 3: Calculate distances
    print("\n📏 Test 3: Calculating distances (using Haversine formula)")
    test_cases = [
        ("London", "Paris", 343.55),  # Approximate expected distance
        ("New York", "London", 5570.22),
        ("Tokyo", "New York", 10847.50),
    ]
    
    for city1, city2, expected_km in test_cases:
        coords1 = db.get_city_coordinates(city1)
        coords2 = db.get_city_coordinates(city2)
        distance = calculator.haversine_distance(coords1, coords2)
        
        # Allow 1% margin of error
        error_margin = expected_km * 0.01
        if abs(distance - expected_km) <= error_margin:
            print(f"  ✓ {city1} ↔ {city2}: {distance:.2f} km (expected ~{expected_km} km)")
        else:
            print(f"  ⚠ {city1} ↔ {city2}: {distance:.2f} km (expected ~{expected_km} km)")
    
    # Test 4: List all cities
    print("\n📋 Test 4: Listing all cities")
    all_cities = db.list_all_cities()
    print(f"  Total cities in database: {len(all_cities)}")
    for name, lat, lon in all_cities:
        print(f"    • {name}: ({lat}°, {lon}°)")
    
    # Test 5: Duplicate prevention
    print("\n🔒 Test 5: Testing duplicate prevention")
    result = db.add_city("London", 51.5074, -0.1278)
    print(f"  {'✗' if not result else '✓'} Attempted to add duplicate 'London': {'Rejected' if not result else 'Added'}")
    
    # Test 6: Verify Haversine formula accounts for Earth's curvature
    print("\n🌍 Test 6: Verifying spherical Earth calculations")
    # At equator, 1 degree longitude ≈ 111 km
    # At 60° latitude, 1 degree longitude ≈ 55.5 km
    equator_point = (0, 0)
    equator_1deg = (0, 1)
    high_lat_point = (60, 0)
    high_lat_1deg = (60, 1)
    
    equator_dist = calculator.haversine_distance(equator_point, equator_1deg)
    high_lat_dist = calculator.haversine_distance(high_lat_point, high_lat_1deg)
    
    print(f"  • 1° longitude at equator: {equator_dist:.2f} km")
    print(f"  • 1° longitude at 60° latitude: {high_lat_dist:.2f} km")
    print(f"  • Ratio: {high_lat_dist/equator_dist:.2f} (should be ~0.5)")
    
    if 0.49 <= high_lat_dist/equator_dist <= 0.51:
        print(f"  ✓ Correctly accounts for Earth's spherical shape")
    else:
        print(f"  ✗ Spherical calculations may be incorrect")
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60)
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"\n🧹 Cleaned up test database: {db_path}")


if __name__ == "__main__":
    test_distance_calculator()
