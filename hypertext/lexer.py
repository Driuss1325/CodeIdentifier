import ply.lex as lex
# Lexer tokens and states
tokens = (
    'HTML_COMMENT', 'HTML_CONDITIONAL_COMMENT', 'XML', 'CDATA', 'DTD',
    'SCRIPTLET', 'SEA_WS', 'SCRIPT_OPEN', 'STYLE_OPEN', 'TAG_OPEN',
    'HTML_TEXT', 'TAG_CLOSE', 'TAG_SLASH_CLOSE', 'TAG_SLASH',
    'TAG_EQUALS', 'TAG_NAME', 'SCRIPT_BODY', 'STYLE_BODY', 'ATTVALUE_VALUE'
)

states = (
    ('tag', 'exclusive'),
    ('script', 'exclusive'),
    ('style', 'exclusive'),
    ('attvalue', 'exclusive')
)

t_ignore = ' \t'

def t_HTML_COMMENT(t):
    r'<!--.*?-->'
    return t

def t_HTML_CONDITIONAL_COMMENT(t):
    r'<!\[.*?\]>'
    return t

def t_XML(t):
    r'<\?xml.*?\?>'
    return t

def t_CDATA(t):
    r'<!\[CDATA\[.*?\]\]>'
    return t

def t_DTD(t):
    r'<!.*?>'
    return t

def t_SCRIPTLET(t):
    r'<\?.*?\?>|<%.*?%>'
    t.value = t.value.strip('<%>').strip() # Clean the scriptlet content
    return t

def t_SEA_WS(t):
    r'[ \t]+'
    return t

def t_SCRIPT_OPEN(t):
    r'<script.*?>'
    t.lexer.begin('script')
    return t

def t_STYLE_OPEN(t):
    r'<style.*?>'
    t.lexer.begin('style')
    return t

def t_TAG_OPEN(t):
    r'<'
    t.lexer.begin('tag')
    return t

def t_HTML_TEXT(t):
    r'[^<]+'
    return t

# Tag state rules
def t_tag_TAG_CLOSE(t):
    r'>'
    t.lexer.begin('INITIAL')
    return t

def t_tag_TAG_SLASH_CLOSE(t):
    r'/>'
    t.lexer.begin('INITIAL')
    return t

def t_tag_TAG_SLASH(t):
    r'/'
    return t

def t_tag_TAG_EQUALS(t):
    r'='
    t.lexer.begin('attvalue')
    return t

def t_tag_TAG_NAME(t):
    r'[a-zA-Z_:][a-zA-Z0-9_:.\u00B7\u0300-\u036F\u203F-\u2040]*'
    return t

def t_tag_TAG_WHITESPACE(t):
    r'[ \t\r\n]+'
    return t

t_tag_ignore = ' \t\r\n'

def t_tag_error(t):
    print(f"Unexpected character in 'tag' state: {t.value[0]}")
    t.lexer.skip(1)

# Script state rules
def t_script_SCRIPT_BODY(t):
    r'[^<]+'
    return t

def t_script_TAG_CLOSE(t):
    r'</script>'
    t.lexer.begin('INITIAL')
    return t

t_script_ignore = ' \t\r\n'

def t_script_error(t):
    print(f"Unexpected character in 'script' state: {t.value[0]}")
    t.lexer.skip(1)

# Style state rules
def t_style_STYLE_BODY(t):
    r'[^<]+'
    return t

def t_style_TAG_CLOSE(t):
    r'</style>'
    t.lexer.begin('INITIAL')
    return t

t_style_ignore = ' \t\r\n'

def t_style_error(t):
    print(f"Unexpected character in 'style' state: {t.value[0]}")
    t.lexer.skip(1)

# Attvalue state rules
def t_attvalue_ATTVALUE_VALUE(t):
    r'[^<>]+'
    t.lexer.begin('tag')
    return t

t_attvalue_ignore = ' \t\r\n'

def t_attvalue_error(t):
    print(f"Unexpected character in 'attvalue' state: {t.value[0]}")
    t.lexer.skip(1)

def t_error(t):
    print(f"Illegal html character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()