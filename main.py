import json
import index

with open("IR_data_news_5k 2.json", 'r') as file:
    data = json.load(file)
print(len(data))

inverted = index.create_index(data, delete=50)

print("saving inverted...")
index.InvertedIndex.save(inverted, "G:/IR-Project/test.pkl", "wb")
print("saved.")