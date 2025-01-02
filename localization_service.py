translations = {
    "en": {"greeting": "Hello"},
    "es": {"greeting": "Hola"},
    "fr": {"greeting": "Bonjour"}
}

def get_localized_message(language, key):
    return translations.get(language, translations["en"]).get(key, "")

# Example Usage
message = get_localized_message("es", "greeting")
print(message)  # Outputs: Hola
