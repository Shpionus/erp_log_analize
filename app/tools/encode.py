import sys
from email.header import Header
from email.utils import COMMASPACE, getaddresses, formataddr


def get_encodings(hint_encoding='utf-8'):
    fallbacks = {
        'latin1': 'latin9',
        'iso-8859-1': 'iso8859-15',
        'cp1252': '1252',
    }
    if hint_encoding:
        yield hint_encoding
        if hint_encoding.lower() in fallbacks:
            yield fallbacks[hint_encoding.lower()]

    # some defaults (also taking care of pure ASCII)
    for charset in ['utf8','latin1']:
        if not hint_encoding or (charset.lower() != hint_encoding.lower()):
            yield charset

    from locale import getpreferredencoding
    prefenc = getpreferredencoding()
    if prefenc and prefenc.lower() != 'utf-8':
        yield prefenc
        prefenc = fallbacks.get(prefenc.lower())
        if prefenc:
            yield prefenc


def exception_to_unicode(e):
    if (sys.version_info[:2] < (2,6)) and hasattr(e, 'message'):
        return ustr(e.message)
    if hasattr(e, 'args'):
        return "\n".join((ustr(a) for a in e.args))
    try:
        return unicode(e)
    except Exception:
        return u"Unknown message"


def ustr(value, hint_encoding='utf-8', errors='strict'):
    if isinstance(value, Exception):
        return exception_to_unicode(value)

    if isinstance(value, unicode):
        return value

    if not isinstance(value, basestring):
        try:
            return unicode(value)
        except Exception:
            raise UnicodeError('unable to convert %r' % (value,))

    for ln in get_encodings(hint_encoding):
        try:
            return unicode(value, ln, errors=errors)
        except Exception:
            pass
    raise UnicodeError('unable to convert %r' % (value,))

def encode_header(header_text):
    if not header_text: return ""
    header_text_utf8 = ustr(header_text).encode('utf-8')
    header_text_ascii = try_coerce_ascii(header_text_utf8)
    return header_text_ascii if header_text_ascii\
         else Header(header_text_utf8, 'utf-8')


def try_coerce_ascii(string_utf8):
    try:
        string_utf8.decode('ascii')
    except UnicodeDecodeError:
        return
    return string_utf8

def encode_rfc2822_address_header(header_text):
    def encode_addr(addr):
        name, email = addr
        if not try_coerce_ascii(name):
            name = str(Header(name, 'utf-8'))
        return formataddr((name, email))

    addresses = getaddresses([ustr(header_text).encode('utf-8')])
    return COMMASPACE.join(map(encode_addr, addresses))