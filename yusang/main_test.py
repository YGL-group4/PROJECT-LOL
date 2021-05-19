

# from mod import lol_api
# key = lol_api.get_api_key()

from mod import lol_api
df_challenger = lol_api.get_challenger_df()
print(df_challenger)