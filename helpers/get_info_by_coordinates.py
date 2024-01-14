from geopy.geocoders import Nominatim
from config import APP_NAME


def get_info_by_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent=APP_NAME)
    location = geolocator.reverse((latitude, longitude), addressdetails=True)

    if location is not None:
        address = location.raw['address']

        # Используем номер дома, если он есть
        house_number = address.get('house_number', '')

        # Определяем, используем ли мы 'city' или 'town'
        city_or_town = address.get('city', '') or address.get('town', '')

        road = address.get('road', '')

        country = address.get('country', '')

        # Формируем строку адреса
        address_parts = [part for part in [house_number, road, city_or_town, country] if part]
        return ', '.join(address_parts)

    else:
        return "Название местоположения не найдено"
