import argparse
parser = argparse.ArgumentParser()
parser.add_argument('editors_csv')
parser.add_argument('keywords', nargs='+')
args = parser.parse_args()

import pandas as pd
from crossref.restful import Works
from tqdm import tqdm

df = pd.read_csv(args.editors_csv, header=None, usecols=[0])[0]
results = []
works = Works()
for editor in tqdm(df):
    papers = works.query(author=editor).filter(has_abstract='true').sample(100)
    papers = [(paper['title'][0], paper['abstract']) for paper in papers if any(keyword in paper['abstract'] for keyword in args.keywords)]
    results.append((len(papers), editor, [p[0] for p in papers]))

for count, editor, papers in sorted(results):
    print(f'{count:03d} {editor} {papers}')
