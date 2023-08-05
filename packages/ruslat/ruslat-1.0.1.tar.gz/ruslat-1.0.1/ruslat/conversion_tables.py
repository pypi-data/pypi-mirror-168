# These conversions are supposed to be used with regularized cyrillic orthography to prevent
# conversions like рожь -> rožj, or Цюрих -> Ciurih. See cyrillic_ortho_fix.py.

hardvowel = {
    'а': 'a',
    'у': 'u',
    'э': 'e',
    'о': 'o',
    'ы': 'y',
}

softvowel_after_vowel = {
    'я': 'ja',
    'ю': 'ju',
    'е': 'je',
    'ё': 'jë',
    'и': 'i',
}

softvowel_after_jer_or_jerj = {
    'я': 'ja',
    'ю': 'ju',
    'е': 'je',
    'ё': 'jë',
    'и': 'ji', # Ильи -> Ilji
}

softvowel_after_consonant = {
    'я': 'ia',
    'ю': 'iu',
    'е': 'e',
    'ё': 'ë',
    'и': 'i',
}

consonant = {
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'з': 'z',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'ф': 'f',
    'х': 'h',
    'ц': 'c',
    'й': 'j',
    'ж': 'ž',
    'ч': 'č',
    'ш': 'š',
    'щ': 'sč',
}