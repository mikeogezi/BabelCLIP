import argparse

'''
    python compute.py
'''

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", "-i", default='./results/on_gold.txt')
args = parser.parse_args()

both, neither, babelpic, babelclip, nothing = (0,) * 5

with open(args.input_file) as f:
    _in = { int(i.strip().split('. ')[0]): i.strip().split('. ')[1].split(' ') for i in f.readlines() }
    _max = max(_in.keys())
    _min = min(_in.keys())
    assert (_max - _min + 1) == _max
    for k, v in _in.items():
        if v[0] == 'n':
            neither += 1
        elif v[0] == 'b':
            both += 1
        elif (v[0] == '1' or v[0] == '2') and v[1] == 'g':
            babelpic += 1
        elif (v[0] == '1' or v[0] == '2') and v[1] == 's':
            babelclip += 1
        elif v[0] == '-':
            nothing += 1
        else:
            raise Exception('Unexpected line: {} -> {}'.format(k, v))
            
print('Both:', both)
print('Neither:', neither)
print('BabelPic:', babelpic)
print('BabelCLIP:', babelclip)
print('Nothing:', nothing)

print('BabelCLIP Preference: {:.2f}%'.format((babelclip + both + neither) * 100. / (both + neither + babelclip + babelpic)))
print('BabelPIC Preference: {:.2f}%'.format((babelpic + both + neither) * 100. / (both + neither + babelclip + babelpic)))
print('Both/Neither Rate: {:.2f}%'.format((both + neither) * 100. / (both + neither + babelclip + babelpic)))