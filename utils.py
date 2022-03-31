__replace_map = {
    'jpeg': 'jpg',
    'tiff': 'tif',
    'asp': 'aspx',
}

def clean_ext(ext: str):
    ext = ext.lower()
    for k, v in __replace_map.items():
        if ext.endswith(k):
            ext = ext.replace(k, v)
    if '?' in ext:
        ext = ext.split('?')[0]
    return ext