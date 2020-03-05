#!/usr/bin/env python3

import os
import sys

replacement = {
    '<p>': '',
    '</p>': '\n',
    '<br />': '',
    '&amp;': '&',
    '&#47;': '/',
    '&ldquo;': '"',
    '&rdquo;': '"',
    '&nbsp;': ' ',
    '&hellip;': '...',
    '&bull;': '•',
    '&ndash;': '-',
    '&mdash;': '-',
    '<pre>': '```',
    '</pre>': '```',
    '<code>': '```',
    '</code>': '```',
    '\n\n\n```\n\n\n': '\n\n```\n\n',
    '<del>': '~~',
    '</del>': '~~',
    '<h1>': '# ',
    '</h1>': '',
    '<h2>': '## ',
    '</h2>': '',
    '<h3>': '### ',
    '</h3>': '',
    '<strong>': '**',
    '</strong>': '**',
    '\n\n\n': '\n\n',
}

def main(filename):
    print(f"processing {filename}")
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    lines = extract_header(lines)
    content = format(''.join(lines))
    
    filename=os.path.basename(filename)[11:]
    with open(filename, 'w') as f:
        f.write(content)


def format(content):
    content = content.replace('\n\n\n', '\n\n')
    content = content.replace('\n\n\n', '\n\n')
    content = content.replace('\n\n\n', '\n\n')
    for k, v in replacement.items():
        content = content.replace(k, v)
    return content


def extract_header(lines):
    content = []
    headers = 0
    for line in lines:
        if headers == 2:
            content.append(line)
            continue

        if line.strip() == '---':
            headers += 1
            content.append(line)

        if headers > 0:
            if line.startswith('title:') or line.startswith('date:'):
                content.append(line)
    return content


def generate_summary(root):
    files = [f for f in os.listdir(root) if f.endswith('.md') and os.path.isfile(os.path.join(root, f))]
    print(files)


if __name__=="__main__":
    main(sys.argv[1])