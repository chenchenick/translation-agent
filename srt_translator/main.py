from .parser import parse_srt
from .preprocessor import extract_texts, combine_texts, remove_overlaps, segment_text
from .translator import translate_chunks
from .postprocessor import align_translations
from .exporter import export_to_srt

def translate_srt(input_srt_path, output_srt_path, source_lang, target_lang, country):
    captions = parse_srt(input_srt_path)
    texts = extract_texts(captions)
    combined_text = combine_texts(texts)
    cleaned_text = remove_overlaps(texts)
    max_chunk_size = 2000  # Adjust based on LLM's token limit
    chunks = segment_text(cleaned_text, max_chunk_size)
    translated_chunks = translate_chunks(chunks, source_lang, target_lang, country)
    translated_text = ' '.join(translated_chunks)
    aligned_captions = align_translations(captions, translated_text)
    export_to_srt(aligned_captions, output_srt_path)
    print(f"Translation complete. Translated SRT saved to {output_srt_path}")