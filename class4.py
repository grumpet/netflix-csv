import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

df = pd.read_csv('netflix_titles.csv', encoding='latin1')



country_count = df.groupby('country').size().nlargest(10)
country_count = country_count.sort_values(ascending=False)
print(country_count)
fig = plt.figure(figsize=(15, 15))
axs = fig.subplots(2)



# Plot the country counts
axs[0].bar(country_count.index, country_count.values)
axs[0].set_title('Movies by Country')
axs[0].set_xlabel('Country')
axs[0].set_xticklabels(country_count.index, rotation=90)


cast_count = {}
cast_list = df['cast'].dropna().tolist()
for i in cast_list:
    i = i.split(', ')
    for j in i:
        if j in cast_count:
            cast_count[j] += 1
        else:
            cast_count[j] = 1


top_ten_cast = Counter(cast_count).most_common(10)
# Plot the cast counts
cast_names, cast_counts = zip(*top_ten_cast)

axs[1].bar(cast_names, cast_counts)
axs[1].set_title('Most Common Cast Members in Movies')
axs[1].set_xlabel('Cast Member')
axs[1].set_ylabel('Number of Movies')
axs[1].set_xticklabels(cast_names, rotation=90)

# Show the plots
plt.tight_layout()
plt.show()