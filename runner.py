import time
import json
import queryrunner
import index

def print_results(query, result):
    for i in range(len(result)):
        temp = str(int(result[i][0]) - 1)
        print("doc_id: ", temp, "\nScore: ", result[i][1], "\nTitle: ", data[temp]['title'] ,"\nURL: ", data[temp]['url'])
        print("In doc:\n")
        content = data[temp]['content'].split()
        for i in range(len(content)):
            if content[i]==query.split()[0]:
                if i < 6:
                    print("".join(content[:10]))
                elif i > len(content) - 5:
                    print("".join(content[i-5:]))
                else:
                    print("".join(content[i-5:i+5]))
                print("============================================================\n============================================================")
        print("\n------------------------------------------------------------\n------------------------------------------------------------\n")


with open("G:/IR-Project/IR_data_news_12k.json", 'r') as file:
    data = json.load(file)

inverted = index.InvertedIndex.load("G:/IR-Project/ii-deleted-terms.pkl", "rb")
queryrunner = queryrunner.QueryProcessor(inverted)

while True:
    query = input("Enter query : ")
    if query == "exit:::":
        break
    start = time.time()
    result = queryrunner.findChampion(query, 10)
    end = time.time()
    print("time : ", end-start)
    print_results(query, result)