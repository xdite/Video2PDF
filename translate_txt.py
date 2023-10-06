import requests
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import sys
# Your DeepL API key from the environment variable
api_key = os.getenv('DEEPL_API_KEY')

def translate_text(args):
    text, target_language = args
    text = text.replace("\h", " ")
    base_url = 'https://api.deepl.com/v2/translate'
    payload = {
        'auth_key': api_key,
        'text': text,
        'target_lang': target_language,
    }
    response = requests.post(base_url, data=payload)
    if response.status_code != 200:
        print(f'DeepL request failed with status code {response.status_code} for text: {text}')
        return text
    translated_text = response.json()['translations'][0]['text']
    return translated_text

def parallel_translation(file_path, target_language='zh', num_workers=5):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    sentences = content.split('.')
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        translated_sentences = list(tqdm(executor.map(translate_text, [(sentence, target_language) for sentence in sentences]), total=len(sentences)))

    translated_text = '\n'.join(translated_sentences)
    with open('translated_'+file_path, 'w', encoding='utf-8') as file:
        print(translated_text)
        file.write(translated_text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} filename")
        sys.exit(1)

    parallel_translation(sys.argv[1])
