import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib

# load dataset with trait scores
df = pd.read_csv("data-final-malaysia.csv")

# ---- re-use trait score logic (copy from step1) ----
traits = {
    'Extraversion': ['EXT1','EXT3','EXT5','EXT7','EXT9','EXT10'],
    'Agreeableness': ['AGR2','AGR4','AGR6','AGR8','AGR9','AGR1'],
    'Conscientiousness': ['CSN1','CSN3','CSN5','CSN7','CSN9','CSN6'],
    'Openness': ['OPN1','OPN3','OPN5','OPN7','OPN9','OPN2'],
    'Neuroticism': ['EST1','EST3','EST5','EST6','EST9','EST2']
}
reverse_items = {'EXT10','AGR1','CSN6','OPN2','EST2'}

for col in reverse_items:
    df[col+'_rev'] = 6 - df[col]

for trait, items in traits.items():
    cols = []
    for c in items:
        if c in reverse_items:
            cols.append(c+'_rev')
        else:
            cols.append(c)
    df[trait+'_raw'] = df[cols].sum(axis=1)

X = df[['Openness_raw','Conscientiousness_raw','Extraversion_raw','Agreeableness_raw','Neuroticism_raw']].fillna(0).values

# standardize
scaler = StandardScaler().fit(X)
Xs = scaler.transform(X)

# train kmeans (try k=4 first)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = kmeans.fit_predict(Xs)

df['cluster'] = labels
print("Cluster counts:")
print(df['cluster'].value_counts())

# save models
joblib.dump(scaler, 'scaler.joblib')
joblib.dump(kmeans, 'kmeans.joblib')

# save sample output
df[['Openness_raw','Conscientiousness_raw','Extraversion_raw','Agreeableness_raw','Neuroticism_raw','cluster']].head(10).to_csv('sample_clusters.csv', index=False)
print("Saved sample_clusters.csv")