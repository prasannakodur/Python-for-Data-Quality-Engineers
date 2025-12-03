"""Console interface for city distance calculator."""
from city_database import CityDatabase
from distance_calculator import DistanceCalculator


class CityDistanceTool:
    """Interactive tool to calculate distances between cities."""
    
    def __init__(self):
        """Initialize the tool with database and calculator."""
        self.db = CityDatabase()
        self.calculator = DistanceCalculator()
    
    def get_city_coordinates(self, city_name: str) -> tuple[float, float]:
        """Get coordinates for a city, asking user if not in database.
        
        Args:
            city_name: Name of the city
            
        Returns:
            Tuple of (latitude, longitude)
        """
        coords = self.db.get_city_coordinates(city_name)
        
        if coords:
            print(f"✓ Found {city_name} in database: {coords[0]}°, {coords[1]}°")
            return coords
        
        print(f"\n❌ City '{city_name}' not found in database.")
        print(f"Please provide coordinates for {city_name}:")
        
        while True:
            try:
                lat = float(input("  Latitude (-90 to 90): "))
                if not -90 <= lat <= 90:
                    print("  Error: Latitude must be between -90 and 90")
                    continue
                
                lon = float(input("  Longitude (-180 to 180): "))
                if not -180 <= lon <= 180:
                    print("  Error: Longitude must be between -180 and 180")
                    continue
                
                # Save to database
                self.db.add_city(city_name, lat, lon)
                print(f"✓ Saved {city_name} to database")
                return (lat, lon)
                
            except ValueError:
                print("  Error: Please enter valid numbers")
    
    def calculate_distance(self, city1: str, city2: str) -> float:
        """Calculate distance between two cities.
        
        Args:
            city1: Name of first city
            city2: Name of second city
            
        Returns:
            Distance in kilometers
        """
        print(f"\n{'='*60}")
        print(f"Calculating distance: {city1} ↔ {city2}")
        print(f"{'='*60}")
        
        coords1 = self.get_city_coordinates(city1)
        coords2 = self.get_city_coordinates(city2)
        
        distance = self.calculator.haversine_distance(coords1, coords2)
        
        return distance
    
    def run(self):
        """Run the interactive console interface."""
        print("\n" + "="*60)
        print("🌍 City Distance Calculator")
        print("="*60)
        print("Calculate straight-line distance between cities")
        print("(Using Haversine formula for spherical Earth)")
        print("="*60 + "\n")
        
        # Show existing cities if any
        cities = self.db.list_all_cities()
        if cities:
            print(f"📍 {len(cities)} cities in database:")
            for name, lat, lon in cities:
                print(f"   • {name}: ({lat}°, {lon}°)")
            print()
        
        # Get city names from user
        city1 = input("Enter first city name: ").strip()
        if not city1:
            print("Error: City name cannot be empty")
            return
        
        city2 = input("Enter second city name: ").strip()
        if not city2:
            print("Error: City name cannot be empty")
            return
        
        if city1.lower() == city2.lower():
            print("Error: Please enter two different cities")
            return
        
        # Calculate distance
        distance = self.calculate_distance(city1, city2)
        
        # Display result
        print(f"\n{'='*60}")
        print(f"📏 RESULT")
        print(f"{'='*60}")
        print(f"Distance: {distance:.2f} km")
        print(f"{'='*60}\n")


def main():
    """Main entry point for the tool."""
    tool = CityDistanceTool()
    
    while True:
        try:
            tool.run()
            
            # Ask if user wants to calculate another distance
            again = input("\nCalculate another distance? (y/n): ").strip().lower()
            if again != 'y':
                print("\n👋 Goodbye!")
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            break


if __name__ == "__main__":
    main()
