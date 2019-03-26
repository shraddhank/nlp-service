import re

# from R88R.Core.Logger import logger
from NLP.Utils.utilities import descape
from NLP.Utils.stop_words import StopWords

def splitGeneric(s):
    """splits on comma or whitespace"""
    W = Words()
    return W.splitGeneric(s)

class Words:
    _stops = StopWords()
    _punctuation = '!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~'  # string.puctuation minus apostrophe
    _bg_stops = None


    @staticmethod
    def specialCharsMapper():
        return {' ': 'S', '(': 'C', '#':'H', ')': 'D', '*':'X', '|': 'I', '"': 'QQ', "'": 'SQ', '-':'E', '+': 'T'}

    @staticmethod
    def getStops(language='en'):
        ''' return set of stopwords '''
        return Words._stops.get_stops(language)

    @staticmethod
    def getBigramStops(language='en'):
        ''' return set of stopwords '''
        if Words._bg_stops == None:
            from NLP.Utils.stop_words import _bgstops
            stops = Words.getStops(language=language)
            Words._bg_stops = stops.union(set(_bgstops))
        return Words._bg_stops

    @staticmethod
    def splitGeneric(s):
        """splits on comma or whitespace"""
        s = s.replace(',',' ')
        s = re.sub("\s+", ' ', s).strip()
        return s.split(' ')

    @staticmethod
    def bigrams(words):
        """generator of bigrams from tokenized text"""
        wprev = words[0]
        for w in words[1:]:
            yield (' '.join((wprev,w)))
            wprev = w

    @staticmethod
    def bigramsX(words):
        """generator of bigrams from tokenized text"""
        stops = Words.getBigramStops()
        wprev = words[0]
        for w in words[1:]:
            if w not in stops and wprev  not in stops:
                yield (' '.join((wprev,w)))
            wprev = w

    @staticmethod
    def normalizeText(s,thresh = 0, toReplace="[\.\t\,\:;\(\)\.]", replacement="",remove_stops=True, lower = True, language='en'):
        """ takes a string s, thresh is min word size, returns list of words
        brad added replacement params for more flexibility, defaults to what it always was"""
        stops = Words.getStops(language=language)
        if lower:
            s = s.lower()   # MNT - this already done upstream
        s = re.sub(toReplace, replacement, s, 0,)
        words = s.split()
        norm = []
        for word in words:
            punc = Words._punctuation
            if word[0] in '@ #'.split(): # leave _ in @refs and hashtags
                punc = punc.replace('_','')

            word = ''.join([c for c in word if c not in punc]) #strip  out punctation

            if remove_stops and word in stops:          # remove stop words
                continue
            try:                            # remove numbers
                f = float(word)
                continue
            except:
                pass
            if len(word)>thresh:
                norm.append(word)
        return norm

    @staticmethod
    def normalizeTextNew(s, replacement=" ", blacklist = 'http www'.split(), removeUrls=True, removeRefs=False, replaceAccents=True, verbose=False,remove_stops=True, lower = True,split=True, language='en'):
        """these are brad's improvements to include other special char replacements, and to be able to replace with space instead of collapse
        descape replaces html entities with their unicode equivalents e.g. &aacute;
        replaceAccents then replaces accented with unaccented, whether it was there before descape or after"""
        if removeUrls:
            s = re.sub(r'\b((https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]*[-A-Za-z0-9+&@#/%=~_|])', '', s)

        if removeRefs:
            s = re.sub(r'@\w*', '', s) # (?i)(\bRT\s?)?

        s = s.replace('&amp;', 'and')
        s = s.replace('&nbsp;', ' ')

        before = s
        try:
            s = descape(s, accents=True) # replace html entities
        except Exception as error:
            print('failed changing html entities %s\n%s'%(re.compile(r'&\w*;').findall(s), s))
            s = re.sub(r'&(\w*);', ' \g<1> ', s)
            print('s = %s'%(s))
        before = s

        if replaceAccents:
            s = Words.replaceAccents(s)

        s = ''.join([c if ord(c) < 128 else replacement for c in s ]) # get rid of wacky chars, including quotes

        s = re.sub("\s+", ' ', s)
        s = re.sub("'", '', s)
        # s = re.sub(r'[' + Words._punctuation + ']', ' ', s)
        normed = [x for x in Words.normalizeText(s, toReplace="[\.\t\,\:;\(\)\.\'\"\-]", replacement=" ",remove_stops=remove_stops, lower = lower, language=language) if x not in blacklist]
        if not split:
            normed  = ' '.join(normed)
        return normed


    @staticmethod
    def replaceAccents(s):
        """replaces diacritical characters with the closest unaccented version, eg. s[o accented]cio with socio
        from http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string """
        import unicodedata
        try:
            if type(s) == type(u' '):
                s = ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
        except Exception as error:
            print(error)
        return s


    # word histograms default to dictionaries: {'word1':count1,'word2':count2...}

    @staticmethod
    def generate_histogram(w,norm = False):
        '''w is an array of words as returned by normalizeText'''
        W = {}
        for word in w:
            W.setdefault(word,0)
            W[word] += 1
        if norm:
            return normalize_histogram(W)
        return W

    @staticmethod
    def from_array(w, norm = False):
        '''w is an array of word,count as serialized'''
        W = dict(w)
        if norm:
            return Words.normalize_histogram(W)
        return W

    @staticmethod
    def extend_histogram(W,w,weight = 1.0):
        '''extend one histogram by another'''
        if type(w) == type([]):
            w = dict(w)
        for word,count in w.items():
            W.setdefault(word,0)
            W[word] += count * weight

    @staticmethod
    def normalize_histogram(W,copy = False):
        ''' given histogram,normalize => tf/idf'''
        w_count = float(sum(W.values()))
        if copy:
            X = {}
        else:
            X = W
        for word,count in W.items():
            X[word] = float(count)/w_count
        return X

    @staticmethod
    def rank_histogram(W,copy = False,readable = False,top = None,thresh = None):
        ''' given histogram,ranks and return sorted array'''
        R = sorted(W.items(),key = lambda x: x[1],reverse = True)
        if thresh is not None:
            R = [[k,v] for k,v in R if v >=thresh]
        if readable and len(R)>0:
            x = float(R[0][1])
            if x >0:
                R = [[r[0],int((1000 * r[1])/x)] for r in R]
        if top is not None:
            R = R[:top]
        return R

    @staticmethod
    def truncate_histogram(W,thresh = 1,sort = True):
        ''' truncates words with count < thresh'''
        R = [[word,count] for word,count in W.items() if count > thresh]
        if sort:
            R = sorted(R,key = lambda x: x[1],reverse = True)
        return R

    @staticmethod
    def suppress(w,W):
        '''suppress common terms - in w by subtracting W - both assumed normalized'''
        for word in w.keys():
            if word in W:
                if w[word]>W[word]:
                    w[word] -= W[word]
                else:
                    w.pop(word)
        return Words.normalize_histogram(w)

    @staticmethod
    def wordHist(W,w):
        for x in w:
            W.setdefault(x,0)
            W[x] += 1

    @staticmethod
    def replaceWeird(strng, others={}):
        before = strng
        rex = re.compile(r'\s+')
        strng = rex.sub(" ", strng)
        replace = {
            u'\xae': '&reg;',
            r'\xe2\x80\x99': "'",
            r'\xa0': ' ',
            r'\xb7': '*',
            u'\u25aa': '*',
            u'\u2009': " ",
            u'\u2013': "-",
            u'\u2014': "-",
            u'\u2018': "'",
            u'\u2019': "'",
            u'\u201c': "'",
            u'\u201d': "'",
            u'\u2026': "...",
            u'\n': " ",
            u'\r': " ",
            u'\t': " "
            }
        replace.update(others)
        try:
            for weird, replacement in replace.items():
                strng = re.sub(weird, replacement, strng)
            if before != strng:
                pass # print "REPLACED: ", before, '\n', strng
        except Exception as error:
            print(error)
        return strng

    @staticmethod
    def indexableLatLong(val):
        """converts latitude longitude strings into a list of shorter versions that can be indexed
        also does zipcode"""
        # test for two decimal formatted strings separated by whitespace and/or ,
        test = re.compile(r'\-*[0-9]{1,3}\.[0-9]+[\s,]+\-*[0-9]{1,3}\.[0-9]+\b')
        words = []
        if test.findall(val):
            latlong = re.compile('\-{0,1}[0-9]{1,3}\.[0-9]{1,3}') # precision 3 decimals
            words.extend(latlong.findall(val))
            latlong = re.compile('\-{0,1}[0-9]{1,3}\.[0-9]{1,2}') # precision 2 decimals
            words.extend(latlong.findall(val))
            latlong = re.compile('\-{0,1}[0-9]{1,3}\.[0-9]') # precision 1 decimals
            words.extend(latlong.findall(val))
            latlong = re.compile('(\-{0,1}[0-9]{1,3})\.') # precision degrees
            words.extend(latlong.findall(val))
            zipcode = re.compile(r'[\s,]+([0-9]{5})[\s,]+') # zipcode
            it = zipcode.findall(val)
            words.extend(it)

        return list(set(words))

    @staticmethod
    def normalizeSearchQuery(query):
        """converts an arbitrary Elastic Search query to deterministic, reversible, alphanumeric string for file naming
        NB: assumes query is case-insensitive, uses Uppercase for special characters"""
        mapper = Words.specialCharsMapper()
        qry = query.lower()
        for before, after in mapper.items():
            qry = qry.replace(before,after)
        return qry

    @staticmethod
    def denormalizeSearchQuery(normed):
        """inverts normalizeSearchQuery"""
        mapper = Words.specialCharsMapper()
        nrm = normed
        for before, after in mapper.items():
            nrm = nrm.replace(after,before)
        return nrm

    @staticmethod
    def isEnglish(text):
        """tests if all the words in the text are english, including stemming"""
        from nltk.corpus import words as wds
        words = wds.words()
        from nltk.stem import WordNetLemmatizer
        wnl = WordNetLemmatizer()
        import re
        t = re.sub('\s+', ' ', text.replace('-', ' ')).strip().lower()
        parts = t.split(' ')
        out = []
        english = []
        for part in parts:
            triplet = [part, wnl.lemmatize(part, 'n'), wnl.lemmatize(part, 'v')]
            out.append(triplet)
            english.append([q in words for q in triplet])
        return all([any(triplet) for triplet in english]), out, english

if __name__ == '__main__':
    #print Words.getStops()
    print(Words.normalizeText('Now is the time for all good frogs to jump in a 7 ponds'))
