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
from PIL import Image
import io
from cairosvg import svg2png
from utils import clean_ext
import sys

'''
    python pull.py 
'''

parser = argparse.ArgumentParser()
parser.add_argument("--sample_size", help="The random sample size to pull images for", type=int, default=10)
parser.add_argument("--seed", help="The seed for random generators", type=int, default=42)
parser.add_argument("--input_file", "-i", default='./gold_synsets.json')
parser.add_argument("--output_dir", "-O", default='./pulled_images')
parser.add_argument("--output_file", "-o", default='./sample_synsets.json')
parser.add_argument("--error_log", "-e", default='./{}_log'.format(sys.argv[0].replace('.py', '')))
parser.add_argument("--ids", default=[], nargs='*')
args = parser.parse_args()

open(args.error_log, 'w').close()
logging.basicConfig(filename=args.error_log, level=logging.INFO)

seed(args.seed)
in_ = json.load(open(args.input_file, 'r'))
args.sample_size = min(args.sample_size, len(in_))
ids = [i['id'] for i in in_]
if len(args.ids) == 0:
    id_sample = sample(ids, args.sample_size)
else:
    id_sample = args.ids
dat_map = {i['id']: i for i in in_}
if exists(args.output_dir):
    contents = listdir(args.output_dir)
    for content in contents:
        if content not in id_sample:
            rmtree(join(args.output_dir, content))

def within_allowance(target, img_hashes, allowance=5):
    for img_hash in img_hashes:
        if (target - img_hash) <= allowance:
            return True
    return False

out_dat = {}
headers = {'User-Agent': 'curl/7.68.0'}
def download_images_for_id(id_dat):
  images = id_dat['images']
  id = id_dat['id']
  dest_dir = join(args.output_dir, id)
  makedirs(dest_dir, exist_ok=True)
  cnt = 0
  hashes = set()
  img_urls = set()
  img_hashes = set()
  out_dat[id] = {}
  out_dat[id]['images'] = []
  out_dat[id]['gloss'] = id_dat['mainGloss'] if 'mainGloss' in id_dat else None
  out_dat[id]['example'] = id_dat['mainExample'] if 'mainExample' in id_dat else None
  out_dat[id]['lemmas'] = id_dat['lemmas']
  out_dat[id]['goldImages'] = [join('./babelpic-gold/images', i) for i in id_dat['goldImages']]

  for idx, i in enumerate(images):
    url = i['url']
    _, ext = splitext(url)
    _, name = split(url)
    ext = clean_ext(ext)
    r = requests.get(url, stream=True, allow_redirects=True, headers=headers)
    if r.status_code == requests.codes.ok:
        cnt += 1

        # filter dups by url
        if url in img_urls:
            continue 

        content = r.content
        
        # filter dups by cryptographic hash
        hash = sha512(content).hexdigest()
        if hash in hashes:
            continue
        hashes.add(hash)

        try:
            if ext in ['.jpg', '.png']:
                pi = Image.open(io.BytesIO(content))
            elif ext == '.svg':
                content = svg2png(bytestring=content, unsafe=True)
                pi = Image.open(io.BytesIO(content))
                ext = '.png'
                logging.info('Converted {} to {} for {}'.format(url, str(idx) + ext, id))
            elif ext == '.gif':
                i = Image.open(io.BytesIO(content))
                f = io.BytesIO()
                i.save(f, format='png')
                content = f.getvalue()
                pi = Image.open(io.BytesIO(content))
                ext = '.png'
                logging.info('Converted {} to {} for {}'.format(url, str(idx) + ext, id))
            else: 
                logging.info('Skipping {} because extension was {} for {}'.format(url, ext, id))
                continue
        except Exception as e:
            logging.error('Unable to process image hash of {} for {}: {}'.format(url, id, e))
            cnt -= 1
            continue

        # filter dups by perceptual hash
        within = False
        try:
            img_hash = imagehash.phash(pi)
            within = within_allowance(img_hash, img_hashes)
            if not within:
                img_hashes.add(img_hash)
        except Exception as e:
            logging.error('Unable to compute a perceptual hash of {} for {}: {}'.format(url, id, e))
            cnt -= 1
            
        if within:
            continue

        file_name = join(dest_dir, str(idx) + ext)
        with open(file_name, 'wb') as f:
            f.write(content)
            logging.info('Saving {} to {} for {}'.format(url, file_name, id))

        out_dat[id]['images'].append({'path': file_name})
    else:
        logging.error('{} error while downloading {} for {}. Skipping...'.format(r.status_code, url, id))
    
  return cnt, len(images), id

syns = [dat_map[id] for id in id_sample]
results = ThreadPool(cpu_count()).imap_unordered(download_images_for_id, syns)
_cnt, _total = (0,) * 2
for r in results:
    cnt, total, id = r
    print('Downloaded {}/{} image(s) for {}'.format(cnt, total, id))
    _cnt += cnt
    _total += total

report = 'Downloaded {}/{} image(s) for {} synset(s)'.format(_cnt, _total, len(id_sample))
print(len(report) * '-')
print(report)

out_file = open(args.output_file, 'w')
json.dump(out_dat, out_file, ensure_ascii=False, indent=2)
out_file.close()