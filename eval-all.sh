python run_experiment.py --output_file ranked/ranked_sample_synsets_b32.json --input_file samples/sample_synsets.json --model openai/clip-vit-base-patch32 -bs 1024 --device cuda:0
python run_experiment.py --output_file ranked/ranked_sample_synsets_b16.json --input_file samples/sample_synsets.json --model openai/clip-vit-base-patch16 -bs 1024 --device cuda:0
python run_experiment.py --output_file ranked/ranked_sample_synsets_l14.json --input_file samples/sample_synsets.json --model openai/clip-vit-large-patch14 -bs 1024 --device cuda:0

python run_experiment.py --output_file ranked/ranked_silver_sample_synsets_b32.json --input_file samples/silver_sample_synsets.json --model openai/clip-vit-base-patch32 -bs 1024 --device cuda:0
python run_experiment.py --output_file ranked/ranked_silver_sample_synsets_b16.json --input_file samples/silver_sample_synsets.json --model openai/clip-vit-base-patch16 -bs 1024 --device cuda:0
python run_experiment.py --output_file ranked/ranked_silver_sample_synsets_l14.json --input_file samples/silver_sample_synsets.json --model openai/clip-vit-large-patch14 -bs 1024 --device cuda:0
