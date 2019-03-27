# coding: utf8
from __future__ import unicode_literals

"""

Class wrappers for library-agnostic NLP handling

Base_Nlp class - handles tokenization, stops initially
Language class - Factory, provides Language instance on demand

- all imports done once and only once on demand
- first version supports stops and tokenization
- uses nltk for en
- else uses spacy

TODO later:
- named entities
- POS tagging etc
- clean up text normalization mess
- look into additional NLTL languages

"""

# from R88R.Core.Logger import logger


class BaseNLP(object):

  def __init__(self, language, **kwargs):
    self._lang = language
    self._nlp = None
    self._stops = None
    # self.log = logger.getSubLogger(self._lang)

  def __repr__(self):
    return '_'.join((str(self._lang), 'NLP'))

  @property
  def language(self):
    return self._lang

  @property
  def stops(self):
    if self._stops is None:
      from NLP.Utils.stop_words import StopWords
      self._stops = StopWords().get_stops(self.language)
    return self._stops

  def sentence_tokenize(self, text):
    """ sentence tokenize"""
    return []


class SpacyNLP(BaseNLP):
  """ after instantition, this is language_specific
  """

  def __init__(self, language, **kwargs):
    super(SpacyNLP, self).__init__(language, **kwargs)

  @property
  def nlp(self):
    """ copies and encapsulates code from spacey_tokenization.py"""
    if self._nlp is None:
      if self._lang == 'en':
        import en_core_web_sm as lang
      elif self._lang == 'de':
        import de_core_news_sm as lang
      elif self._lang == 'es':
        import es_core_news_sm as lang
      elif self._lang == 'pt':
        import pt_core_news_sm as lang
      elif self._lang == 'fr':
        import fr_core_news_sm as lang
      elif self._lang == 'it':
        import it_core_news_sm as lang
      elif self._lang == 'nl':
        import nl_core_news_sm as lang
      else:
        # TODO - add 'any' support
        self.log.error('unsupported language %s' % self._lang)
        return None

      self._nlp = lang.load(disable=['parser', 'tagger', 'ner', 'vector', 'entity'])
      if len(self._nlp.pipe_names) > 0 and 'sbd' in self._nlp.pipe_names:
        pass
      else:
        self._nlp.add_pipe(self._nlp.create_pipe('sentencizer'))
    return self._nlp

  def sentence_tokenize(self, text):
    doc = self.nlp(text.encode("utf-8").decode("utf-8"))
    return doc.sents


class NLTKNLP(BaseNLP):

  def __init__(self, language, **kwargs):
    super(NLTKNLP, self).__init__(language, **kwargs)
    self._tokenizer = None

  @property
  def tokenizer(self):
    if self._tokenizer is None:
      from nltk.tokenize import sent_tokenize
      self._tokenizer = sent_tokenize
    return self._tokenizer

  def sentence_tokenize(self, text):
    return self.tokenizer(text)


class NLP(object):
  """
  Factory for managing and instantiating NLP instances
  Since only classmethods used, no singleton needed
  can handle different libraries
  """
  _nlps = {}
  # log = logger.getSubLogger('NLP')
  _supported_languages = ['en', 'de', 'es', 'pt', 'fr', 'it', 'nl']

  @classmethod
  def nlp(_cls, language):
    if not language in NLP._supported_languages:
      NLP.log.error('language %s not supported' % language)
    if not language in NLP._nlps:
      _nlp = NLP.load_nlp(language)
      if _nlp is None:
        NLP.log.error('language %s  could not be loaded' % language)
        return None
      NLP._nlps[language] = _nlp
    return NLP._nlps[language]

  @classmethod
  def load_nlp(_cls, language):
    return SpacyNLP(language)  # until we un dertsand NLTK lemmatization
    if language == 'en':
      return NLTKNLP('en')
    else:
      return SpacyNLP(language)
    return None



