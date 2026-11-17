"""Topic-model the references (site/references.html themes).

Pipeline: recommendations -> sentences -> TF-IDF -> NMF -> top words per theme.
Theme names and the quotes shown on the page are chosen by a person from this
output; the model decides which sentences group together.

Run: /opt/anaconda3/bin/python scripts/references/topics.py [--k 10]
"""
import argparse
import json
import re
from pathlib import Path

import numpy as np
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer

HERE = Path(__file__).parent
# names and filler that would otherwise dominate topics without describing a skill
EXTRA_STOP = {"rodrigo", "posit", "positron", "team", "work", "worked", "working",
              "ve", "ll", "just", "really", "pleasure", "having", "make", "makes"}


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z“])", text.replace("\n", " "))
    return [p.strip() for p in parts if len(p.split()) >= 4]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    recs = json.loads((HERE / "recommendations.json").read_text())
    rows = [(r["author"], s) for r in recs for s in sentences(r["text"])]
    print(f"{len(recs)} recommendations, {len(rows)} sentences\n")

    vec = TfidfVectorizer(stop_words=list(ENGLISH_STOP_WORDS | EXTRA_STOP),
                          ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    X = vec.fit_transform([s for _, s in rows])
    nmf = NMF(n_components=args.k, init="nndsvd", random_state=args.seed, max_iter=1000)
    W = nmf.fit_transform(X)
    H = nmf.components_
    terms = np.array(vec.get_feature_names_out())

    for t in range(args.k):
        top = terms[np.argsort(H[t])[::-1][:8]]
        print(f"theme {t}: {' · '.join(top)}")
        for i in np.argsort(W[:, t])[::-1][:6]:
            if W[i, t] > 0 and W[i].argmax() == t:
                print(f"   {W[i, t]:.3f}  [{rows[i][0]}] {rows[i][1]}")
        print()


if __name__ == "__main__":
    main()
