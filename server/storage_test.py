import unittest
from storage import db, create_user, create_voice, get_user_by_id, get_voices_by_user_id, User, VoiceModel
from flask import Flask

class StorageTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a new Flask app and in-memory database for testing."""
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(self.app)

        # Create all database tables within the app context
        with self.app.app_context():
            db.create_all()

        self.app.app_context().push()  # Push context for tests to access DB

    def tearDown(self):
        """Tear down the database after each test."""
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        """Test creating a user."""
        user_data = {"id": "user1", "name": "John Doe"}
        user = create_user(user_data)

        # Verify the user was created correctly
        self.assertIsNotNone(user)
        self.assertEqual(user.id, "user1")
        self.assertEqual(user.name, "John Doe")

    def test_create_voice(self):
        """Test creating a voice model."""
        # First, create a user to link the voice to
        create_user({"id": "user1", "name": "John Doe"})

        voice_data = {
            "id": "voice1",
            "user_id": "user1",
            "name": "English Voice",
            "language": "en",
            "is_public": True
        }
        voice = create_voice(voice_data)

        # Verify the voice was created correctly
        self.assertIsNotNone(voice)
        self.assertEqual(voice.id, "voice1")
        self.assertEqual(voice.user_id, "user1")
        self.assertEqual(voice.language, "en")

    def test_get_user_by_id(self):
        """Test retrieving a user by ID."""
        create_user({"id": "user1", "name": "John Doe"})
        user = get_user_by_id("user1")

        # Verify the user was retrieved correctly
        self.assertIsNotNone(user)
        self.assertEqual(user.id, "user1")
        self.assertEqual(user.name, "John Doe")

    def test_get_voices_by_user_id(self):
        """Test retrieving all voices by user ID."""
        # Create a user and add some voices
        create_user({"id": "user1", "name": "John Doe"})

        create_voice({
            "id": "voice1",
            "user_id": "user1",
            "name": "English Voice",
            "language": "en"
        })

        create_voice({
            "id": "voice2",
            "user_id": "user1",
            "name": "French Voice",
            "language": "fr"
        })

        # Retrieve voices for the user by user ID
        voices = get_voices_by_user_id("user1")

        # Verify that two voices were returned
        self.assertEqual(len(voices), 2)

        # Check the details of the first voice
        self.assertEqual(voices[0].id, "voice1")
        self.assertEqual(voices[0].language, "en")

        # Check the details of the second voice
        self.assertEqual(voices[1].id, "voice2")
        self.assertEqual(voices[1].language, "fr")


    def test_user_speaks_lang(self):
        """Test the speaks_lang method on a user."""
        user = create_user({"id": "user1", "name": "John Doe"})
        create_voice({"id": "voice1", "user_id": "user1", "name": "English Voice", "language": "en"})

        # Check if the user speaks English
        self.assertTrue(user.speaks_lang('en'))
        self.assertFalse(user.speaks_lang('fr'))

    def test_delete_voice(self):
        """Test deleting a voice model."""
        create_user({"id": "user1", "name": "John Doe"})
        voice = create_voice({
            "id": "voice1",
            "user_id": "user1",
            "name": "English Voice",
            "language": "en"
        })

        # Delete the voice model and verify the result
        result = voice.delete()
        self.assertTrue(result)  # Check that the method returned True if successful

        # Verify the voice model no longer exists
        voices = get_voices_by_user_id("user1")
        self.assertEqual(len(voices), 0)  # Should be empty


if __name__ == "__main__":
    unittest.main()
