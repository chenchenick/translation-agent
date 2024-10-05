import os
from typing import List, Tuple
from icecream import ic
from tqdm import tqdm
from translate import translate_text
from srt_utils import parse_srt, write_srt

def translate_srt(input_file: str, output_file: str, source_lang: str, target_lang: str, country: str):
    # Parse the input SRT file
    subtitles = parse_srt(input_file)
    
    # Extract text from subtitles
    texts = [sub.content for sub in subtitles]
    
    # Translate texts in batches
    translated_texts = translate_texts_in_batches(texts, source_lang, target_lang, country)
    
    # Update subtitle contents with translated text
    for sub, translated_text in zip(subtitles, translated_texts):
        sub.content = translated_text
    
    # Write the translated subtitles to the output file
    write_srt(subtitles, output_file)
    
    print(f"Translation complete. Translated SRT saved to {output_file}")

def translate_texts_in_batches(texts: List[str], source_lang: str, target_lang: str, country: str, batch_size: int = 10) -> List[str]:
    translated_texts = []
    cache = {}
    
    for i in tqdm(range(0, len(texts), batch_size), desc="Translating batches"):
        batch = texts[i:i+batch_size]
        batch_to_translate = [text for text in batch if text not in cache]
        
        if batch_to_translate:
            translated_batch = translate_text("\n".join(batch_to_translate), source_lang, target_lang, country)
            translated_lines = translated_batch.split("\n")
            
            for original, translated in zip(batch_to_translate, translated_lines):
                cache[original] = translated
        
        translated_texts.extend([cache[text] for text in batch])
    
    return translated_texts