import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies.db'
table_name = 'Top_50'
csv_path = '/home/project/top_50_films.csv'
df = pd.DataFrame(columns = ['Average Rank', 'Film', 'Year'])
count = 0

# convert page to html to read
html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')
# find table and store in variable
tables = data.find_all('tbody')
# find rows and store in variable
rows = tables[0].find_all('tr')


# loop that goes over each row and creates empty dict with same
# column vals as df then adds each row of data from said columns
# until count = 50 so the top 50 movies from the table
for row in rows:
    if count < 50:
        col = row.find_all('td')
        if len(col) != 0:
            data_dict = {"Average Rank": int(col[0].contents[0]),
                         "Film": str(col[1].contents[0]),
                         "Year": int(col[2].contents[0])}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df, df1], ignore_index=True)
            count += 1
    else:
        break
print(df)
# Save data frame to CSV file
df.to_csv(csv_path)

conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()














