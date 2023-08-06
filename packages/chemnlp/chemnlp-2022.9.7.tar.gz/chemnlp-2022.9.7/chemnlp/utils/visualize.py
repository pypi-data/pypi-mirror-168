"""Module to visualize tsne."""
import pandas as pd
# import json
from tqdm import tqdm
from jarvis.db.figshare import data
from collections import Counter
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE
from time import time
# import nltk
import matplotlib.pyplot as plt
# import matplotlib.colors
# import matplotlib.cm as cm
# https://github.com/chrismbryant/arXiv-structure
# /blob/master/Attempt%202/arxivstruct_2.ipynb

plt.switch_backend("agg")
# %matplotlib inline
# nltk.download('punkt')
arxiv = data("arXiv")

a = arxiv  # [0:10000]
dfa = pd.DataFrame(a)
y1 = {
    "cs.AI": "Computer Science",
    "cs.AR": "Computer Science",
    "cs.CC": "Computer Science",
    "cs.CE": "Computer Science",
    "cs.CG": "Computer Science",
    "cs.CL": "Computer Science",
    "cs.CR": "Computer Science",
    "cs.CV": "Computer Science",
    "cs.CY": "Computer Science",
    "cs.DB": "Computer Science",
    "cs.DC": "Computer Science",
    "cs.DL": "Computer Science",
    "cs.DM": "Computer Science",
    "cs.DS": "Computer Science",
    "cs.ET": "Computer Science",
    "cs.FL": "Computer Science",
    "cs.GL": "Computer Science",
    "cs.GR": "Computer Science",
    "cs.GT": "Computer Science",
    "cs.HC": "Computer Science",
    "cs.IR": "Computer Science",
    "cs.IT": "Computer Science",
    "cs.LG": "Computer Science",
    "cs.LO": "Computer Science",
    "cs.MA": "Computer Science",
    "cs.MM": "Computer Science",
    "cs.MS": "Computer Science",
    "cs.NA": "Computer Science",
    "cs.NE": "Computer Science",
    "cs.NI": "Computer Science",
    "cs.OH": "Computer Science",
    "cs.OS": "Computer Science",
    "cs.PF": "Computer Science",
    "cs.PL": "Computer Science",
    "cs.RO": "Computer Science",
    "cs.SC": "Computer Science",
    "cs.SD": "Computer Science",
    "cs.SE": "Computer Science",
    "cs.SI": "Computer Science",
    "cs.SY": "Computer Science",
    "econ.EM": "Economics",
    "econ.GN": "Economics",
    "econ.TH": "Economics",
    "eess.AS": "Electrical Engineering",
    "eess.SY": "Electrical Engineering",
    "eess.IV": "Electrical Engineering",
    "eess.SP": "Electrical Engineering",
    "math.AC": "Mathematics",
    "math.AG": "Mathematics",
    "math.AP": "Mathematics",
    "math.AT": "Mathematics",
    "math.CA": "Mathematics",
    "math.CO": "Mathematics",
    "math.CT": "Mathematics",
    "math.CV": "Mathematics",
    "math.DG": "Mathematics",
    "math.DS": "Mathematics",
    "math.FA": "Mathematics",
    "math.GM": "Mathematics",
    "math.GN": "Mathematics",
    "math.GR": "Mathematics",
    "math.GT": "Mathematics",
    "math.HO": "Mathematics",
    "math.IT": "Mathematics",
    "math.KT": "Mathematics",
    "math.LO": "Mathematics",
    "math.MG": "Mathematics",
    "math.MP": "Mathematics",
    "math.NA": "Mathematics",
    "math.NT": "Mathematics",
    "math.OA": "Mathematics",
    "math.OC": "Mathematics",
    "math.PR": "Mathematics",
    "math.QA": "Mathematics",
    "math.RA": "Mathematics",
    "math.RT": "Mathematics",
    "math.SG": "Mathematics",
    "math.SP": "Mathematics",
    "math.ST": "Mathematics",
    "astro-ph": "Physics",
    "astro-ph.CO": "Physics",
    "astro-ph.EP": "Physics",
    "astro-ph.GA": "Physics",
    "astro-ph.HE": "Physics",
    "astro-ph.IM": "Physics",
    "astro-ph.SR": "Physics",
    "cond-mat.dis-nn": "Physics",
    "cond-mat": "Physics",
    "cond-mat.mes-hall": "Physics",
    "cond-mat.mtrl-sci": "Physics",
    "cond-mat.other": "Physics",
    "cond-mat.quant-gas": "Physics",
    "cond-mat.soft": "Physics",
    "cond-mat.stat-mech": "Physics",
    "cond-mat.str-el": "Physics",
    "cond-mat.supr-con": "Physics",
    "gr-qc": "Physics",
    "hep-ex": "Physics",
    "hep-lat": "Physics",
    "hep-ph": "Physics",
    "hep-th": "Physics",
    "math-ph": "Physics",
    "nlin.AO": "Physics",
    "nlin.CD": "Physics",
    "nlin.CG": "Physics",
    "nlin.PS": "Physics",
    "nlin.SI": "Physics",
    "nucl-ex": "Physics",
    "nucl-th": "Physics",
    "physics.acc-ph": "Physics",
    "physics.ao-ph": "Physics",
    "physics.app-ph": "Physics",
    "physics.atm-clus": "Physics",
    "physics.atom-ph": "Physics",
    "physics.bio-ph": "Physics",
    "physics.chem-ph": "Physics",
    "physics.class-ph": "Physics",
    "physics.comp-ph": "Physics",
    "physics.data-an": "Physics",
    "physics.ed-ph": "Physics",
    "physics.flu-dyn": "Physics",
    "physics.gen-ph": "Physics",
    "physics.geo-ph": "Physics",
    "physics.hist-ph": "Physics",
    "physics.ins-det": "Physics",
    "physics.med-ph": "Physics",
    "physics.optics": "Physics",
    "physics.plasm-ph": "Physics",
    "physics.pop-ph": "Physics",
    "physics.soc-ph": "Physics",
    "physics.space-ph": "Physics",
    "quant-ph": "Physics",
    "q-bio": "Quantitative Biology",
    "q-bio.BM": "Quantitative Biology",
    "q-bio.CB": "Quantitative Biology",
    "q-bio.GN": "Quantitative Biology",
    "q-bio.MN": "Quantitative Biology",
    "q-bio.NC": "Quantitative Biology",
    "q-bio.OT": "Quantitative Biology",
    "q-bio.PE": "Quantitative Biology",
    "q-bio.QM": "Quantitative Biology",
    "q-bio.SC": "Quantitative Biology",
    "q-bio.TO": "Quantitative Biology",
    "q-fin.CP": "Quantitative Finance",
    "q-fin.EC": "Quantitative Finance",
    "q-fin.GN": "Quantitative Finance",
    "q-fin.MF": "Quantitative Finance",
    "q-fin.PM": "Quantitative Finance",
    "q-fin.PR": "Quantitative Finance",
    "q-fin.RM": "Quantitative Finance",
    "q-fin.ST": "Quantitative Finance",
    "q-fin.TR": "Quantitative Finance",
    "stat.AP": "Statistics",
    "stat.CO": "Statistics",
    "stat.ME": "Statistics",
    "stat.ML": "Statistics",
    "stat.OT": "Statistics",
    "stat.TH": "Statistics",
    "patt-sol": "Statistics",
    "supr-con": "Physics",
    "plasm-ph": "Physics",
    "chem-ph": "Physics",
    "bayes-an": "Statistics",
    "solv-int": "Mathematics",
    "atom-ph": "Physics",
    "q-alg": "Mathematics",
    "mtrl-th": "Physics",
}

dfa["categories_1"] = dfa["categories"].apply(lambda x: x.split()[-1])
dfa["term"] = dfa["categories_1"].apply(lambda x: y1[x])
dfa["summary"] = dfa["abstract"]
dfb = dfa[["term", "title", "summary", "id"]]
ps = PorterStemmer()

df = dfb
samples = len(df)


def abstract2df(df_small, idx):
    """
    USAGE: Use Porter Stemming to process a paper abstract.

    ARGUMENT:
    df - DataFrame with keys ["term", "title", "summary", "id"]
    idx - index locating paper within DataFrame

    RETURNS: stem_df - DataFrame with keys ["stems", "counts", "docs"]
    """
    abstract = df.iloc[idx].title
    # abstract = df.iloc[idx].summary
    words = word_tokenize(abstract)
    stems = [ps.stem(w).lower() for w in words]
    counts = Counter(stems)
    docs = list(np.ones(len(counts)).astype(int))
    stem_df = pd.DataFrame(
        {
            "stems": list(counts.keys()),
            "counts": list(counts.values()),
            "docs": docs,
        }
    )
    stem_df = stem_df[["stems", "counts", "docs"]]
    return stem_df


def docs2idf(df, num):
    """
    USAGE:
    Get an inverse document frequency (idf) measure for each stem,
    and add that measure to the word stem DataFrame.

    ARGUMENTS:
    df - word stem DataFrame
    num - total number of papers in document pool
    """
    df["idf"] = np.log(num / df["docs"])
    return df


print("Counting word stems in %d abstracts..." % len(df))
full_stem_df = pd.DataFrame()
for idx in range(len(df)):
    # print(idx)
    stem_df = abstract2df(df, idx)
    full_stem_df = pd.concat([full_stem_df, stem_df])
    if idx and idx % 10 == 0 or idx == len(df) - 1:
        full_stem_df = full_stem_df.groupby("stems").sum()
        full_stem_df["stems"] = full_stem_df.index
        full_stem_df = full_stem_df[["stems", "counts", "docs"]]
full_stem_df.sort_values("counts", ascending=False, inplace=True)
all_stems = full_stem_df  # count_stems(dfb)
all_stems = docs2idf(all_stems, len(df))
all_stems.reset_index(drop=True, inplace=True)
df = dfb
stems = all_stems
assert samples <= len(df)
idf = np.array(list(stems["idf"]))
stems = stems[["stems", "idf"]]
matrix = np.zeros((samples, len(stems)))
info = []
print("Embedding paper abstracts...")
i = 0
for idx in tqdm(range(samples)):
    # print(idx)
    information = list(df.iloc[idx][["id", "term", "title"]])
    info.append(information)
    new_df = pd.merge(
        stems, abstract2df(df, idx), on="stems", how="left"
    ).fillna(0)
    vec = np.array(list(new_df["counts"]))
    vec /= np.sum(vec)  # components sum to 1
    vec *= idf  # apply inverse document frequency
    matrix[i, :] = vec
    i += 1
print("Paper abstracts converted to vectors.")


def reduce_dim(matrix, dims):
    """
    USAGE: Perform Truncated SVD to reduce dimensionality of embedding space.

    ARGUMENTS:
    matrix - training data (sparse matrix) with shape (n_features, n_samples)
    dims - number of dimensions to project data into

    RETURNS:
    X_new - array of reduced dimensionality
    """

    tic = time()
    print("Performing Truncated SVD...")
    svd = TruncatedSVD(n_components=dims, random_state=1)
    X = svd.fit_transform(matrix)  # matrix.shape = (n_samples, n_features)
    toc = time()
    print(
        "Embeddings reduced from %d to %d using TruncatedSVD. (Time: %.2f s)"
        % (matrix.shape[1], dims, (toc - tic))
    )
    return X


def TSNE2D(X):
    """
    USAGE: Perform TSNE to reduce embedding space to 2D
    ARGUMENT: X - high-dimensional training array (n_samples, n_features ~ 100)
    RETURNS: X_embedded - 2D matrix (n_samples, 2)
    """

    tic = time()
    print("Performing TSNE...")
    X_embedded = TSNE(
        n_components=2, perplexity=30, random_state=1
    ).fit_transform(X)
    toc = time()
    print(
        "Embeddings reduced to 2 dimensions through TSNE. (Time : %.2f s)"
        % (toc - tic)
    )
    return X_embedded


X = reduce_dim(matrix, 128)
X_embedded = TSNE2D(X)


plt.figure(figsize=(8, 8))
X = X_embedded
x = X[:, 0]
y = X[:, 1]

term_list = list(np.array(info).T[1])
term_set = list(set(term_list))
term_list = [term_set.index(term) for term in term_list]

color_list = plt.cm.tab10(term_list)

lbls = []
xyz = []
for i, j, k, p in zip(x, y, term_list, color_list):
    if k not in lbls:
        lbls.append(k)
        xyz.append([i, j, k])
        plt.scatter(i, j, s=10, c=p, label=term_set[k])


plt.scatter(x, y, s=10, c=color_list)  # ,label=term_list)
plt.legend()

# plt.show()
# plot_2D(X_embedded, info)
plt.savefig("tsne.png")
plt.close()
