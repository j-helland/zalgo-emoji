import os
import json
import random
import argparse

import emoji as emo


def extract_emojis(d: dict, emoji_keys: set = None) -> list:
    if 'value' in d:
        if emoji_keys:
            if d['value'] in emoji_keys:
                return d['value']
            return []
        else:
            return [d['value']]

    emojis = []
    if isinstance(d, list):
        for _d in d:
            emojis.extend(extract_emojis(_d, emoji_keys))
    elif isinstance(d, dict):
        for k in d:
            emojis.extend(extract_emojis(d[k], emoji_keys))

    else:
        raise TypeError(type(d))

    return emojis


def load_emojis(path: str, emoji_keys: set = None) -> list:
    assert os.path.isfile(path)
    with open(path, 'rb') as data:
        d = json.load(data)
    return extract_emojis(d, emoji_keys)


templates = [
    '\\overset{{ {:s} }}{{ {:s} }}',
    '\\underset{{ {:s} }}{{ {:s} }}',
    '{{ {:s} }}^{{ {:s} }}',
    '{{ {:s} }}_{{ {:s} }}',
]


def stack_emojis(string, emojis, num_levels, font_size):
    out_string = ''
    for c in string:
        c = f'\\text{{ {{\\{font_size:s} {c:s} }} }}'
        random.shuffle(emojis)
        #indices = [random.randint(0, len(templates)) for _ in range(num_levels)]
        selected_emojis = [random.choice(emojis) for _ in range(num_levels)]
        for emoji in selected_emojis:
            idx = random.randint(0, len(templates) - 1)
            c = templates[idx].format(c, emoji)
        out_string += c
    return out_string


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-n', '--num-levels', type=int)
    parser.add_argument('--vertical', action='store_true')
    parser.add_argument('--emoji', default=None)
    parser.add_argument('--font-size', default='Huge', type=str)
    args = parser.parse_args()

    if args.vertical:
        templates = templates[:2]

    emoji_dir = os.path.join('./EmojiCodeSheet/json/string')
    assert os.path.isdir(emoji_dir)
    emoji_files = [os.path.join(emoji_dir, f) for f in os.listdir(emoji_dir)]

    emojis = [load_emojis(p, set(args.emoji)) for p in emoji_files]
    emojis = [item for sublist in emojis for item in sublist]

    print(stack_emojis(args.input, emojis, num_levels=args.num_levels, font_size=args.font_size))

