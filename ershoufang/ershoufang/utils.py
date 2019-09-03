import re

def is_full(text):
    """
    text > fangtianxia's html text
    """
    li = re.findall(r'共(\d{1,3})页', text)
    return len(li) != 0 and li[0] == '100'

def is_empty(text):
    """
    text > fangtianxia's html text
    """
    return '很抱歉' in text