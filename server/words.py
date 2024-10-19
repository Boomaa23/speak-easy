# Retrieve practice words for different languages

# English words
english_words = [
    "House", "Water", "Friend", "Book", "Food",
    "Love", "Family", "Dog", "Sun", "Happy"
]

# English phrases
english_phrases = [
    "What is your name?",
    "How are you today?",
    "Where do you live?",
    "I would like some coffee, please.",
    "Can you help me?",
    "What time is it?",
    "I am learning English.",
    "It’s nice to meet you.",
    "I need some water.",
    "What do you do for work?"
]

# Spanish words
spanish_words = [
    "Casa", "Agua", "Amigo", "Libro", "Comida",
    "Amor", "Familia", "Perro", "Sol", "Feliz"
]

# Spanish phrases
spanish_phrases = [
    "¿Cómo te llamas?",  # What is your name?
    "¿Cómo estás hoy?",  # How are you today?
    "¿Dónde vives?",  # Where do you live?
    "Me gustaría un café, por favor.",  # I would like some coffee, please.
    "¿Puedes ayudarme?",  # Can you help me?
    "¿Qué hora es?",  # What time is it?
    "Estoy aprendiendo español.",  # I am learning Spanish.
    "Es un placer conocerte.",  # It’s nice to meet you.
    "Necesito un poco de agua.",  # I need some water.
    "¿A qué te dedicas?"  # What do you do for work?
]

# French words
french_words = [
    "Maison", "Eau", "Ami", "Livre", "Nourriture",
    "Amour", "Famille", "Chien", "Soleil", "Heureux"
]

# French phrases
french_phrases = [
    "Comment t'appelles-tu ?",  # What is your name?
    "Comment ça va aujourd'hui ?",  # How are you today?
    "Où habites-tu ?",  # Where do you live?
    "Je voudrais un café, s'il vous plaît.",  # I would like some coffee, please.
    "Peux-tu m'aider ?",  # Can you help me?
    "Quelle heure est-il ?",  # What time is it?
    "J'apprends le français.",  # I am learning French.
    "Enchanté de te rencontrer.",  # It’s nice to meet you.
    "J'ai besoin d'eau.",  # I need some water.
    "Que fais-tu dans la vie ?"  # What do you do for work?
]

practice_words = { "en": {"words": english_words,
                          "phrases": english_phrases},
                  "es":  {"words": spanish_words,
                          "phrases": spanish_phrases},
                  "fr":  {"words": french_words,
                          "phrases": french_phrases},
}

def practice_word(index=0, language='en'):
    return practice_words[language]['words'][index]

def practice_phrase(index=0, language='en'):
    return practice_words[language]['phrases'][index]
