import webvtt
import os
import re

def strip_tags(text):
    """
    Remove HTML-like tags from the text.
    
    Args:
        text (str): The text containing tags.
    
    Returns:
        str: The text with tags removed.
    """
    return re.sub(r'<[^>]+>', '', text)

def read_and_print_vtt(file_path):
    """
    Read a VTT file and print each cue, handling tags in the text content.

    Args:
        file_path (str): Path to the VTT file.
    """
    try:
        for caption in webvtt.read(file_path):
            print(f"Start: {caption.start}")
            print(f"End: {caption.end}")
            print(f"Text (with tags): {caption.text}")
            print(f"Text (without tags): {strip_tags(caption.text)}")
            print("---")
    except Exception as e:
        print(f"An error occurred while reading the VTT file: {e}")

if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Specify the name of your VTT file
    vtt_file_name = "sample-texts/sample.en.vtt"  # Replace with your actual VTT file name
    
    # Construct the full path to the VTT file
    vtt_file_path = os.path.join(script_dir, vtt_file_name)
    
    # Check if the file exists
    if os.path.exists(vtt_file_path):
        read_and_print_vtt(vtt_file_path)
    else:
        print(f"VTT file not found: {vtt_file_path}")