


def preproccess(input : str)->list[str]:
    normalized = normalize(input)
    tokenized = tokenize(normalized)
    output = stem(tokenized)
    return output

def tokenize(input:str)->list[str]:
    pass

def normalize(input:str)->str:
    pass

def stem(input:list[str])->list[str]:
    pass