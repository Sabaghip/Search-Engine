import json
import index

with open("G:/IR-Project/IR_data_news_12k.json", 'r') as file:
    data = json.load(file)


inverted = index.create_index(data, delete=50)

print("saving inverted...")
index.InvertedIndex.save(inverted, "G:/IR-Project/ii-deleted-terms.pkl", "wb")
print("saved.")