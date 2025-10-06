# step1_eda_scoring.py
import pandas as pd

# change path if needed
df = pd.read_csv("data-final-malaysia.csv")  

print("Rows,Cols:", df.shape)
print("Columns sample:", df.columns[:40].tolist())

# quick count of country (confirm Malaysia rows)
if 'country' in df.columns:
    print(df['country'].value_counts().head())

# --- 30-item mapping (adjust if column names differ) ---
traits = {
    'Extraversion': ['EXT1','EXT3','EXT5','EXT7','EXT9','EXT10'],
    'Agreeableness': ['AGR2','AGR4','AGR6','AGR8','AGR9','AGR1'],
    'Conscientiousness': ['CSN1','CSN3','CSN5','CSN7','CSN9','CSN6'],
    'Openness': ['OPN1','OPN3','OPN5','OPN7','OPN9','OPN2'],
    'Neuroticism': ['EST1','EST3','EST5','EST6','EST9','EST2']
}

# Which items are reverse-scored (from codebook)
reverse_items = {'EXT10','AGR1','CSN6','OPN2','EST2'}

# make sure columns exist
missing = [c for t in traits.values() for c in t if c not in df.columns]
if missing:
    print("Missing columns from CSV:", missing)
else:
    # reverse score: new = 6 - response (1..5)
    for col in reverse_items:
        df[col+'_rev'] = 6 - df[col]
        # use reversed column name in traits mapping
    # build trait scores
    trait_scores = {}
    for trait, items in traits.items():
        cols = []
        for c in items:
            if c in reverse_items:
                cols.append(c + '_rev')
            else:
                cols.append(c)
        df[trait + '_raw'] = df[cols].sum(axis=1)
        trait_scores[trait] = (df[trait + '_raw'].min(), df[trait + '_raw'].max(), df[trait + '_raw'].mean())
    print("Trait score ranges & means:")
    for t, stats in trait_scores.items():
        print(t, "min,max,mean =", stats)

    # save a small sample
    print(df[['Extraversion_raw','Agreeableness_raw','Conscientiousness_raw','Openness_raw','Neuroticism_raw']].head())

    # write sample
    df[['Extraversion_raw','Agreeableness_raw','Conscientiousness_raw','Openness_raw','Neuroticism_raw']].head(10).to_csv('sample_trait_scores.csv', index=False)
    print("Saved sample_trait_scores.csv")