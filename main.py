import json
import index

with open("G:/IR-Project/IR_data_news_12k.json", 'r') as file:
    data = json.load(file)

index.create_index(data)