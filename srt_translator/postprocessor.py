import xml.etree.ElementTree as ET

def align_translations(captions, translated_xml):
    aligned_captions = []
    translated_root = ET.fromstring(translated_xml)
    
    for caption, translated_caption in zip(captions, translated_root.findall('caption')):
        aligned_caption = caption.copy()
        translated_text = translated_caption.find('text').text
        aligned_caption['text'] = translated_text
        aligned_captions.append(aligned_caption)
    
    return aligned_captions