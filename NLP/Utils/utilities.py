# $HeadURL: svn+ssh://s2.r88r.org/opt/svn/r8i8r/trunk/R88R/Crawler/Utilities.py $

""" Various string related utilities
"""

__RCSID__ = '$Id: Utilities.py 3740 2011-03-13 19:47:19Z atsareg $'

from R88R.Core.Logger import logger


def cleanStrings(data):
    """fixes funky string, e.g. backslashes in urls
    operates on strings here, recurses on other types ({} and [])"""
    changed = False
    if isinstance(data, basestring):
        # this is where strings are fixed, add other processing here if you like
        other = data.replace("\\", "")  # get rid of escaping
        changed = other != data
        if changed: data = other
    elif type(data) == type({}):  # recurse
        for k, v in data.items():
            v, thisChanged = cleanStrings(v)
            changed = changed or thisChanged
            data[k] = v
    elif type(data) == type([]):  # recurse
        for item in data:
            item, thisChanged = cleanStrings(item)
            changed = changed or thisChanged

    return data, changed


def cleanString(s, encoding='utf-8', errors='strict'):
    """
    Returns a bytestring version of strings. Migrated from smart_str in twitterIO
    """
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s


import re, htmlentitydefs

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
'''from http://effbot.org/zone/re-sub.htm#unescape-html'''


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is

    return re.sub("&#?\w+;", fixup, text)


pattern = re.compile("&(\w+?);")
'''from http://effbot.org/librarybook/htmlentitydefs.htm'''


def descape_entity(m, defs=htmlentitydefs.entitydefs):
    # callback: translate one entity to its ISO Latin value
    # logger.info('descape %s'%m.groups())
    try:
        return defs[m.group(1)]
    except KeyError:
        # logger.warning('key error descape %s'%(m.groups()))
        return m.group(0)  # use as is
    except Exception as error:
        logger.warning('error descaping text %s' % (m.groups()))
        return None


def descape(string, accents=False):
    try:
        it = pattern.sub(de_accent, string) if accents else pattern.sub(descape_entity, string)
    except Exception as error:
        logger.error('Could not map html entities %s : string = %s' % (error, string))
        return string
    return it


# the following is adapted from htmlentitydefs, maps accented letters to unaccented versions
de_accent_map = {'AElig': 'AE',
                 'Aacute': 'A',
                 'Acirc': 'A',
                 'Agrave': 'A',
                 'Alpha': '&#913;',
                 'Aring': 'A',
                 'Atilde': 'A',
                 'Auml': 'A',
                 'Beta': 'B',
                 'Ccedil': 'C',
                 'Chi': 'X',
                 'Dagger': '&#8225;',
                 'Delta': '&#916;',
                 'ETH': '\xd0',
                 'Eacute': 'E',
                 'Ecirc': 'E',
                 'Egrave': 'E',
                 'Epsilon': '&#917;',
                 'Eta': '&#919;',
                 'Euml': 'E',
                 'Gamma': '&#915;',
                 'Iacute': 'I',
                 'Icirc': 'I',
                 'Igrave': 'I',
                 'Iota': 'I',
                 'Iuml': 'I',
                 'Kappa': 'K',
                 'Lambda': '&#923;',
                 'Mu': 'M',
                 'Ntilde': 'N',
                 'Nu': 'N',
                 'OElig': 'OE',
                 'Oacute': 'O',
                 'Ocirc': 'O',
                 'Ograve': 'O',
                 'Omega': '&#937;',
                 'Omicron': 'O',
                 'Oslash': 'O',
                 'Otilde': 'O',
                 'Ouml': 'O',
                 'Phi': '&#934;',
                 'Pi': '&#928;',
                 'Prime': "''",
                 'Psi': '&#936;',
                 'Rho': '&#929;',
                 'Scaron': 'S',
                 'Sigma': '&#931;',
                 'THORN': '\xde',
                 'Tau': '&#932;',
                 'Theta': '&#920;',
                 'Uacute': 'U',
                 'Ucirc': 'U',
                 'Ugrave': 'U',
                 'Upsilon': '&#933;',
                 'Uuml': 'U',
                 'Xi': '&#926;',
                 'Yacute': 'Y',
                 'Yuml': 'Y',
                 'Zeta': '&#918;',
                 'aacute': 'a',
                 'acirc': 'a',
                 'acute': '\xb4',
                 'aelig': 'ae',
                 'agrave': 'a',
                 'alefsym': '&#8501;',
                 'alpha': '&#945;',
                 'amp': '&',
                 'and': '^',
                 'ang': '&#8736;',
                 'aring': 'a',
                 'asymp': '&#8776;',
                 'atilde': 'a',
                 'auml': 'a',
                 'bdquo': '"',
                 'beta': '&#946;',
                 'brvbar': '|',
                 'bull': '*',
                 'cap': '&#8745;',
                 'ccedil': 'c',
                 'cedil': '\xb8',
                 'cent': '\xa2',
                 'chi': '&#967;',
                 'circ': '&#710;',
                 'clubs': '&#9827;',
                 'cong': '&#8773;',
                 'copy': '\xa9',
                 'crarr': '&#8629;',
                 'cup': '&#8746;',
                 'curren': '\xa4',
                 'dArr': '&#8659;',
                 'dagger': '&#8224;',
                 'darr': '&#8595;',
                 'deg': 'deg',
                 'delta': '&#948;',
                 'diams': '&#9830;',
                 'divide': '/',
                 'eacute': 'e',
                 'ecirc': 'e',
                 'egrave': 'e',
                 'empty': '',
                 'emsp': ' ',
                 'ensp': '&#8194;',
                 'epsilon': '&#949;',
                 'equiv': '=',
                 'eta': '&#951;',
                 'eth': '\xf0',
                 'euml': 'e',
                 'euro': '&#8364;',
                 'exist': '&#8707;',
                 'fnof': 'f',
                 'forall': '&#8704;',
                 'frac12': '\xbd',
                 'frac14': '\xbc',
                 'frac34': '\xbe',
                 'frasl': '/',
                 'gamma': '&#947;',
                 'ge': '&#8805;',
                 'gt': '>',
                 'hArr': '&#8660;',
                 'harr': '&#8596;',
                 'hearts': '&#9829;',
                 'hellip': '...',
                 'iacute': 'i',
                 'icirc': 'i',
                 'iexcl': '!',
                 'igrave': 'i',
                 'image': '&#8465;',
                 'infin': '&#8734;',
                 'int': '&#8747;',
                 'iota': 'i',
                 'iquest': '\xbf',
                 'isin': '&#8712;',
                 'iuml': 'i',
                 'kappa': 'k',
                 'lArr': '&#8656;',
                 'lambda': '&#955;',
                 'lang': '&#9001;',
                 'laquo': '<<',
                 'larr': '&#8592;',
                 'lceil': '&#8968;',
                 'ldquo': '"',
                 'le': '&#8804;',
                 'lfloor': '&#8970;',
                 'lowast': '&#8727;',
                 'loz': '&#9674;',
                 'lrm': '&#8206;',
                 'lsaquo': '<',
                 'lsquo': "'",
                 'lt': '<',
                 'macr': '\xaf',
                 'mdash': '-',
                 'micro': '\xb5',
                 'middot': '*',
                 'minus': '-',
                 'mu': '&#956;',
                 'nabla': '&#8711;',
                 'nbsp': ' ',
                 'ndash': '-',
                 'ne': '&#8800;',
                 'ni': '&#8715;',
                 'not': '\xac',
                 'notin': '&#8713;',
                 'nsub': '&#8836;',
                 'ntilde': 'n',
                 'nu': '&#957;',
                 'oacute': 'o',
                 'ocirc': 'o',
                 'oelig': 'oe',
                 'ograve': 'o',
                 'oline': '_',
                 'omega': '&#969;',
                 'omicron': 'o',
                 'oplus': '+',
                 'or': 'V',
                 'ordf': '\xaa',
                 'ordm': '\xba',
                 'oslash': 'o',
                 'otilde': 'o',
                 'otimes': 'x',
                 'ouml': 'o',
                 'para': '\xb6',
                 'part': '&#8706;',
                 'permil': '&#8240;',
                 'perp': '&#8869;',
                 'phi': '&#966;',
                 'pi': '&#960;',
                 'piv': '&#982;',
                 'plusmn': '\xb1',
                 'pound': '\xa3',
                 'prime': "'",
                 'prod': '&#8719;',
                 'prop': '&#8733;',
                 'psi': '&#968;',
                 'quot': '"',
                 'rArr': '&#8658;',
                 'radic': '&#8730;',
                 'rang': '&#9002;',
                 'raquo': '>>',
                 'rarr': '&#8594;',
                 'rceil': '&#8969;',
                 'rdquo': '"',
                 'real': '&#8476;',
                 'reg': '\xae',
                 'rfloor': '&#8971;',
                 'rho': '&#961;',
                 'rlm': '&#8207;',
                 'rsaquo': '>',
                 'rsquo': "'",
                 'sbquo': "'",
                 'scaron': 's',
                 'sdot': 's',
                 'sect': '\xa7',
                 'shy': '-',
                 'sigma': '&#963;',
                 'sigmaf': '&#962;',
                 'sim': '&#8764;',
                 'spades': '&#9824;',
                 'sub': '&#8834;',
                 'sube': '&#8838;',
                 'sum': '&#8721;',
                 'sup': '&#8835;',
                 'sup1': '\xb9',
                 'sup2': '\xb2',
                 'sup3': '\xb3',
                 'supe': '&#8839;',
                 'szlig': 'sz',
                 'tau': '&#964;',
                 'there4': '&#8756;',
                 'theta': '&#952;',
                 'thetasym': '&#977;',
                 'thinsp': ' ',
                 'thorn': '\xfe',
                 'tilde': '&#732;',
                 'times': '*',
                 'trade': '&#8482;',
                 'uArr': 'u',
                 'uacute': 'u',
                 'uarr': '&#8593;',
                 'ucirc': 'u',
                 'ugrave': 'u',
                 'uml': '\xa8',
                 'upsih': '&#978;',
                 'upsilon': '&#965;',
                 'uuml': 'u',
                 'weierp': '&#8472;',
                 'xi': '&#958;',
                 'yacute': 'y',
                 'yen': 'Y',
                 'yuml': 'y',
                 'zeta': '&#950;',
                 'zwj': '',
                 'zwnj': ''}


def de_accent(m, defs=de_accent_map):
    return descape_entity(m, defs=defs)


if __name__ == '__main__':
    input = 'Venture Capital Firm Raises $1.1 Billion for \x91Green\x92 Funds - NYTimes.com'
    output, cleaned = cleanStrings(input)
    print(output)
    print('was cleaned', cleaned)

    url = 'http:\\/\\/bit.ly\\/krMN7a'
    print(cleanStrings(url))

