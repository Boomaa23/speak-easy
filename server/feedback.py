import os
import difflib
from google.cloud import speech
from pydub import AudioSegment

# Set up Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path_to_your_service_account_file.json'

def transcribe_audio(file_path):
    client = speech.SpeechClient()
    audio = AudioSegment.from_file(file_path).set_channels(1).set_frame_rate(16000)
    temp_file = "temp.wav"
    audio.export(temp_file, format="wav")

    with open(temp_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        return result.alternatives[0].transcript

def compare_transcriptions(correct_transcription, user_transcription):
    d = difflib.Differ()
    diff = list(d.compare(correct_transcription.split(), user_transcription.split()))
    return '\n'.join(diff)

def generate_suggestions(differences):
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

if __name__ == "__main__":
    # File paths for the correct pronunciation and user audio
    correct_audio_file_path = "path_to_correct_audio.wav"
    user_audio_file_path = "path_to_user_audio.wav"

    # Transcribe both audio files
    correct_transcription = transcribe_audio(correct_audio_file_path)
    user_transcription = transcribe_audio(user_audio_file_path)

    # Compare transcriptions and generate feedback
    differences = compare_transcriptions(correct_transcription, user_transcription)
    suggestions = generate_suggestions(differences)

    # Print feedback
    print("Feedback:")
    for feedback_line in suggestions['feedback']:
        print(feedback_line)

    if suggestions['missing_words']:
        print("Words to practice (missing):", ', '.join(suggestions['missing_words']))
    if suggestions['extra_words']:
        print("Words to correct (extra):", ', '.join(suggestions['extra_words']))
