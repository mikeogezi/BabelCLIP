import json
import os
import argparse
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

'''
    python run_experiment.py
'''

parser = argparse.ArgumentParser()
parser.add_argument("--output_file", "-o", default='./ranked_sample_synsets.json')
parser.add_argument("--input_file", "-i", default='./sample_synsets.json')
parser.add_argument("--model", "-m", default='openai/clip-vit-base-patch32', choices=['openai/clip-vit-base-patch32', 'openai/clip-vit-base-patch16', 'openai/clip-vit-large-patch14'])

args = parser.parse_args()
max_seq_len = 77

_in = json.load(open(args.input_file, 'r'))
out_dict = json.load(open(args.input_file, 'r'))

device = 'cuda'
model = CLIPModel.from_pretrained(args.model).to(device)
processor = CLIPProcessor.from_pretrained(args.model)
pred_map = {
    0: 'lemmas',
    1: 'gloss',
    2: 'example',
}

for id, v in _in.items():
    images_objs = v['images']
    
    images = [Image.open(i['path']).resize((224, 224)).convert('RGB') for i in images_objs]
    texts = [
        ', '.join(v['lemmas'])[:], 
        v['gloss'][:] if ('gloss' in v and v['gloss']) else None,
        v['example'][:] if ('example' in v and v['example']) in v else None,
    ]
    text_pops = [bool(text) for text in texts]

    inputs = processor(text=[text for text in texts if bool(text)], images=images, return_tensors="pt", padding=True, truncation=True)
    inputs = inputs.to(device)
    outputs = model(**inputs)
    
    probs = outputs.logits_per_image.softmax(dim=0)
    # print(probs)

    for r_idx, r in enumerate(probs):
        c_idx = 0
        for idx in range(len(texts)):
            populated = text_pops[idx]
            out_dict[id]['images'][r_idx]['{}_confidence'.format(pred_map[idx])] = float(r[c_idx]) if populated else None
            if populated:
                c_idx += 1

json.dump(out_dict, open(args.output_file, 'w'), ensure_ascii=False, indent=2)