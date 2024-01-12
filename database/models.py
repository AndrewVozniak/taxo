from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ENUM, BYTEA
from config import database_config

Base = declarative_base()


class Driver(Base):
    __tablename__ = 'drivers'

    id = Column(Integer, primary_key=True)
    language = Column(String(50))
    name = Column(String(100))
    nickname = Column(String(50))
    registration_number = Column(String(50), unique=True)
    car_brand = Column(String(100))
    seating_capacity = Column(Integer)
    has_child_seat = Column(Boolean)
    about = Column(Text)
    current_location = Column(BYTEA)  # PostGIS geography point should be used for production
    active_radius = Column(Integer)
    is_active = Column(Boolean)


class Passenger(Base):
    __tablename__ = 'passengers'

    id = Column(String, primary_key=True)
    language = Column(String(50))
    name = Column(String(100))
    registration_number = Column(String(50), unique=True)


class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True)
    passenger_id = Column(Integer, ForeignKey('passengers.id'))
    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=True)
    passenger_count = Column(Integer)
    has_luggage = Column(Boolean)
    has_child_seat = Column(Integer)
    pickup_location = Column(BYTEA)  # PostGIS geography point should be used for production
    dropoff_location = Column(BYTEA)  # PostGIS geography point should be used for production
    status = Column(ENUM('waiting', 'en_route', 'completed', 'cancelled', name='trip_statuses'))
    requested_at = Column(DateTime)
    confirmed_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    driver = relationship('Driver', backref=backref('trips', cascade='all, delete-orphan'))
    passenger = relationship('Passenger', backref=backref('trips', cascade='all, delete-orphan'))


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.id'), nullable=False)
    passenger_rating = Column(Integer)  # Assuming rating out of 5
    driver_rating = Column(Integer)  # Assuming rating out of 5
    rating_date = Column(DateTime)

    trip = relationship('Trip', backref=backref('ratings', cascade='all, delete-orphan'))


class Charity(Base):
    __tablename__ = 'charity'

    id = Column(Integer, primary_key=True)
    donor_id = Column(Integer, ForeignKey('passengers.id'))
    amount = Column(Float)
    donation_date = Column(DateTime)


class Advertisement(Base):
    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True)
    image = Column(String)  # Path to image
    url = Column(String)  # URL for redirection
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_active = Column(Boolean)


class Block(Base):
    __tablename__ = 'blocks'

    id = Column(Integer, primary_key=True)
    passenger_id = Column(Integer, ForeignKey('passengers.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    reason = Column(Text)


# Настройка движка базы данных
engine = create_engine(f"postgresql://{database_config['user']}:{database_config['password']}@{database_config['host']}/{database_config['db']}")

# Создание таблиц в базе данных
Base.metadata.create_all(engine)
