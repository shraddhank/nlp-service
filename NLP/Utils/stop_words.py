# coding: utf8
from __future__ import unicode_literals              
from R88R.Core.Utilities import singleton
from R88R.Core.Logger import logger

@singleton
class StopWords(object):
    """
    a factory class supporting lazy_loading stop words    
    This is a stop gap until we better refactor language support   
    
    TODO - move to NLP.py?
    """
    _stops = {}
    
    def get_stops(self,lang):
        _stops = None
        if lang in self._stops:
            return  self._stops[lang]
            
        if lang == 'en':
            from spacy.lang.en.stop_words import STOP_WORDS as _stops_english
            _stops_english_extra = set("""
            PRON
            """)
            _stops_english.update(_stops_english_extra)
            self._stops[lang] = _stops_english
        elif lang == 'es':
            from spacy.lang.es.stop_words import STOP_WORDS as _stops_spanish
            self._stops[lang] = _stops_spanish
        elif lang == 'de':
            from spacy.lang.de.stop_words import STOP_WORDS as _stops_german
            self._stops[lang] = _stops_german
        elif lang == 'nl':
            from spacy.lang.nl.stop_words import STOP_WORDS as _stops_dutch
            self._stops[lang] =  _stops_dutch
        elif lang == 'it':
            from spacy.lang.it.stop_words import STOP_WORDS as _stops_italian
            self._stops[lang] = _stops_italian
        elif lang == 'fr':
            from spacy.lang.fr.stop_words import STOP_WORDS as _stops_french
            _stops_french_extra = set("""
                c' c’
                d' d’
                j' j’
                l' l’
                m' m’
                n' n’
                qu' qu’
                s' s’
                t' t’
                """)
            _stops_french.update(_stops_french_extra)
            self._stops[lang] = _stops_french
        elif lang == 'pt':
            from spacy.lang.pt.stop_words import STOP_WORDS as _stops_portuguese   
            self._stops[lang] = _stops_portuguese
        else:
            logger.error('no stopwords for language %s'%lang)
            self._stops[lang] = []
        return  self._stops[lang]
        
# used for bigrams

_bgstops = [
    '.',
    ',',
    '--',
    '\'s',
    '?',
    ')',
    '(',
    ':',
    '\'',
    '\'re',
    '"',
    '-',
    '}',
    '{',
    ]


            
    
    


