def export_to_srt(aligned_captions, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for caption in aligned_captions:
            file.write(f"{caption['sequence']}\n")
            file.write(f"{caption['start']} --> {caption['end']}\n")
            file.write(f"{caption['text']}\n\n")