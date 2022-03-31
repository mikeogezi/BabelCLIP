### Stats
- Gold synsets: 2,756
- Gold images: 15,140
- Average images per synset: 5.4934687954

### Preprocessing
- Script to select an n-sample of the BabelPic dataset
- Deduplicate with URLs
- Deduplicate with conventional cryptographic SHA512 hashes
- Deduplicate with image hashes
- Filter out problematic file types like pdf, djvu, xcf
- Filter out weird audio/video files: ogg, oga, webm, ogv, mid, wav, flac
- Filtered out 3d files like stl
- Extracted images from gifs
- Converted svg, tif, bmp to png
- Ended up with only png and jpg
- Filtered out php and aspx files
- Convert svgs and pngs to jpgs
- 98.706% coverage with pngs, jpegs, converted svgs, and converted gifs
- Compared image embeddings to texts embeddings for:
    - concatenated lemmas
    - main gloss
    - main example
- Truncated text at the maximum sequence lenght causing us to lose some information
- Reshaped image
- TODO: Try cropping and other techniques

- BERT-based tokenizer
- Truncated after 77 tokens