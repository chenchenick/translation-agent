import os
import json
from typing import List
from tqdm import tqdm
import xml.etree.ElementTree as ET
from .parser import parse_srt
from .preprocessor import extract_texts, remove_overlaps
from .postprocessor import align_translations
from .exporter import export_to_srt
from translation_agent.utils import translate_simple

def save_step_result(step_name, data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{step_name}.xml")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)
    print(f"Saved {step_name} result to {file_path}")

def translate_texts_in_batches(xml_str: str, source_lang: str, target_lang: str, country: str, batch_size: int = 20, output_dir: str = "") -> str:
    root = ET.fromstring(xml_str)
    translated_root = ET.Element("captions")
    
    log_file = os.path.join(output_dir, "batch_translations.json")
    batch_results = []

    captions = list(root)
    for i in tqdm(range(0, len(captions), batch_size), desc="Translating batches"):
        batch = captions[i:i+batch_size]
        
        batch_xml = ET.Element("captions")
        for caption in batch:
            batch_xml.append(caption)
        
        batch_xml_str = ET.tostring(batch_xml, encoding='unicode')
        
        batch_result = {
            "batch_number": i // batch_size + 1,
            "original_texts": batch_xml_str,
            "translated_texts": "",
            "warnings": []
        }

        translated_batch = translate_simple(
            source_lang=source_lang,
            target_lang=target_lang,
            source_text=batch_xml_str
        ).strip()  # Add .strip() here to remove any leading/trailing whitespace
        
        try:
            translated_batch_root = ET.fromstring(translated_batch)
            for translated_caption in translated_batch_root:
                translated_root.append(translated_caption)
            batch_result["translated_texts"] = translated_batch
        except ET.ParseError:
            warning = f"Warning: Unable to parse translated XML for batch {batch_result['batch_number']}"
            print(warning)
            batch_result["warnings"].append(warning)
            batch_result["translated_texts"] = translated_batch
        
        batch_results.append(batch_result)

    # Save batch results to file
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(batch_results, f, ensure_ascii=False, indent=2)
    print(f"Batch translation results saved to {log_file}")

    return ET.tostring(translated_root, encoding='unicode')

def translate_srt(input_srt_path, output_srt_path, source_lang, target_lang, country):
    output_dir = os.path.join(os.path.dirname(output_srt_path), "analysis")
    
    captions = parse_srt(input_srt_path)
    save_step_result("1_parsed_captions", json.dumps(captions, ensure_ascii=False, indent=2), output_dir)
    
    xml_str = extract_texts(captions)
    save_step_result("2_extracted_texts", xml_str, output_dir)
    
    print(f"Translating text...")
    translated_xml = translate_texts_in_batches(xml_str, source_lang, target_lang, country, output_dir=output_dir)
    save_step_result("3_translated_texts", translated_xml, output_dir)
    
    aligned_captions = align_translations(captions, translated_xml)
    save_step_result("4_aligned_captions", json.dumps(aligned_captions, ensure_ascii=False, indent=2), output_dir)
    
    export_to_srt(aligned_captions, output_srt_path)
    print(f"Translation complete. Translated SRT saved to {output_srt_path}")
    print(f"Analysis files saved in {output_dir}")