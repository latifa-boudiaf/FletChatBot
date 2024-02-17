import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


lemmatizer = nltk.WordNetLemmatizer()

def lemmatize_input(input_string):
    lemmatized_words = []
    for word in word_tokenize(input_string):
        # Get the base form of the word (lemma)
        lemma = lemmatizer.lemmatize(word)
        lemmatized_words.append(lemma)
        
        # Add synonyms to the list
        synonyms = [synonym for syn in wordnet.synsets(word) for synonym in syn.lemma_names()]
        lemmatized_words.extend(synonyms)

    return lemmatized_words

def calculate_jaccard_similarity(list1, list2, min_similarity_threshold=0.4):
    set1 = set(list1)
    set2 = set(list2)

    intersection_size = len(set1.intersection(set2))
    union_size = len(set1) + len(set2) - intersection_size

    if union_size == 0:
        return 0

    similarity = intersection_size / union_size

    # If the input is short, apply a minimum similarity threshold
    if len(set1) < 3:
        similarity = max(similarity, min_similarity_threshold)

    return similarity

def enhance_required_words_matching(user_input, required_words):
    lemmatized_input = lemmatize_input(user_input)
    matching_scores = []

    for required_word in required_words:
        score = calculate_jaccard_similarity(lemmatized_input, [required_word])
        matching_scores.append(score)

    return max(matching_scores, default=0)
