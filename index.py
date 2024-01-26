import preprocess

def create_index(data):
    for i in range(len(data)):
        content = data[str(i)]['content']
        tokens = preprocess.preproccess(content)
        terms = {}
        for j in range(len(tokens)):
            if tokens[j] not in terms:
                terms[tokens[j]] = [0, []]

            terms[tokens[j]][0] += 1
            terms[tokens[j]][1].append(j + 1)

        if (i + 1) % 500 == 0:
            print("done processing doc: ", i + 1)