from nltk.corpus import wordnet
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')  # For additional word relationships
def get_synonyms_antonyms(word):
    synonyms = set()
    antonyms = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
            if lemma.antonyms():
                for ant in lemma.antonyms():
                    antonyms.add(ant.name())
    return synonyms, antonyms
word = "happy"
synonyms, antonyms = get_synonyms_antonyms(word)
print(f"Synonyms of '{word}':", synonyms)
print(f"Antonyms of '{word}':", antonyms)
