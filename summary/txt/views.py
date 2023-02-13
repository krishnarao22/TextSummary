from django.shortcuts import render

# Create your views here.

import json
from django.contrib.auth.models import User #####
from django.http import JsonResponse , HttpResponse ####

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download('stopwords')
nltk.download('punkt')

def index(request):
    return HttpResponse("Hello, world. You're at the wiki index.")


# # https://pypi.org/project/wikipedia/#description
# def get_wiki_summary(request):
#     # topic = request.GET.get('topic', None)

#     # print('topic:', topic)

#     # data = {
#     #     'summary': wikipedia.summary(topic, sentences=1),
#     #     'raw': 'Successful',
#     # }

#     # print('json-data to be sent: ', data)

#     return JsonResponse(data)


def get_summary(request):
    text = request.GET.get('text', None)

    print('text:', text)

    data = {
        'summary': summarize(text),
        'raw': 'Successful',
    }

    print('json-data to be sent: ', data)

    return JsonResponse(data)

def summarize(text):

    print('SUMMARIZE CALLED WITH TEXT: ', text)
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)
    
    word_freq_table = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in word_freq_table:
            word_freq_table[word] += 1
        else:
            word_freq_table[word] = 1
    
    sentences = sent_tokenize(text)
    numSentences = 0
    sentenceValue = dict()
    
    for sentence in sentences:
        numSentences += 1
        for word in word_freq_table:
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += word_freq_table[word]
                else:
                    sentenceValue[sentence] = word_freq_table[word]
    
    sentence_value_sum = 0
    for sentence, value in sentenceValue.items():
        sentence_value_sum += value
    
    # Average value of a sentence from the original text
    
    avg_sentence_value = int(sentence_value_sum / numSentences)
    
    # Storing sentences into our summary.
    summary = ''
    for sentence in sentences:
        if sentence in sentenceValue and sentenceValue[sentence] > (1.2 * avg_sentence_value):
            summary += " " + sentence
    print(summary)
    return summary