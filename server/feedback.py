import difflib
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


def compare_transcriptions(correct_transcription, user_transcription):
    """Compare correct and user transcriptions and return the differences."""
    d = difflib.Differ()
    diff = list(d.compare(correct_transcription.split(), user_transcription.split()))
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
            feedback.append(f"Consider practicing the pronunciation of the word: '{word}'.")

        elif line.startswith('+ '):  # Extra in user transcription
            word = line[2:]
            extra_words.append(word)
            feedback.append(f"The word '{word}' was not in the expected transcription. Please check if it was pronounced correctly.")

    suggestions = {
        "missing_words": missing_words,
        "extra_words": extra_words,
        "feedback": feedback
    }

    return suggestions
