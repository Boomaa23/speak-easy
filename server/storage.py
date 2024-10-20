from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# -------------------------
# Models
# -------------------------

class User(db.Model):
    """
    Represents a user in the system.
    Each user can have multiple voices associated with them.
    """
    user_id = db.Column(db.String, primary_key=True)  # Cartesia user_id
    created_at = db.Column(db.DateTime, default=datetime.now())

    # One-to-Many relationship: A user can have multiple voices
    voices = db.relationship('VoiceModel', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.user_id}>"

    # Check if the user speaks a specific language
    def speaks_lang(self, lang):
        """Check if the user has a voice model in the given language."""
        return any(voice.language == lang for voice in self.voices)

    # Retrieve all voice models associated with this user
    def get_voices(self):
        """Return all voice models associated with this user."""
        return self.voices

    # Delete the user and their associated voice models
    def delete(self):
        """Delete the user and all their voice models."""
        for voice in self.voices:
            db.session.delete(voice)  # Delete related voices
        db.session.delete(self)  # Delete the user
        db.session.commit()

    # Get voice ID from language
    def get_voiceid_from_lang(self, lang):
        """Return the ID of the voice with the given language, if it exists."""
        if self.speaks_lang(lang):
            for voice in self.voices:
                if voice.language == lang:
                    return voice.voice_id
        return None

class VoiceModel(db.Model):
    """
    Represents a voice associated with a user.
    Includes metadata like language and privacy settings.
    """
    voice_id = db.Column(db.String, primary_key=True)  # Cartesia voice_id
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=False)  # Links to User
    is_public = db.Column(db.Boolean, default=False)  # Voice privacy setting
    description = db.Column(db.Text, nullable=True)  # Voice description
    language = db.Column(db.String(2), nullable=False)  # Language code (e.g., 'en', 'fr')
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"<VoiceModel {self.voice_id} in {self.language}>"

    # Get the user associated with this voice
    def belongs_to_user(self):
        """Return the user associated with this voice."""
        return self.user

    # Delete this voice model
    def delete(self):
        """Delete this voice model and return success status."""
        db.session.delete(self)
        db.session.commit()
        # Verify if the object was deleted
        deleted = VoiceModel.query.get(self.voice_id)
        return deleted is None  # Return True if deletion succeeded


# -------------------------
# Repository Functions
# -------------------------

def create_user(data):
    """Create a new user from a JSON object."""
    user_id = data.get("user_id")
    created_at = data.get("created_at", datetime.now())

    new_user = User(user_id=user_id, created_at=created_at)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def create_voice(data):
    """Create a new voice model from a JSON object."""
    voice_id = data.get("voice_id")
    user_id = data.get("user_id")  # User ID must exist in the database
    language = data.get("language")
    is_public = data.get("is_public", False)  # Default to False if not provided
    description = data.get("description")
    created_at = data.get("created_at", datetime.now())  # Use provided date or current date

    new_voice = VoiceModel(
        voice_id=voice_id,
        user_id=user_id,
        language=language,
        is_public=is_public,
        description=description,
        created_at=created_at
    )
    db.session.add(new_voice)
    db.session.commit()
    return new_voice

def get_user_by_id(user_id):
    """Retrieve a user by their user_id."""
    return User.query.get(user_id)

def get_voices_by_user_id(user_id):
    """Retrieve all voice models associated with a user."""
    user = get_user_by_id(user_id)
    if user:
        return user.get_voices()
    return []

def user_exists(user_id):
    """Check if a user with the given ID exists in the database."""
    return User.query.get(user_id) is not None
