from translation_agent import translate

def translate_chunks(chunks, source_lang, target_lang, country):
    translated_chunks = []
    for chunk in chunks:
        translated_text = translate(
            source_lang=source_lang,
            target_lang=target_lang,
            source_text=chunk,
            country=country,
        )
        translated_chunks.append(translated_text.strip())
    return translated_chunks