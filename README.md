# CMPUT 600 W22 Project

## Prerequisites
- Install Java (OpenJDK 11.0.14.1; I make extensive use of lambdas and streams)
- Install Python 3.8.12

## Playing with this work
- Download and configure [BabelNet 5.0 indices](https://babelnet.org/guide#access)
- Download the Java API from the same page as above
- [Download](https://drive.google.com/file/d/1pOsn2dlRaSAMjX-0x_Bj4MnSaXcHXOFs/view?usp=sharing) and extract [BabelPic](https://sapienzanlp.github.io/babelpic/)-Gold
- Generate `gold_synsets.json`: 
    - `cd java`
    - `sh run-babelpic.sh`
    - `cd ..`
- Optionally download and extract the silver splits of [BabelPic](https://sapienzanlp.github.io/babelpic/)
- `python pull.py --sample_size 100`
- `python run_experiments.py`