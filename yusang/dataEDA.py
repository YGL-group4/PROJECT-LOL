import pandas as pd
import seaborn as sns

df = pd.read_csv('yusang/challenger_log_rev.csv')

df_win = df[df['win'] == 1]
df_win = df_win.drop(['win'], axis=1)

df_lose = df[df['win'] == 0]
df_lose = df_lose.drop(['win'], axis=1)

# correlation
sns.heatmap(df_win.corr(), annot=True)
sns.heatmap(df_lose.corr(), annot=True)


