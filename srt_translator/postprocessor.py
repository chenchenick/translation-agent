def align_translations(captions, translated_text):
    total_original_length = sum(len(caption['text']) for caption in captions)
    translated_text_length = len(translated_text)
    aligned_captions = []
    current_index = 0

    for caption in captions:
        original_length = len(caption['text'])
        proportion = original_length / total_original_length
        translated_length = int(proportion * translated_text_length)
        translated_segment = translated_text[current_index:current_index + translated_length]
        # Adjust to the nearest space to avoid cutting words
        next_space = translated_text.find(' ', current_index + translated_length)
        if next_space != -1:
            translated_segment = translated_text[current_index:next_space]
            current_index = next_space + 1
        else:
            current_index = translated_text_length

        aligned_captions.append({
            'sequence': caption['sequence'],
            'start': caption['start'],
            'end': caption['end'],
            'text': translated_segment.strip()
        })
    return aligned_captions