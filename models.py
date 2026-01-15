"""
Database Models for the Late Show API

This module defines the SQLAlchemy models for the application.
The models represent the data structure for episodes, guests, and their appearances.

Relationships:
- Episode has many Guests through Appearance
- Guest has many Episodes through Appearance
- Appearance belongs to Episode and Guest
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from datetime import datetime

# Define naming conventions for foreign keys
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


class Episode(db.Model):
    """
    Episode Model
    
    Represents a single episode of the Late Show.
    
    Attributes:
        id (int): Primary key, unique identifier for the episode
        date (str): Air date of the episode (format: M/D/YY)
        number (int): Episode number in the series
    
    Relationships:
        appearances: List of Appearance objects associated with this episode
    """
    
    __tablename__ = 'episodes'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Episode details
    date = db.Column(db.String(20), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    
    # One-to-many relationship with Appearance
    # cascade='all, delete-orphan' ensures that when an episode is deleted,
    # all associated appearances are also deleted
    appearances = db.relationship(
        'Appearance', 
        back_populates='episode', 
        cascade='all, delete-orphan',
        lazy='dynamic'
    )
    
    def __repr__(self):
        return f'<Episode {self.id}: {self.date}>'
    
    def to_dict(self, include_appearances=False):
        """
        Convert episode to dictionary representation
        
        Args:
            include_appearances (bool): Whether to include appearances in the output
        
        Returns:
            dict: Dictionary representation of the episode
        """
        result = {
            'id': self.id,
            'date': self.date,
            'number': self.number
        }
        
        if include_appearances:
            # Limit recursion by serializing appearances without nested guest details
            # The nested guest details will be handled in the route
            result['appearances'] = [
                appearance.to_dict(include_guest=True, include_episode=False)
                for appearance in self.appearances.all()
            ]
        
        return result


class Guest(db.Model):
    """
    Guest Model
    
    Represents a guest who appeared on the Late Show.
    
    Attributes:
        id (int): Primary key, unique identifier for the guest
        name (str): Full name of the guest
        occupation (str): Occupation/profession of the guest
    
    Relationships:
        appearances: List of Appearance objects associated with this guest
    """
    
    __tablename__ = 'guests'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Guest details
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    
    # One-to-many relationship with Appearance
    appearances = db.relationship(
        'Appearance', 
        back_populates='guest',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )
    
    def __repr__(self):
        return f'<Guest {self.id}: {self.name}>'
    
    def to_dict(self, include_appearances=False):
        """
        Convert guest to dictionary representation
        
        Args:
            include_appearances (bool): Whether to include appearances in the output
        
        Returns:
            dict: Dictionary representation of the guest
        """
        result = {
            'id': self.id,
            'name': self.name,
            'occupation': self.occupation
        }
        
        if include_appearances:
            result['appearances'] = [
                appearance.to_dict(include_guest=False, include_episode=True)
                for appearance in self.appearances.all()
            ]
        
        return result


class Appearance(db.Model):
    """
    Appearance Model
    
    Represents a guest's appearance on a specific episode.
    This is a join table with additional attributes (rating).
    
    Attributes:
        id (int): Primary key, unique identifier for the appearance
        rating (int): Rating for the appearance (1-5, inclusive)
        guest_id (int): Foreign key referencing the guest
        episode_id (int): Foreign key referencing the episode
    
    Relationships:
        guest: The Guest object associated with this appearance
        episode: The Episode object associated with this appearance
    """
    
    __tablename__ = 'appearances'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Appearance details with validation
    rating = db.Column(db.Integer, nullable=False)
    
    # Foreign keys
    guest_id = db.Column(
        db.Integer, 
        db.ForeignKey('guests.id', ondelete='CASCADE'),
        nullable=False
    )
    episode_id = db.Column(
        db.Integer, 
        db.ForeignKey('episodes.id', ondelete='CASCADE'),
        nullable=False
    )
    
    # Relationships
    guest = db.relationship('Guest', back_populates='appearances')
    episode = db.relationship('Episode', back_populates='appearances')
    
    def __repr__(self):
        return f'<Appearance {self.id}: Guest {self.guest_id} on Episode {self.episode_id}>'
    
    @validates('rating')
    def validate_rating(self, key, rating):
        """
        Validate that the rating is between 1 and 5 (inclusive)
        
        Args:
            key: The field name (should be 'rating')
            rating: The rating value to validate
        
        Returns:
            int: The validated rating
        
        Raises:
            ValueError: If the rating is not between 1 and 5
        """
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5 (inclusive)")
        return rating
    
    def to_dict(self, include_guest=True, include_episode=True):
        """
        Convert appearance to dictionary representation
        
        Args:
            include_guest (bool): Whether to include guest details
            include_episode (bool): Whether to include episode details
        
        Returns:
            dict: Dictionary representation of the appearance
        """
        result = {
            'id': self.id,
            'rating': self.rating,
            'guest_id': self.guest_id,
            'episode_id': self.episode_id
        }
        
        if include_guest:
            result['guest'] = self.guest.to_dict()
        
        if include_episode:
            result['episode'] = self.episode.to_dict()
        
        return result

