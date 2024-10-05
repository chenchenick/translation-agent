import nltk
import ssl
import xml.etree.ElementTree as ET
from xml.dom import minidom

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)

download_nltk_data()

def extract_texts(captions):
    root = ET.Element("captions")
    for caption in captions:
        caption_elem = ET.SubElement(root, "caption")
        sequence_elem = ET.SubElement(caption_elem, "sequence")
        sequence_elem.text = str(caption['sequence'])
        text_elem = ET.SubElement(caption_elem, "text")
        text_elem.text = caption['text']
    
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    return xml_str

# The rest of the functions remain unchanged
def combine_texts(texts):
    return ' '.join(texts)

def remove_overlaps(texts):
    cleaned_texts = [texts[0]]
    for i in range(1, len(texts)):
        prev_text = cleaned_texts[-1]
        curr_text = texts[i]
        overlap = find_overlap(prev_text, curr_text)
        if overlap:
            curr_text = curr_text[len(overlap):].lstrip()
        cleaned_texts.append(curr_text)
    return ' '.join(cleaned_texts)

def find_overlap(a, b):
    min_length = min(len(a), len(b))
    for i in range(min_length, 0, -1):
        if a[-i:] == b[:i]:
            return a[-i:]
    return ''

def segment_text(combined_text, max_chunk_size):
    sentences = nltk.tokenize.sent_tokenize(combined_text)
    chunks = []
    current_chunk = ''
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += ' ' + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks