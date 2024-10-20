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
    id = db.Column(db.String, primary_key=True)  # Cartesia user_id
    name = db.Column(db.String(100), nullable=False)  # User's name
    created_at = db.Column(db.DateTime, default=datetime.now())

    # One-to-Many relationship: A user can have multiple voices
    voices = db.relationship('VoiceModel', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"

    # Instance method to check if the user speaks a specific language
    def speaks_lang(self, lang):
        """Check if the user has a voice model in the given language."""
        return any(voice.language == lang for voice in self.voices)

    # Instance method to get all voice models for the user
    def get_voices(self):
        """Retrieve all voice models associated with this user."""
        return self.voices

    # Instance method to delete the user and their voices
    def delete(self):
        """Delete the user and all associated voice models."""
        for voice in self.voices:
            db.session.delete(voice)  # Delete all related voice models
        db.session.delete(self)  # Delete the user
        db.session.commit()

    def get_voiceid_from_lang(self, lang):
        if self.speaks_lang(lang=lang):
            for voice in self.voices:
                if voice.language == lang:
                        return voice.id
        return None
    
                

class VoiceModel(db.Model):
    """
    Represents a voice associated with a user.
    Includes metadata like language and privacy settings.
    """
    id = db.Column(db.String, primary_key=True)  # Cartesia voice_id
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)  # Links to User
    is_public = db.Column(db.Boolean, default=False)  # Voice privacy setting
    name = db.Column(db.String(100), nullable=False)  # Voice name
    description = db.Column(db.Text, nullable=True)  # Voice description
    language = db.Column(db.String(2), nullable=False)  # Language code (e.g., 'en', 'fr')
    base_voice_id = db.Column(db.String, nullable=True)  # Optional: Base voice ID
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"<VoiceModel {self.name} in {self.language}>"

    def belongs_to_user(self):
        """Get the user associated with this voice."""
        return self.user
    
    # Instance method to delete the voice model
    def delete(self):
        """Delete this voice model."""
        db.session.delete(self)
        db.session.commit()


# -------------------------
# Repository Functions
# -------------------------

def create_user(data):
    """Create a new user from a JSON object."""
    user_id = data.get("id")
    name = data.get("name")
    created_at = data.get("created_at", datetime.now())  # Use provided date or current date

    new_user = User(id=user_id, name=name, created_at=created_at)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def create_voice(data):
    """Create a new voice model from a JSON object."""
    voice_id = data.get("id")
    user_id = data.get("user_id")  # User ID must exist in the database
    name = data.get("name")
    language = data.get("language")
    is_public = data.get("is_public", False)  # Default to False if not provided
    description = data.get("description")
    base_voice_id = data.get("base_voice_id")
    created_at = data.get("created_at", datetime.now())  # Use provided date or current date

    new_voice = VoiceModel(
        id=voice_id,
        user_id=user_id,
        name=name,
        language=language,
        is_public=is_public,
        description=description,
        base_voice_id=base_voice_id,
        created_at=created_at
    )
    db.session.add(new_voice)
    db.session.commit()
    return new_voice


def get_user_by_id(user_id):
    """Retrieve a user by their ID."""
    return User.query.get(user_id)

def get_voices_by_user_id(user_id):
    """Retrieve a voice model by its ID."""
    user = get_user_by_id(user_id)
    return user.get_voices()





