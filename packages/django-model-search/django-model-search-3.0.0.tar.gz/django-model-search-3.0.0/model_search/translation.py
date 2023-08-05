
from modeltranslation.translator import translator

from model_search.models import SearchTag


translator.register(SearchTag, fields=['text'])
