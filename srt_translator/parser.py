import re

def parse_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> '
                         r'(\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\Z)', re.DOTALL)
    subtitles = pattern.findall(content)

    captions = []
    for subtitle in subtitles:
        captions.append({
            'sequence': int(subtitle[0]),
            'start': subtitle[1],
            'end': subtitle[2],
            'text': subtitle[3].strip().replace('\n', ' ')
        })
    return captions