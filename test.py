from deep_translator import GoogleTranslator

def get_translation(word):
    try:
        translator = GoogleTranslator(source='en', target='zh-CN')  # 使用 zh-CN
        translation = translator.translate(word)
        return translation
    except Exception as e:
        print(f"Error: {e}")
        return "Translation failed"

# 示例
word = "apple"
meaning = get_translation(word)
print(f"{word}: {meaning}")