# CMPUT 600 W22 Project

## Prerequisites
- Install Java (OpenJDK 11.0.14.1; I make extensive use of lambdas and streams)
- Install Python 3.8.12

## Playing with this work
- Download and configure [BabelNet 5.0 indices](https://babelnet.org/guide#access)
- Download the Java API from the same page as above
- [Download](https://drive.google.com/file/d/1pOsn2dlRaSAMjX-0x_Bj4MnSaXcHXOFs/view?usp=sharing) and extract [babelpic](https://sapienzanlp.github.io/babelpic/)-gold
- Generate `gold_synsets.json`: 
    - `cd java`
    - `sh run-babelpic.sh`
    - `cd ..`
- Optionally [download](https://drive.google.com/file/d/16wmaAuvJUWALs-lN0Ao55UuvusZpWUen/view?usp=sharing) and extract the first split of [babelpic](https://sapienzanlp.github.io/babelpic/)-silver
- `python pull.py --sample_size 100`
- `python run_experiments.py`