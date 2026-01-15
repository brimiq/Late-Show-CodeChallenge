"""
API Routes for the Late Show Application

This module defines all the API endpoints for the Late Show API.
Each route returns JSON data as specified in the requirements.

Routes:
- GET /episodes: List all episodes
- GET /episodes/<id>: Get a specific episode with its appearances
- GET /guests: List all guests
- POST /appearances: Create a new appearance
"""

from flask import Blueprint, request, jsonify
from models import db, Episode, Guest, Appearance


# Create a Blueprint for API routes
api = Blueprint('api', __name__)


@api.route('/episodes', methods=['GET'])
def get_episodes():
    """
    Get all episodes
    
    Returns:
        JSON: List of all episodes with id, date, and number
        HTTP Status: 200 OK
    
    Example Response:
        [
            {"id": 1, "date": "1/11/99", "number": 1},
            {"id": 2, "date": "1/12/99", "number": 2}
        ]
    """
    # Query all episodes, ordered by episode number
    episodes = Episode.query.order_by(Episode.number).all()
    
    # Convert to list of dictionaries (without nested appearances for list view)
    episodes_list = [episode.to_dict(include_appearances=False) for episode in episodes]
    
    return jsonify(episodes_list), 200


@api.route('/episodes/<int:episode_id>', methods=['GET'])
def get_episode(episode_id):
    """
    Get a specific episode by ID with its appearances
    
    Args:
        episode_id (int): The ID of the episode to retrieve
    
    Returns:
        JSON: Episode data with nested appearances and guest details
        HTTP Status: 200 OK if found, 404 Not Found if not found
    
    Example Response (200):
        {
            "id": 1,
            "date": "1/11/99",
            "number": 1,
            "appearances": [
                {
                    "episode_id": 1,
                    "guest": {
                        "id": 1,
                        "name": "Michael J. Fox",
                        "occupation": "actor"
                    },
                    "guest_id": 1,
                    "id": 1,
                    "rating": 4
                }
            ]
        }
    
    Example Response (404):
        {"error": "Episode not found"}
    """
    # Query the episode by ID
    episode = Episode.query.get(episode_id)
    
    # If episode doesn't exist, return 404 error
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    
    # Convert to dictionary with nested appearances
    episode_data = episode.to_dict(include_appearances=True)
    
    return jsonify(episode_data), 200


@api.route('/guests', methods=['GET'])
def get_guests():
    """
    Get all guests
    
    Returns:
        JSON: List of all guests with id, name, and occupation
        HTTP Status: 200 OK
    
    Example Response:
        [
            {"id": 1, "name": "Michael J. Fox", "occupation": "actor"},
            {"id": 2, "name": "Sandra Bernhard", "occupation": "Comedian"},
            {"id": 3, "name": "Tracey Ullman", "occupation": "television actress"}
        ]
    """
    # Query all guests, ordered by name
    guests = Guest.query.order_by(Guest.name).all()
    
    # Convert to list of dictionaries (without nested appearances for list view)
    guests_list = [guest.to_dict(include_appearances=False) for guest in guests]
    
    return jsonify(guests_list), 200


@api.route('/appearances', methods=['POST'])
def create_appearance():
    """
    Create a new appearance
    
    This endpoint creates a new appearance record that associates
    a guest with an episode. The request body must include:
    - rating (1-5, inclusive)
    - episode_id (must exist in database)
    - guest_id (must exist in database)
    
    Request Body:
        {
            "rating": 5,
            "episode_id": 100,
            "guest_id": 123
        }
    
    Returns:
        JSON: Created appearance with nested guest and episode details
        HTTP Status: 201 Created if successful, 400 Bad Request if validation fails
    
    Example Response (201):
        {
            "id": 162,
            "rating": 5,
            "guest_id": 3,
            "episode_id": 2,
            "episode": {
                "date": "1/12/99",
                "id": 2,
                "number": 2
            },
            "guest": {
                "id": 3,
                "name": "Tracee Ullman",
                "occupation": "television actress"
            }
        }
    
    Example Response (400):
        {"errors": ["validation errors"]}
    """
    # Get JSON data from request body
    data = request.get_json()
    
    # Extract required fields
    rating = data.get('rating')
    episode_id = data.get('episode_id')
    guest_id = data.get('guest_id')
    
    # List to collect validation errors
    errors = []
    
    # Validate rating is present and within range
    if rating is None:
        errors.append("Rating is required")
    elif not isinstance(rating, int):
        errors.append("Rating must be an integer")
    elif rating < 1 or rating > 5:
        errors.append("Rating must be between 1 and 5 (inclusive)")
    
    # Validate episode_id is present
    if episode_id is None:
        errors.append("Episode ID is required")
    else:
        # Check if episode exists
        episode = Episode.query.get(episode_id)
        if not episode:
            errors.append("Episode not found")
    
    # Validate guest_id is present
    if guest_id is None:
        errors.append("Guest ID is required")
    else:
        # Check if guest exists
        guest = Guest.query.get(guest_id)
        if not guest:
            errors.append("Guest not found")
    
    # If there are validation errors, return 400 with error list
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Create the appearance
    appearance = Appearance(
        rating=rating,
        guest_id=guest_id,
        episode_id=episode_id
    )
    
    # Add to database session
    db.session.add(appearance)
    
    # Commit the transaction
    db.session.commit()
    
    # Return the created appearance with nested details
    return jsonify(appearance.to_dict(include_guest=True, include_episode=True)), 201


# Error handlers for 404 and 500 errors
@api.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors"""
    return jsonify({"error": "Resource not found"}), 404


@api.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors"""
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

