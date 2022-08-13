from pathlib import Path
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--length', default=None, type=int)

wordlist = '/usr/share/dict/words'
words = Path(wordlist).read_text().splitlines()

args = parser.parse_args()
np = None
while (np is None) or (args.length and len(np) > args.length):
    np = '.'.join(random.choice(words) for x in range(4)).replace("'s", '')
print(np)
with open('pwdlist.txt', 'a') as f: f.write(np+'\n')
