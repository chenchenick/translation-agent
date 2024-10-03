import os
import json
from .parser import parse_srt
from .preprocessor import extract_texts, combine_texts, remove_overlaps
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
    
    combined_text = combine_texts(texts)
    save_step_result("3_combined_text", {"combined_text": combined_text}, output_dir)
    
    cleaned_text = remove_overlaps(texts)
    save_step_result("4_cleaned_text", {"cleaned_text": cleaned_text}, output_dir)
    
    print(f"Translating text...")
    translated_text = translate(
        source_lang=source_lang,
        target_lang=target_lang,
        source_text=cleaned_text,
        country=country,
    )
    save_step_result("5_translated_text", {"translated_text": translated_text}, output_dir)
    
    # Extract only the translation from the response
    translation_start = translated_text.find("<TRANSLATION>") + len("<TRANSLATION>")
    translation_end = translated_text.find("</TRANSLATION>")
    if translation_start != -1 and translation_end != -1:
        translated_text = translated_text[translation_start:translation_end].strip()
    
    aligned_captions = align_translations(captions, translated_text)
    save_step_result("6_aligned_captions", aligned_captions, output_dir)
    
    export_to_srt(aligned_captions, output_srt_path)
    print(f"Translation complete. Translated SRT saved to {output_srt_path}")
    print(f"Analysis files saved in {output_dir}")