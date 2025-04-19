from PyDictionary import PyDictionary

dictionary = PyDictionary()

def get_meaning(word):
    meaning = dictionary.meaning(word)
    return meaning

# 示例
word = "apple"
meaning = get_meaning(word)
print(f"{word}: {meaning}")