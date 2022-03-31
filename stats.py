import json
import requests
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
import argparse
import numpy as np
from random import seed, sample
from os.path import join, splitext, split, exists
from os import makedirs, listdir
from shutil import rmtree
from hashlib import sha512
import logging
import imagehash
from utils import clean_ext

'''
    python stats.py 
'''

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", "-i", default='./gold_synsets.json')
parser.add_argument("--input_sample_file", "-is", default='./sample_synsets.json')
args = parser.parse_args()

noun_synsets, noun_gold_images, noun_images = (0,) * 3
adj_synsets, adj_gold_images, adj_images = (0,) * 3
adv_synsets, adv_gold_images, adv_images = (0,) * 3
verb_synsets, verb_gold_images, verb_images = (0,) * 3
synsets, gold_images, images = (0,) * 3
img_exts = {}

in_ = json.load(open(args.input_file, 'r'))

# 1    NOUN 
# 2    VERB 
# 3    ADJECTIVE 
# 4    ADVERB 
# 5    ADJECTIVE SATELLITE
for g in in_:
    id = g['id']
    g_image_len = len(g['goldImages'])
    image_len = len(g['images'])
    synsets += 1
    gold_images += g_image_len
    images += image_len

    for i in g['images']:
        _, ext = splitext(i['url'])
        ext = clean_ext(ext)
        if ext not in img_exts:
            img_exts[ext] = 0
        img_exts[ext] += 1

    pos = id[-1:]
    if pos == 'n':
        noun_synsets += 1
        noun_gold_images += g_image_len
        noun_images += image_len
    elif pos == 'v':
        verb_synsets += 1
        verb_gold_images += g_image_len
        verb_images += image_len
    elif pos in ['a', 's']:
        adj_synsets += 1
        adj_images += g_image_len
        adj_images += image_len
    elif pos == 'r':
        adv_synsets += 1
        adv_images += g_image_len
        adv_images += image_len
    else:
        raise Exception('Unexpected POS: {}'.format(pos))


print('Statistics')
print('----------')
for s, g, i, n in [
        (noun_synsets, noun_gold_images, noun_images, 'Noun'), (verb_synsets, verb_gold_images, verb_images, 'Verb'), 
        (adj_synsets, adj_gold_images, adj_images, 'Adjective'), (adv_synsets, adv_gold_images, adv_images, 'Adverb'),
        (synsets, gold_images, images, 'All'),
    ]:
    if g == s == 0:
        q_g = 0.
        q = 0.
    else:
        q_g = g/s
        q = i/s
    print('{} synsets: {}\t{} images (gold / all): {} / {}\t\t{} images per synset (gold / all): {:.2f} / {:.2f}'.format(n, s, n, g, i, n, q_g, q))

print()
for e, c in img_exts.items():
    print('{} files showed up {} time(s) in all images making up {:.3f}%'.format(e, c, c*100./images))
