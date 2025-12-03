"""Distance calculator using Haversine formula for spherical Earth."""
import math
from typing import Tuple


class DistanceCalculator:
    """Calculate distances between coordinates on Earth's surface."""
    
    # Earth's mean radius in kilometers
    EARTH_RADIUS_KM = 6371.0
    
    @staticmethod
    def haversine_distance(
        coord1: Tuple[float, float],
        coord2: Tuple[float, float]
    ) -> float:
        """Calculate great-circle distance between two points on Earth.
        
        Uses the Haversine formula to calculate the shortest distance over
        the Earth's surface, taking into account that Earth is a sphere.
        
        Args:
            coord1: Tuple of (latitude, longitude) for first point in degrees
            coord2: Tuple of (latitude, longitude) for second point in degrees
            
        Returns:
            Distance in kilometers
            
        Note:
            The Haversine formula accounts for the spherical nature of Earth,
            where the length of one degree varies with latitude.
        """
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        # Convert degrees to radians
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        # Haversine formula
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        # Calculate distance
        distance = DistanceCalculator.EARTH_RADIUS_KM * c
        
        return distance
