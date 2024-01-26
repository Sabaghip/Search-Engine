import json


space_chars = [' ', '\t', '\n', '\xa0']
special_subwords_before = ["می", "نمی"]
special_space = '|'
abbrs = {"AFC":"کنفدراسیون فوتبال آسیا", "(AFC)":"کنفدراسیون فوتبال آسیا"}


with open("G:/IR-Project/IR_data_news_12k.json", 'r') as file:
    data = json.load(file)

def tokenize(input:str)->list[str]:
    output = []
    word = []
    for i in range(len(input)):
        if input[i] in space_chars:
            if len(word) < 1:
                continue
            #check verbs
            if "".join(word) in special_subwords_before:
                word.append(special_space)
                continue
            #check abbrevations
            if "".join(word) in abbrs:
                output.append(abbrs["".join(word)])
                word = []
                continue
            #check id and email
            if('@' in word):
                if len(word) == 1:
                    temp = output.pop()
                    output.append("@" + "".join(temp))
                    word = []
                    continue
                elif word[-1] == '@':
                    output.append("@" + "".join(word[:-1]))
                    word = []
                    continue

            output.append("".join(word))
            word = []
        else:
            word.append(input[i])
    return output

def normalize(input:list[str])->list[str]:
    return input

def stem(input:list[str])->list[str]:
    return input

def preproccess(input : str)->list[str]:
    tokenized = tokenize(input)
    normalized = normalize(tokenized)
    output = stem(normalized)
    return output

for i in range(len(data)):
    content = data[str(i)]['content']
    tokens = preproccess(content)
    doc_terms = {}
    for j in range(len(tokens)):
        if '@' in tokens[j]:
            print(tokens[j])
        if tokens[j] not in doc_terms:
            doc_terms[tokens[j]] = [0, []]
        
        doc_terms[tokens[j]][0] += 1
        doc_terms[tokens[j]][1].append(j + 1)
    

#     if (i + 1) % 500 == 0:
#         print("done processing doc: ", i + 1)
#for i in range(len(temp)):
#    print("".join(temp[i]))