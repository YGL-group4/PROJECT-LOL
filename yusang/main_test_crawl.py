from module import lol_api
from module import crawling

df1 = lol_api.get_challenger_df()
df2 = lol_api.get_grandmaster_df()
print(df1)

data1 = crawling.get_data(df1)
print("Done 1")
crawling.save_data(data1, 'challenger_0521.csv')

data2 = crawling.get_data(df2)
print("Done 2")
crawling.save_data(data2, 'grandmaster_0521.csv')

print("All done")

