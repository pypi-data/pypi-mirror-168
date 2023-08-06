import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


key='term'
value='title'
df=pd.read_csv('/home/knc6/Software/chemdata/chemnlp/chemnlp/clustering/id_term_title.csv')


#"""
from jarvis.db.figshare import data
arxiv=data('arXiv')
df = pd.DataFrame(arxiv)
cond_mat_topics = ['cond-mat.mtrl-sci', 'cond-mat.mes-hall', 'cond-mat.str-el',
                   'cond-mat.stat-mech','cond-mat.supr-con','cond-mat.soft','cond-mat.dis-nn']
df_cond_mat = df[df['categories'].apply(lambda x: 'cond-mat' in x and x in cond_mat_topics)]
df_cond_mat_forScikit = df_cond_mat[['id', 'categories',  'title', 'abstract']].reset_index(drop = True)
df_cond_mat_forScikit.rename(columns = {'categories': 'term',
                                      'title': 'title'})
df=df_cond_mat_forScikit
key='categories'
#"""

print (df)
print (df[key].value_counts())
df['category_id'] = df[key].factorize()[0]
category_id_df = df[[key, 'category_id']].drop_duplicates().sort_values('category_id')

category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', key]].values)

print (df.head())



title_tfidf = TfidfVectorizer(sublinear_tf=True,  # logarithmic form for frequency
                        min_df=5,  # minimum numbers of documents a word must be present in to be kept
                        norm='l2',  # norm is set to l2, to ensure all our feature vectors have a euclidian norm of 1
                        encoding='latin-1',  # utf-8 possible 
                        ngram_range=(1, 2),  # (1, 2) to indicate that we want to consider both unigrams and bigrams
                        stop_words='english'  # remove common pronouns ("a", "the", ...) to reduce the number of noisy features
                       )

# Title features:
title_features = title_tfidf.fit_transform(df[value]).toarray()  # title 
title_labels = df.category_id  # categories (cond-mat)
print ('title_features.shape',title_features.shape)  # titles represented by features, representing tf-idf score for different unigrams and bigrams

"""
N = 2  # number of correlated items to display
for title, category_id in sorted(category_to_id.items()):
    features_chi2 = chi2(title_features, title_labels == category_id)
    indices = np.argsort(features_chi2[0])
    feature_names = np.array(title_tfidf.get_feature_names_out())[indices]
    unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
    bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
    print("# '{}':".format(title))
    print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
    print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))
"""



########################################

models = [
    RandomForestClassifier(), #n_estimators=200, max_depth=3, random_state=0),
    LinearSVC(),
    MultinomialNB(),
    LogisticRegression(random_state=0),  # try: multi_class='multinomial', solver='lbfgs'...same accuracy actually
]

CV = 5  # n-fold cross-validation
cv_df = pd.DataFrame(index=range(CV * len(models)))
entries = []
for model in models:
  model_name = model.__class__.__name__
  accuracies = cross_val_score(model, title_features, title_labels, scoring='accuracy', cv=CV)  # features: ; labels: 
  for fold_idx, accuracy in enumerate(accuracies):
    entries.append((model_name, fold_idx, accuracy))
cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])

print(cv_df)
# Visualize model accuracy with box plot and strip plot:
import seaborn as sns
sns.boxplot(x='model_name', y='accuracy', data=cv_df)
sns.stripplot(x='model_name', y='accuracy', data=cv_df, 
              size=8, jitter=True, edgecolor="gray", linewidth=2)

plt.ylim(0, 1)
#plt.title('Model Benchmark Comparison from Title Text Data')
plt.ylabel('Accuracy (cross-validation score)')
#plt.xlabel('Model')
plt.xticks(rotation = 45)
plt.tight_layout()
plt.savefig('cv.png')
plt.close()


model = LinearSVC()
X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(title_features, title_labels, df.index, test_size=0.33, random_state=0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
from sklearn.metrics import confusion_matrix
conf_mat = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(10,10))
sns.heatmap(conf_mat, annot=True, fmt='d',
            xticklabels=category_id_df[key].values, yticklabels=category_id_df[key].values)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.tight_layout()
plt.savefig('conf.png')
plt.close()
