from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ENUM
from config import database_config
from sqlalchemy import BigInteger

Base = declarative_base()


class Driver(Base):
    __tablename__ = 'drivers'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    car_brand = Column(String(100))
    seating_capacity = Column(Integer)
    has_child_seat = Column(Boolean)
    about = Column(Text)
    current_location = Column(String)
    active_radius = Column(Integer)
    is_active = Column(Boolean)


class Passenger(Base):
    __tablename__ = 'passengers'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(BigInteger, primary_key=True)


class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True)
    passenger_id = Column(BigInteger, ForeignKey('passengers.id'))
    driver_id = Column(BigInteger, ForeignKey('drivers.id'), nullable=True)
    passenger_count = Column(Integer)
    has_luggage = Column(Boolean)
    has_child_seat = Column(Boolean)
    pickup_location = Column(String)
    dropoff_location = Column(String)
    status = Column(ENUM('waiting', 'en_route', 'driver_arrived', 'completed', 'cancelled', name='trip_statuses'))
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


class Feedback(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('drivers.id'))
    feedback = Column(Text)


class Advertisement(Base):
    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True)
    image = Column(String, nullable=True)
    text = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    last_published_at = Column(DateTime, nullable=True)

# Настройка движка базы данных
engine = create_engine(f"postgresql://{database_config['user']}:{database_config['password']}@{database_config['host']}/{database_config['db']}")

# Создание таблиц в базе данных
Base.metadata.create_all(engine)
