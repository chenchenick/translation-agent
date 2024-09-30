import webvtt
import os
import re

def vtt_to_srt(vtt_file_path, srt_file_path):
    """
    Convert a VTT file to SRT format.

    Args:
        vtt_file_path (str): Path to the input VTT file.
        srt_file_path (str): Path to the output SRT file.
    """
    try:
        with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
            for i, caption in enumerate(webvtt.read(vtt_file_path), start=1):
                # Write subtitle number
                srt_file.write(f"{i}\n")
                
                # Convert and write timestamp
                start = convert_to_srt_time(caption.start)
                end = convert_to_srt_time(caption.end)
                srt_file.write(f"{start} --> {end}\n")
                
                # Write text content
                srt_file.write(f"{caption.text}\n\n")
        
        print(f"Conversion complete. SRT file saved as: {srt_file_path}")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

def convert_to_srt_time(vtt_time):
    """
    Convert VTT timestamp to SRT timestamp format.

    Args:
        vtt_time (str): VTT format timestamp.

    Returns:
        str: SRT format timestamp.
    """
    # VTT format: HH:MM:SS.mmm
    # SRT format: HH:MM:SS,mmm
    return vtt_time.replace('.', ',')

if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Specify the name of your VTT file
    vtt_file_name = "sample.en.vtt"  # Replace with your actual VTT file name
    
    # Construct the full path to the VTT file
    vtt_file_path = os.path.join(script_dir, "sample-texts", vtt_file_name)
    
    # Construct the output SRT file path
    srt_file_name = os.path.splitext(vtt_file_name)[0] + ".srt"
    srt_file_path = os.path.join(script_dir, "sample-texts", srt_file_name)
    
    # Check if the VTT file exists
    if os.path.exists(vtt_file_path):
        vtt_to_srt(vtt_file_path, srt_file_path)
    else:
        print(f"VTT file not found: {vtt_file_path}")
