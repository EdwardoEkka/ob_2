import pandas as pd
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from pandas import Timestamp
from datetime import datetime
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
import json

file_path = 'video_details.json'

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Create a DataFrame
df = pd.DataFrame(data)

# Tokenize the titles with stop words
stop_words=[
    'for', 'couldn', 'hers', 'so', 'myself', 'themselves', 'each',
    's', 'from', 'why', 'aren', 'yours', 'can', 'such', 'the', 'into', 'on', 'now', "aren't",
    'does', 'my', 'and', 'you', 'him', 'she', 'at', 'up', "hasn't", 'between', 'what', 'there',
    'no', "don't", 'just', "isn't", 'ma', 'he', 'your',
    'than', 'didn', "shan't", "wouldn't", 'but', 'nor', 'of', 're', 'hasn', 'when', 'same', 'me', 'until',
    'weren', "that'll", 'don', 'll', 'these', 'too', 'o', 'whom', "you'll", "didn't", 'own', 'are', 't',
    'was', 'itself', 'having', 'about', 'should', 'once', 'has', 'under', 'while', "doesn't", "mustn't", 'this',
    'again', 'them', 'which', 'been', 'hadn', 'during', 'both', 'will', "weren't",
    'because', 'wasn', 'y', 'after', 'out', 'am', 'then', 'doing', 'any', 'through', 'most', "couldn't",
    'herself', 'her', 'an', 'm', 'himself', 'its', "won't", "you've", 'ain', 'it', 'needn', 'against', 'i',
    'other', 'haven', 'by', 'only', 'few', 'their', 'who',
    'ourselves', 'shouldn', 'more', 'is', 'have', 'isn', "needn't", "hadn't", 'our', 'ours', 'being', 'be', "mightn't", 'yourself', 'here',
    "haven't", "should've", 'his', 'down', 'yourselves', 'had', 'some', 'if', "she's", 'do', 'wouldn', 'were', 'where',
    "you'd", 'over', "wasn't", 'mightn',
    'in', 'all', 'a', 'further', 'shan', "shouldn't", "you're",
    'above', 'or', 'they', 'to', 'theirs', 'how', 'doesn', "it's", 'we', 'those', 'with', 'won', 'd', 've','news','did', 'very',
    'that', 'as', 'below', 'off', 'not', 'mustn', 'before','shorts','india','today','news','39','newsnight'
]

vectorizer = CountVectorizer(stop_words=stop_words)
X = vectorizer.fit_transform(df['title'])

# Topic modeling using Latent Dirichlet Allocation (LDA)
num_topics = 5  # Adjust as needed based on your data
lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
lda.fit(X.toarray())  # Convert the sparse matrix to an array before fitting

# Assign topics to each video
df['topic'] = lda.transform(X).argmax(axis=1)

# Display the results
topics_data = []

def create_sentence(words):
    tagged_words = pos_tag(words)
    sentence = ' '.join(word for word, pos in tagged_words)
    return sentence

print("Topic Modeling Results:")
for topic_idx, topic in enumerate(lda.components_):
    top_words = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-6:-1]]
    topic_name = f"Topic {topic_idx + 1}: {', '.join(top_words)}"
    result_sentence = create_sentence(top_words)
    print(topic_name)

    # Print titles for each topic
    titles_in_topic = df.loc[df['topic'] == topic_idx, 'title'].tolist()
    print(f"Titles in {topic_name}: {titles_in_topic}")

    df.loc[df['topic'] == topic_idx, 'topic'] = topic_name

    # Save topics and titles to the list
    topics_data.append({
        'topic_name': topic_name,
        'titles_in_topic': titles_in_topic
    })

# Save topics and titles to a separate JSON file
with open('model_3.json', 'w', encoding='utf-8') as json_file:
    json.dump(topics_data, json_file, ensure_ascii=False, indent=4)

# Trend analysis and visualization for each topic
df['publishedAt'] = pd.to_datetime(df['publishedAt'])
df.set_index('publishedAt', inplace=True)
df.sort_index(inplace=True)

# Create separate plots for each topic
for topic_name in df['topic'].unique():
    plt.figure(figsize=(20, 20))
    topic_df = df[df['topic'] == topic_name]
    x = pd.DatetimeIndex(topic_df.index).to_list()
    y = topic_df['likes'].values
    date_objects = [pd.to_datetime(timestamp) for timestamp in x]
    values = [int(value) for value in y]
    md = pd.DataFrame({'Timestamps': date_objects, 'Values': values})
    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(md['Timestamps'], md['Values'], marker='o', linestyle='-', color='b', label=topic_name)
    plt.title(f'Trend Analysis - Likes Over Time for {topic_name}')
    plt.xlabel('Timestamps')
    plt.ylabel('Likes')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.tight_layout()
    plt.show()
