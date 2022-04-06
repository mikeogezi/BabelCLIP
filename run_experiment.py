import json
import os
import argparse
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import numpy as np
import torch

'''
    python run_experiment.py
'''

parser = argparse.ArgumentParser()
parser.add_argument("--output_file", "-o", default='./ranked/ranked_silver_sample_synsets.json')
parser.add_argument("--input_file", "-i", default='./samples/silver_sample_synsets.json')
parser.add_argument("--model", "-m", default='openai/clip-vit-base-patch32', choices=['openai/clip-vit-base-patch32', 'openai/clip-vit-base-patch16', 'openai/clip-vit-large-patch14'])
parser.add_argument("--image_batch_size", "-bs", default=100, type=int)
parser.add_argument("--device", "-d", default='cuda', type=str)

args = parser.parse_args()

_in = json.load(open(args.input_file, 'r'))
out_dict = json.load(open(args.input_file, 'r'))

device = args.device
model = CLIPModel.from_pretrained(args.model).to(device)
processor = CLIPProcessor.from_pretrained(args.model)
pred_map = {
    0: 'lemmas',
    1: 'gloss',
    2: 'example',
    3: 'ex+gloss',
    4: 'ex+lemmas'
}

def join_lemmas(lemmas):
    return ', '.join(lemmas)

with torch.no_grad():
    progress = 0
    for id, v in _in.items():
        progress += 1
        images_objs = v['images']

        images = [Image.open(i['path']).resize((224, 224)).convert('RGB') for i in images_objs]
        print('Processing {: 4} images for {}/{}\r'.format(len(images), progress, len(_in)), end='')

        texts = [
            join_lemmas(v['lemmas']),
            v['gloss'] if ('gloss' in v and v['gloss']) else None,
            v['example'] if ('example' in v and v['example']) in v else None,
            v['example'] if ('example' in v and v['example']) in v else v['gloss'],
            v['example'] if ('example' in v and v['example']) in v else join_lemmas(v['lemmas']),
        ]
        text_pops = [bool(text) for text in texts]

        probs = torch.Tensor().to(device)
        start = 0
        end = args.image_batch_size
        will_break = False
        while True:
            if will_break:
                break
            __images = images[start:end]
            start += args.image_batch_size
            end += args.image_batch_size
            will_break = (len(images) - end) <= 0
            inputs = processor(text=[text for text in texts if bool(text)], images=__images, return_tensors="pt", padding=True, truncation=True)
            inputs = inputs.to(device)
            outputs = model(**inputs)
            __probs = outputs.logits_per_image.softmax(dim=0)
            probs = torch.cat((probs, __probs), dim=0)
        
        for r_idx, r in enumerate(probs):
            c_idx = 0
            for idx in range(len(texts)):
                populated = text_pops[idx]
                out_dict[id]['images'][r_idx]['{}_confidence'.format(pred_map[idx])] = float(r[c_idx]) if populated else None
                if populated:
                    c_idx += 1

json.dump(out_dict, open(args.output_file, 'w'), ensure_ascii=False, indent=2)
