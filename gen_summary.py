#!/usr/bin/env python3

import os
import sys

def generate_summary(root):
    lines = []
    files = [f for f in os.listdir(root) if f.endswith('.md') and os.path.isfile(os.path.join(root, f))]
    for file in files:
        meta = get_meta(file)
        if 'title' not in meta: continue
        date = meta['date'][:11]
        lines.append(f"* [{date} {meta['title']}]({meta['file']})")

    lines.sort(reverse=True)
    print("# Table of contents\n")
    print('\n'.join(lines))

def get_meta(filename):
    meta = {'file': filename}
    with open(filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('title'):
            meta['title'] = line.strip().replace('title: ', '')
        if line.startswith('date'):
            meta['date'] = line.strip().replace('date: ', '').replace("'", "")
    return meta


def main(root):
    generate_summary(root)

if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else '.')