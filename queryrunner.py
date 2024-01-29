import index
import preprocess
from math import log10, sqrt
import heapq

class QueryProcessor:
    def __init__(self, index: index.InvertedIndex):
        self.index = index

    def findNormal(self, query: str, k: int):
        tokens = preprocess.preproccess(query.strip())
        remove_list = []
        for i in range(len(tokens)):
            pl = self.index.getPostingList(tokens[i])
            if pl is None:
                remove_list.append(i)
        for i in remove_list:
            tokens.pop(i)
        
        query_scores = {}
        query_frequency = {}
        for i in tokens:
            if i not in query_frequency:
                query_frequency[i] = 0
            query_frequency[i] += 1

        for i in query_frequency:
            query_scores[i] = 1 + log10(query_frequency[i])

        doc_scores = {}
        for i in tokens:
            scores = self.getScoreList(i)
            for id in scores:
                if id not in doc_scores:
                    doc_scores[id] = {}
                doc_scores[id][i] = scores[id]

        heap = []
        for docID, doc_vector in doc_scores.items():
            doc_score = self.getSimilarity(query_scores, doc_vector)
            heapq.heappush(heap, (-doc_score, docID))
        
        if len(heap) < k:
            k = len(heap)
        
        result = []
        for _ in range(k):
            neg_score, id = heapq.heappop(heap)
            result.append((id, -neg_score))
        
        return result
        
    def findChampion(self, query: str, k: int):
        tokens = preprocess.preproccess(query.strip())
        remove_list = []
        for i in range(len(tokens)):
            pl = self.index.getChampionPostingList(tokens[i])
            if pl is None:
                remove_list.append(tokens[i])
        for i in remove_list:
            tokens.remove(i)
        
        query_scores = {}
        query_frequency = {}
        for i in tokens:
            if i not in query_frequency:
                query_frequency[i] = 0
            query_frequency[i] += 1

        for i in query_frequency:
            query_scores[i] = 1.0 + log10(query_frequency[i])

        doc_scores = {}
        for i in tokens:
            scores = self.getScoreListChampion(i)
            for id in scores:
                if id not in doc_scores:
                    doc_scores[id] = {}
                doc_scores[id][i] = scores[id]
        heap = []
        for docID, doc_vector in doc_scores.items():
            doc_score = self.getSimilarity(query_scores, doc_vector)
            heapq.heappush(heap, (-doc_score, docID))

        if len(heap) < k:
            result = []
            for _ in range(len(heap)):
                neg_score, id = heapq.heappop(heap)
                result.append((id, -neg_score))
            normal_res = self.findNormal(query, 2 * k)
            for i in range(len(normal_res)):
                if normal_res[i] not in result:
                    result.append(normal_res[i])
        else:
            result = []
            for _ in range(k):
                neg_score, id = heapq.heappop(heap)
                result.append((id, -neg_score))
        return result 

    def getScoreList(self, token: str):
        scores = self.index.vertices
        postings = self.index.getPostingList(token)
        result = {}
        for i in postings.list:
            try:
                result[str(i.getDocID())] = scores[str(i.getDocID())][token]
            except:
                result[str(i.getDocID())]=0
        return result

    def getScoreListChampion(self, token: str):
        scores = self.index.vertices
        postings = self.index.getChampionPostingList(token)
        result = {}
        for i in postings.list:
            try:
                result[str(i.getDocID())] = scores[str(i.getDocID())][token]
            except:
                result[str(i.getDocID())] = 0
        return result

    def getSimilarity(self, vector1: dict, vector2: dict):
        squared_sum1 = 0.0
        squared_sum2 = 0.0

        for t in vector1:
            squared_sum1 += vector1[t] ** 2
        for t in vector2:
            squared_sum2 += vector2[t] ** 2
        
        squared_sum1 = sqrt(squared_sum1)
        squared_sum2 = sqrt(squared_sum2)

        score = 0.0
        for i in vector1:
            if i in vector2:
                try:
                    score += (vector1[i] / squared_sum1) * (vector2[i] / squared_sum2)
                except:
                    score += 0
        
        return score 