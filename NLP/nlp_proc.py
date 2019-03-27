import sys, traceback

from NLP.Utils.TextUtilities import fix_bad_unicode_textacy as fix_bad_unicode
from NLP.Utils.Words import Words
from NLP.Utils.text_normalization import plain_text_abstract



class NlpProc():

    def __init__(self):
        self._nlp = None

    @property
    def nlp(self):
        if self._nlp is None:
            from NLP.nlp import NLP
            self._nlp = NLP.nlp(self.language)
            assert self.nlp is not None
        return self._nlp

    def get_language_from_object(self, odata):
        """ Gets language from given mongo object of content
            If not found, returns language as 'en'
        Args:
            odata: mongo object of content

        Returns: language from mongo object

        """
        try:
            if odata.get('lxp', {}).get('language', None):
                language = odata['lxp']['language']
            elif odata.get('meta', {}).get('ecl', {}).get('lang', None):
                language = odata['meta']['ecl']['lang']
            else:
                language = 'en'
        except (AttributeError, KeyError):
            print("Exception getting language")
            language = 'en'

        return language

    def _tokenize(self, text, language, stemming=False,remove_stops=True,split=True,lemmatize=True):
        """ refactored to preserve tokenized sentences
        Test case fail L'objectif de l'ex GDF-Suez est de 2.200 MWc installÃ©s Ã  l'horizon 2021.
        """
        special = {'fr': 'dans y'.split(' ')}  # why not add to fr stops?
        spec = special.get(language, [])
        text = fix_bad_unicode(text.encode("utf-8").decode("utf-8"))
        sentences = self.nlp.sentence_tokenize(text.lower())
        cleaned_sentences = []

        for sentence in sentences:

            if lemmatize:
                lookup = dict([[x.text.lower(), x.lemma_] for x in sentence if
                               x.text.lower() not in spec])  # fixes L'
                lemmatized_text = ' '.join(
                    [lookup.get(x.text.lower(), x.text.lower()) for x in sentence if not (x.is_space or x.is_punct)])
            else:
                lemmatized_text = ' '.join([x.text.lower() for x in sentence if not (x.is_space or x.is_punct)])
            normed = (Words.normalizeTextNew(lemmatized_text, removeRefs=False, remove_stops=remove_stops, lower=False,
                                             split=split, language=language))
            cleaned_sentences.append(normed)
        if stemming:
            cleaned_sentences = [self.stemmer(language=language).stemWords(sentence) for sentence in cleaned_sentences]

        return cleaned_sentences  # backwards compatability

    def perform_nlp(self, oid, odata, stemming=False, named_entities=False,
                          remove_stops=True, lemmatize = True):
        """ """
        try:
            item = {}
            text = odata.get('excerpt') or odata.get('lxp', {}).get('description')

            #get content language
            language = self.get_language_from_object(odata)

            if not text:
                self.log.error('no excerpt for %s, keys %s' % (oid))
                return None
            plain_text = plain_text_abstract(text)
            item['sentences'] = self._tokenize(plain_text, language=language, stemming=stemming, item=item,
                                               remove_stops=remove_stops, lower=True, split=True,lemmatize = lemmatize)

            if named_entities:
                """ generates list of entities for each type"""
                try:
                    ent_kinds = ['PERSON', 'ORG','WORK_OF_ART', 'PRODUCT','EVENT']
                    entities = {}
                    text = str(plain_text)
                    doc = self.nlp(text) or []
                    for ent in doc.ents:
                        if ent.label_ in ent_kinds:
                            ne = ent.text.replace('\n','')
                            ents = entities.setdefault(ent.label_, [])
                            ents.append(ne)
                    item['ents'] = entities

                except Exception as error:
                    self.log.error('>>>entity_exception %s',error)
                    return None
        except Exception as error:
            self.log.error(error)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.log.error('TRACE %s' % (repr(traceback.format_tb(exc_traceback))))
            return None
        return oid, item
