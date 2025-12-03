"""Demo script showing city distance calculator in action."""
from city_database import CityDatabase
from distance_calculator import DistanceCalculator


def demo():
    """Demonstrate the city distance calculator."""
    print("="*70)
    print("🌍 City Distance Calculator - DEMO")
    print("="*70)
    print("This demo shows how the tool calculates distances between cities")
    print("using the Haversine formula (accounting for Earth's spherical shape)")
    print("="*70 + "\n")
    
    # Initialize
    db = CityDatabase("demo_cities.db")
    calculator = DistanceCalculator()
    
    # Pre-populate some cities
    demo_cities = [
        ("London", 51.5074, -0.1278),
        ("Paris", 48.8566, 2.3522),
        ("New York", 40.7128, -74.0060),
        ("Tokyo", 35.6762, 139.6503),
        ("Sydney", -33.8688, 151.2093),
        ("Mumbai", 19.0760, 72.8777),
    ]
    
    print("📍 Pre-populating database with sample cities:")
    for name, lat, lon in demo_cities:
        db.add_city(name, lat, lon)
        print(f"   • {name}: ({lat}°, {lon}°)")
    
    print("\n" + "="*70)
    print("📏 CALCULATING DISTANCES")
    print("="*70 + "\n")
    
    # Calculate various distances
    distance_pairs = [
        ("London", "Paris"),
        ("New York", "London"),
        ("Tokyo", "Sydney"),
        ("Mumbai", "London"),
        ("New York", "Tokyo"),
    ]
    
    for city1, city2 in distance_pairs:
        coords1 = db.get_city_coordinates(city1)
        coords2 = db.get_city_coordinates(city2)
        distance = calculator.haversine_distance(coords1, coords2)
        
        print(f"{city1} ↔ {city2}")
        print(f"  {city1}: {coords1[0]}°, {coords1[1]}°")
        print(f"  {city2}: {coords2[0]}°, {coords2[1]}°")
        print(f"  ➜ Distance: {distance:.2f} km")
        print()
    
    print("="*70)
    print("🌍 WHY HAVERSINE FORMULA?")
    print("="*70)
    print("Earth is a sphere, so the length of one degree varies:")
    print()
    
    # Demonstrate latitude effect
    equator = (0, 0)
    equator_1deg = (0, 1)
    lat_60 = (60, 0)
    lat_60_1deg = (60, 1)
    
    eq_dist = calculator.haversine_distance(equator, equator_1deg)
    high_dist = calculator.haversine_distance(lat_60, lat_60_1deg)
    
    print(f"• At equator (0°):     1° longitude = {eq_dist:.2f} km")
    print(f"• At 60° latitude:     1° longitude = {high_dist:.2f} km")
    print(f"• Ratio:               {high_dist/eq_dist:.2%}")
    print()
    print("This is why we can't use simple Euclidean distance!")
    print("The Haversine formula correctly accounts for Earth's curvature.")
    
    print("\n" + "="*70)
    print("✅ Demo completed!")
    print("="*70)
    print("\nTo use the interactive tool, run:")
    print("  python city_distance_tool.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo()
