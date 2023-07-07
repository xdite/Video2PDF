import requests
import pysrt
import concurrent.futures
import os

# Your DeepL API key from the environment variable
api_key = os.getenv('DEEPL_API_KEY')

def translate_text(text, target_language='en'):
    base_url = 'https://api.deepl.com/v2/translate'
    payload = {
        'auth_key': api_key,
        'text': text,
        'target_lang': target_language,
    }
    response = requests.post(base_url, data=payload)
    if response.status_code != 200:
        raise Exception('DeepL request failed with status code {}'.format(response.status_code))
    translated_text = response.json()['translations'][0]['text']
    print(translate_text)
    return translated_text

def translate_srt_file(file_path, target_language='zh'):
    # Load the .srt file
    subs = pysrt.open(file_path)

    # Translate each subtitle
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_sub = {executor.submit(translate_text, sub.text, target_language): sub for sub in subs}
        for future in concurrent.futures.as_completed(future_to_sub):
            sub = future_to_sub[future]
            try:
                translated_text = future.result()
                sub.text = translated_text
            except Exception as exc:
                print('%r generated an exception: %s' % (sub, exc))

    # Save the translated .srt file
    subs.save(file_path.replace('.srt', '.zh.srt'), encoding='utf-8')

# Translate an .srt file to English
translate_srt_file('JaVBG7tFAU8_zh_Hans.srt', 'zh')
