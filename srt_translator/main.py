import os
import json
from .parser import parse_srt
from .preprocessor import extract_texts, remove_overlaps
from .postprocessor import align_translations
from .exporter import export_to_srt
from translation_agent import translate

def save_step_result(step_name, data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{step_name}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {step_name} result to {file_path}")

def translate_srt(input_srt_path, output_srt_path, source_lang, target_lang, country):
    output_dir = os.path.join(os.path.dirname(output_srt_path), "analysis")
    
    captions = parse_srt(input_srt_path)
    save_step_result("1_parsed_captions", captions, output_dir)
    
    texts = extract_texts(captions)
    save_step_result("2_extracted_texts", texts, output_dir)
    
    # Remove the combine_texts step
    
    print(f"Translating text...")
    translated_texts = []
    for text in texts:
        translated_text = translate(
            source_lang=source_lang,
            target_lang=target_lang,
            source_text=text,
            country=country,
        )
        # Extract only the translation from the response
        translation_start = translated_text.find("<TRANSLATION>") + len("<TRANSLATION>")
        translation_end = translated_text.find("</TRANSLATION>")
        if translation_start != -1 and translation_end != -1:
            translated_text = translated_text[translation_start:translation_end].strip()
        translated_texts.append(translated_text)
    
    save_step_result("3_translated_texts", translated_texts, output_dir)
    
    aligned_captions = align_translations(captions, translated_texts)
    save_step_result("4_aligned_captions", aligned_captions, output_dir)
    
    export_to_srt(aligned_captions, output_srt_path)
    print(f"Translation complete. Translated SRT saved to {output_srt_path}")
    print(f"Analysis files saved in {output_dir}")