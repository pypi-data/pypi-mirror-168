"""Module to generate data for classification."""
from jarvis.db.figshare import data
import pandas as pd

d = data("arXiv")

df = pd.DataFrame(d)
cond_mat_topics = [
    "cond-mat.mtrl-sci",
    "cond-mat.mes-hall",
    "cond-mat.str-el",
    "cond-mat.stat-mech",
    "cond-mat.supr-con",
    "cond-mat.soft",
    "cond-mat.quant-gas",
    "cond-mat.other",
    "cond-mat.dis-nn",
]
df_cond_mat = df[
    df["categories"].apply(lambda x: "cond-mat" in x and x in cond_mat_topics)
]
dff = df_cond_mat[["id", "title", "abstract", "categories"]]
dff["title_abstract"] = dff["title"] + " " + df["abstract"]
dff.to_csv("cond_mat.csv")
