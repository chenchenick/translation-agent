import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from srt_translator import translate_srt

if __name__ == "__main__":
    source_lang, target_lang, country = "English", "Chinese", "China"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_srt = os.path.join(script_dir, "sample-texts", "sample.en.srt")
    output_srt = os.path.join(script_dir, "translations", f"chinese_sample.en.srt")
    
    # Ensure the translations directory exists
    os.makedirs(os.path.dirname(output_srt), exist_ok=True)
    
    translate_srt(input_srt, output_srt, source_lang, target_lang, country)
