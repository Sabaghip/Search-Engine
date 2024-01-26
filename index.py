import heapq
import pickle
import preprocess
    
class PositionalPosting:
    def __init__(self, doc_id: int, tf : int, positions):
        self.doc_id = doc_id
        self.tf = tf
        self.positions = positions

    def getDocID(self):
        return self.docID

    def getTF(self):
        return self.tf

    def getPositions(self):
        return self.positions

class PostingsList:
    def __init__(self):
        self.df = 0
        self.list = []
        self.tf = 0
        self.champions = []

    def getPostings(self):
        return self.list

    def getTf(self):
        frequency = 0
        for posting in self.list:
            frequency += posting.getTF()
        
        self.tf = frequency
        return frequency
    
    def getDF(self):
        return self.df

    def addPosting(self, p: PositionalPosting):
        self.list.append(p)

    def addDF(self):
        self.df += 1
    
    def getAllDocIdTF(self):
        res = []
        for p in self.list:
            res.append((p.getDocID(), p.getTF()))
        return res

    def addChampion(self, p):
        self.list.append(p)

class InvertedIndex:
    def __init__(self, docs_num : int):
        self.dict = {}
        self.docs_num= docs_num
        self.champions = {}

    def getPostingList(self, term: str) -> PostingsList:
        if term not in self.dict:
            return None
        return self.dict[term]

    def getdocsNum(self):
        return self.docs_num
        
    def addPosting(self, term: str, doc_id: int, tf: int, positions = None):
        if term not in self.dict:
            self.dict[term] = PostingsList()
        
        self.dict[term].addDF()
        self.dict[term].addPosting(PositionalPosting(doc_id, tf, positions))

        if tf >= 3:
            if term not in self.champions:
                self.champions[term] = PostingsList()
            self.champions[term].addPosting(PositionalPosting(doc_id, tf, positions))


    def deleteRepeatedWords(self, k: int):
        heap = []
        for key in self.dict:
            heapq.heappush(heap, (-self.dict[key].getTf(), key))
        remove_list = []
        for _ in range(k):
            item = heapq.heappop(heap)
            self.delete(item[1])
            remove_list.append(item)
        
        heap = []
        for key in self.champions:
            heapq.heappush(heap, (-self.champions[key].getTf(), key))
        champion_remove_list = []
        for _ in range(k):
            item = heapq.heappop(heap)
            self.deleteChamp(item[1])
            champion_remove_list.append(item)
        
        return [(-key, value) for key, value in remove_list] ,[(-key, value) for key, value in champion_remove_list] 

    def delete(self, term):
        self.dict.pop(term)

    def deleteChamp(self, term):
        self.champions.pop(term)

    def save(obj, path, mode):
        with open(path, mode) as file:
            pickle.dump(obj, file)
        print(f"{obj} saved.")

    
    def load(path, mode):
        with open(path, mode) as file:
            obj = pickle.load(file)
        return obj



def create_index(data, delete):
    inverted = InvertedIndex(len(data))
    for i in range(len(data)):
        content = data[str(i)]['content']
        tokens = preprocess.preproccess(content)
        terms = {}
        for j in range(len(tokens)):
            if tokens[j] not in terms:
                terms[tokens[j]] = [0, []]

            terms[tokens[j]][0] += 1
            terms[tokens[j]][1].append(j + 1)

        for key in terms:
            inverted.addPosting(key, i + 1, terms[key][0], terms[key][1])

        if i % 1000 == 0:
            print("docs processed: ", i)
    print("processing finished\ndeleting for inverted...")
    inverted_deletes = inverted.deleteRepeatedWords(delete)
    print("normal deletes = ", inverted_deletes[0])
    print("champion deletes = ", inverted_deletes[1])
        
    return inverted
