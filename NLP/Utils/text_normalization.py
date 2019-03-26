import re
from lxml.html import fromstring
from NLP.Utils.BeautifulSoup import BeautifulSoup


def fix_fake_unicode(s):
    """
    Fix unicode in string
    :param s:
    :return:
    """
    def convert(s):
        try:
            return s.group(0).encode('latin1').decode('utf8')
        except:
            return s.group(0)

    return re.sub(r'[\x80-\xFF]+', convert, s)


def newlines_from_p_tags(excerpt):
    """
    Removes <p> and replaces with \n\n

    :param excerpt: Content item description
    :return: excerpt
    """
    excerpt = re.sub('&#13;', r'\n', excerpt)
    opens = re.compile('<p>').findall(excerpt)
    opens.extend(re.compile('<p\s+.*?>').findall(excerpt))
    closes = re.compile('</p>').findall(excerpt)
    if len(opens) != len(closes):
        print('excerpt has mismatched <p> tags %s opens %s closes' % (len(opens), len(closes)))

    # remove opens
    exc = re.sub('<p>', '', excerpt)
    exc = re.sub('<p\s+.*?>', '', exc)
    exc = re.sub('<li>', '', exc)
    exc = re.sub('<li\s+.*?>', '', exc)

    # replace closes
    exc = re.sub('</p>', r'\n\n', exc)
    exc = re.sub('</li>', r'\n', exc)
    exc = re.sub('</br>', r'\n', exc)
    exc = re.sub('<br/>', r'\n', exc)

    return exc.strip()


def plain_text_abstract(excerpt, max_words=None):
    """
    Return plain text version of given html abstract

    :param excerpt: Content item description
    :param max_words:
    :return: normalized text
    """

    abstract = newlines_from_p_tags(excerpt)
    m = re.compile('&#160;|&nbsp;')

    # abstract.replace(r'&#13;', r' ')
    temp = m.sub(' ', abstract)
    m = re.compile('&#13;')

    # force spaces between links so they don't merge
    temp = re.sub('</a><a', '</a> <a', temp)

    temp = m.sub(r'\n', temp)
    lines = re.compile(r'\s*\n\s*\n\s*')

    # temp.replace(r'\n\n', 'qzqqq') # preserve double newlines (paragraphs)
    temp = lines.sub('qzqqq', temp)

    # collapse whitespace
    m = re.compile(r'\s+')
    temp = m.sub(' ', temp)

    # replace paragraphs with one
    m = re.compile('(qzqqq)+')
    temp = m.sub(r'\n\n', temp)


    try:
        tree = fromstring(temp)
        result = tree.text_content()
    except Exception as x:
        try:
            text = ''.join(BeautifulSoup(abstract).findAll(text=True))
            result = text
        except:
            result = abstract

    before = result
    try:
        result = fix_fake_unicode(result)
        x = re.compile(r'(\n|\r|\s){2,}')  # reduce \n to max 2
        result = x.sub(r'\n\n', result)
    except Exception as error:
        print(error)
        result = before

    if isinstance(result, str):
        result = result.strip()
    if max_words:
        parts = re.split('\s+', result)
        result = ' '.join(parts[:max_words])

    return result