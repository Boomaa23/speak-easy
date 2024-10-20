import difflib
import string
import unicodedata
import speech_recognition as sr
from pydub import AudioSegment


def transcribe_audio(file_path):
    """Transcribe the given audio file to text using SpeechRecognition."""
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(file_path)

    # Convert audio to a format supported by SpeechRecognition
    temp_file = "temp.wav"
    audio.export(temp_file, format="wav")

    with sr.AudioFile(temp_file) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file
        try:
            # Use the Google Web Speech API for transcription
            transcription = recognizer.recognize_google(audio_data)
            return transcription
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

def strip_accents(text):
    """Remove accents from a given text."""
    # Normalize the text and remove combining diacritical marks
    return ''.join(
        char for char in unicodedata.normalize('NFD', text) 
        if unicodedata.category(char) != 'Mn'
    )

def clean_text(text):
    """Remove punctuation and accents, and convert to lowercase."""
    # Strip accents
    text_no_accents = strip_accents(text)
    # Remove punctuation
    text_no_punctuation = ''.join(char for char in text_no_accents if char not in string.punctuation)
    # Convert to lowercase for case-insensitive comparison
    return text_no_punctuation.lower()

def compare_transcriptions(correct_transcription, user_transcription):
    """Compare correct and user transcriptions and return the differences."""
    # TODO: give phonetic feedback from comparison of audio files (pitch, freq, etc.)
    d = difflib.Differ()
    correct_cleaned = clean_text(correct_transcription)
    user_cleaned = clean_text(user_transcription)
    diff = list(d.compare(correct_cleaned.split(), user_cleaned.split()))
    return '\n'.join(diff)


def generate_suggestions(differences):
    """Generate suggestions based on the differences between the transcriptions."""
    missing_words = []
    extra_words = []
    feedback = []

    for line in differences.splitlines():
        if line.startswith('- '):  # Missing in user transcription
            word = line[2:]
            missing_words.append(word)
            #feedback.append(f"Consider practicing the pronunciation of the word: '{word}'.")

        elif line.startswith('+ '):  # Extra in user transcription
            word = line[2:]
            extra_words.append(word)
            #feedback.append(f"The word '{word}' was not in the expected transcription. Please check if it was pronounced correctly.")

    # Add feedback about missing words
    if missing_words:
        feedback += f"You missed the following word{'s' if len(missing_words) > 1 else ''} from the phrase: {', '.join(missing_words)}. Make sure to practice pronouncing {'these words' if len(missing_words) > 1 else 'this word'}.\n"
    else:
        feedback += "Great job! You pronounced all the expected words.\n"

    # Add feedback about extra words
    if extra_words:
        feedback += f"You said the following extra word{'s' if len(extra_words) > 1 else ''}: {', '.join(extra_words)}. Try to focus on the exact phrase next time.\n"

    suggestions = {
        "missing_words": missing_words,
        "extra_words": extra_words,
        "feedback": feedback
    }

    return suggestions
