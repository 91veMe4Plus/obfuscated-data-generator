import random

# Hangul decomposition and composition
def split_syllable_char(char):
    code = ord(char) - 0xAC00
    if not (0 <= code <= 11171):
        raise ValueError("Not a Hangul syllable.")
    initial = code // 588
    vowel = (code % 588) // 28
    final = code % 28
    return (
        chr(0x1100 + initial),
        chr(0x1161 + vowel),
        ' ' if final == 0 else chr(0x11A7 + final)
    )

def join_jamos(initial, vowel, final=' '):
    ini = ord(initial) - 0x1100
    vow = ord(vowel) - 0x1161
    fin = 0 if final == ' ' else ord(final) - 0x11A7
    return chr(0xAC00 + 588 * ini + 28 * vow + fin)

# 테스트용: 규칙 함수 틀
def rule_liaison(text):
    result = ""
    i = 0
    while i < len(text) - 1:
        curr = text[i]
        next_char = text[i + 1]

        try:
            c_init, c_med, c_final = split_syllable_char(curr)
            n_init, n_med, n_final = split_syllable_char(next_char)
        except:
            result += curr
            i += 1
            continue

        # 받침 있고, 다음 글자의 초성이 'ᄋ'이면 연음화
        if c_final != ' ' and n_init == 'ᄋ':  # 초성 'ᄋ' 기준으로 비교
            if random.random() < 0.7:
                moved = join_jamos(c_init, c_med, ' ')
                # 종성 → 초성 변환
                jong2cho = {
                    'ᆨ': 'ᄀ', 'ᆫ': 'ᄂ', 'ᆮ': 'ᄃ', 'ᆯ': 'ᄅ', 'ᆷ': 'ᄆ',
                    'ᆸ': 'ᄇ', 'ᆺ': 'ᄉ', 'ᆼ': 'ᄋ', 'ᆽ': 'ᄌ', 'ᆾ': 'ᄎ',
                    'ᆿ': 'ᄏ', 'ᇀ': 'ᄐ', 'ᇁ': 'ᄑ', 'ᇂ': 'ᄒ'
                }
                converted_init = jong2cho.get(c_final, 'ᄋ')
                new_next = join_jamos(converted_init, n_med, n_final)
                result += moved + new_next
                i += 2  # 두 글자 모두 소모
                continue
        result += curr
        i += 1

    if i < len(text):
        result += text[i]
    return result

def rule_duplicate_onset(text):
    result = ""
    i = 0
    while i < len(text) - 1:
        curr = text[i]
        next_char = text[i + 1]
        try:
            c_init, c_med, c_final = split_syllable_char(curr)
            n_init, n_med, n_final = split_syllable_char(next_char)
        except:
            result += curr
            i += 1
            continue

        if c_final == ' ' and n_init != 'ᄋ':  # 받침이 없고, 다음 초성이 자음이면
            if random.random() < 0.7:
                jong = {
                    'ᄀ': 'ᆨ', 'ᄁ': 'ᆩ', 'ᄂ': 'ᆫ', 'ᄃ': 'ᆮ', 'ᄄ': 'ᆯ', 'ᄅ': 'ᆯ',
                    'ᄆ': 'ᆷ', 'ᄇ': 'ᆸ', 'ᄈ': 'ᆹ', 'ᄉ': 'ᆺ', 'ᄊ': 'ᆻ', 'ᄋ': 'ᆼ',
                    'ᄌ': 'ᆽ', 'ᄍ': 'ᆾ', 'ᄎ': 'ᆾ', 'ᄏ': 'ᆿ', 'ᄐ': 'ᇀ', 'ᄑ': 'ᇁ', 'ᄒ': 'ᇂ'
                }.get(n_init, 'ᆼ')  # fallback to 'ᆼ' if not matched
                new_curr = join_jamos(c_init, c_med, jong)
                result += new_curr
                i += 1
            else:
                result += curr
                i += 1
        else:
            result += curr
            i += 1

    if i < len(text):
        result += text[i]
    return result

def rule_replace_jamo(text):
    jamo_map = {
        'ᅡ': 'ᅣ', 'ᅥ': 'ᅧ', 'ᅩ': 'ᅭ', 'ᅮ': 'ᅲ',
        'ᅢ': 'ᅤ', 'ᅦ': 'ᅨ'
    }

    result = ""
    for ch in text:
        try:
            cho, jung, jong = split_syllable_char(ch)
            if random.random() < 0.7:
                cho = jamo_map.get(cho, cho)
                jung = jamo_map.get(jung, jung)
            result += join_jamos(cho, jung, jong)
        except:
            result += ch
    return result

import random

def rule_add_jongseong(text):
    meaningless_jongs = ['ㄱ', 'ㄴ', 'ᆮ', 'ᆯ', 'ᆷ', 'ᆸ', 'ᆺ', 'ᆼ']
    result = ""
    for ch in text:
        try:
            cho, jung, jong = split_syllable_char(ch)
            if jong == ' ' and random.random() < 0.3:
                jong = random.choice(meaningless_jongs)
            result += join_jamos(cho, jung, jong)
        except:
            result += ch
    return result

rules = [
    ("연음 적용", rule_liaison),
    ("받침 중복", rule_duplicate_onset),
    ("유사 자모 대체", rule_replace_jamo),
    ("의미없는 받침 추가", rule_add_jongseong),
]

def obfuscate(text):
    print("\n[적용 순서]")
    selected = random.sample(rules, k=random.randint(1, len(rules)))
    for name, _ in selected:
        print("- " + name)
    for _, func in selected:
        text = func(text)
    return text

if __name__ == '__main__':
    input_text = input("한글 문장을 입력하세요: ")
    result = obfuscate(input_text)
    print("\n[난독화 결과]")
    print(result)
