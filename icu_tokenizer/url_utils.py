import re
import regex

__all__ = ['email_pattern', 'grubber_url_matcher']


sub_domain_pstr = r'[0-9A-Za-z\-\_\~]+'
top_domain_pstr = r'(?:[.](?:{}))'.format(r'|'.join(re.escape(s) for s in [
    'com', 'org', 'net', 'int', 'edu', 'gov', 'mil', 'ac', 'ad',
    'ae', 'af', 'ag', 'ai', 'al', 'am', 'ao', 'aq', 'ar', 'as',
    'at', 'au', 'aw', 'ax', 'az',
    'ba', 'bb', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bm',
    'bn', 'bo', 'br', 'bs', 'bt', 'bw', 'by', 'bz',
    'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm',
    'cn', 'co', 'cr', 'cu', 'cv', 'cw', 'cx', 'cy', 'cz',
    'de', 'dj', 'dk', 'dm', 'do', 'dz',
    'ec', 'ee', 'eg', 'er', 'es', 'et', 'eu',
    'fi', 'fj', 'fk', 'fm', 'fo', 'fr',
    'ga', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn',
    'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gw', 'gy',
    'hk', 'hm', 'hn', 'hr', 'ht', 'hu',
    'id', 'ie', 'il', 'im', 'in', 'io', 'iq', 'ir', 'is', 'it',
    'je', 'jm', 'jo', 'jp',
    'ke', 'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kr', 'kw', 'ky',
    'kz',
    'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv',
    'ly',
    'ma', 'mc', 'md', 'me', 'mg', 'mh', 'mk', 'ml', 'mm', 'mn',
    'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx',
    'my', 'mz',
    'na', 'nc', 'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr',
    'nu', 'nz',
    'om',
    'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn', 'pr',
    'ps', 'pt', 'pw', 'py',
    'qa',
    're', 'ro', 'rs', 'ru', 'rw',
    'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sk', 'sl',
    'sm', 'sn', 'so', 'sr', 'ss', 'st', 'su', 'sv', 'sx', 'sy',
    'sz',
    'tc', 'td', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn',
    'to', 'tr', 'tt', 'tv', 'tw', 'tz',
    'ua', 'ug', 'uk', 'us', 'uy', 'uz',
    'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu',
    'wf', 'ws',
    'ye', 'yt',
    'za', 'zm', 'zw'
]))  # https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains

domain_pstr = r'(?:{sub_domain}\.)*{sub_domain}{top_domain}'.format(
    sub_domain=sub_domain_pstr,
    top_domain=top_domain_pstr,
)

# https://stackoverflow.com/questions/2049502/what-characters-are-allowed-in-an-email-address
local_part_valid_word = r'[0-9A-Za-z\!\#\$\%\&\'\*\+\-\/\=\?\^\_\`\{\|\}\~]+'
local_part_pstr = r'{word}(?:\.{word})*'.format(word=local_part_valid_word)

email_pstr = r'({})'.format(
    r'{local_part}\@{domain}'.format(
        local_part=local_part_pstr,
        domain=domain_pstr,
    )
)
email_pattern: regex.regex.Pattern = regex.compile(email_pstr, re.IGNORECASE)
"""Custom email matcher based on
https://en.wikipedia.org/wiki/International_email
"""


# A customized grubber v1 URL matcher
# Designed to work with urls starting with https, http, ftp, or www
grubber_url_pstr = r'(?i)\b((?:(?:https|http|ftp):/{1,3}|www[.])[^\s()<>\（\）\【\】]+(?:\([\w\d]+\)|(?:[^!"#$%&\'()*+,\-./:;<=>?@\[\]\s\（\）\【\】。，？！]|/)))'  # noqa
grubber_url_matcher: re.Pattern = re.compile(grubber_url_pstr, re.ASCII)
"""Grubber v1 URL matcher with additional rules to account for chinese
punctuations.

Designed to work with urls starting with https, http, ftp, or www.
"""
