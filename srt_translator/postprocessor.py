def align_translations(captions, translated_texts):
    aligned_captions = []
    for caption, translated_text in zip(captions, translated_texts):
        aligned_caption = caption.copy()
        aligned_caption['text'] = translated_text
        aligned_captions.append(aligned_caption)
    return aligned_captions