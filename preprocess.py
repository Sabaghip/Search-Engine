import json
from hazm import Lemmatizer
from hazm import Stemmer


   

space = ' '
space_chars = [' ', '\t', '\n', '\xa0']
special_subwords_before = ["می", "نمی"]
special_subwords_after = ["ی", "ای", "ها", "های", "هایی", "تر", "تری", "ترین", "گر", "گری", "وری", 
                           "ام", "ات", "اش", "مان", "تان", "شان", "گانه", ]
to_be_deleted_chars = ['\u064b', '\u064c', '\u064d', '\u064e', '\u064f', '\u0650',
                 '\u0651', '\u0621', '\u0652', '\u0670', '\u0654', '\u0640',
                 '۞', '۩','\ufdf2', '\u0611', '\u0612', '\u0613',
                 '\u0614', '\u0615', '\u0616', '\u0617', '\u0618', '\u0619',
                 '\u0620', '!', ',', '?', ':', '،', '؛', '.', '(', ')', '؟', '«', '»',
                 '#', '*', '《', '》', '\"', '[', ']', '{', '}', '-', '/']
special_space = '|'
abbrs = {"AFC":"کنفدراسیون فوتبال آسیا", "(AFC)":"کنفدراسیون فوتبال آسیا", "NBA":"اتحادیۀ ملی بسکتبال", 
"(NBA)":"اتحادیۀ ملی بسکتبال", "NFL":"لیگ ملی فوتبال", "(NFL)":"لیگ ملی فوتبال", 
"IWF":"فدراسیون جهانی وزنه برداری", "(IWF)":"فدراسیون جهانی وزنه برداری",
 "IOC":"کمیته بین المللی المپیک", "(IOC)":"کمیته بین المللی المپیک", 
 "JNTO":"سازمان گردشگری ژاپن", "(JNTO)":"سازمان گردشگری ژاپن", "VAR":"کمک داور ویدیویی", 
 "(VAR)":"کمک داور ویدیویی", "CAS":"دادگاه داوری ورزشی", "(CAS)":"دادگاه داوری ورزشی", 
 "Covid":"کرونا", "(Covid)":"کرونا"}
numbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']

should_change_to = {'ئ': 'ی', 'ي': 'ی', 'یٰ':'ی', 'ك': 'ک', 'آ': 'ا',
              'أ': 'ا', 'ٱ': 'ا', 'إ': 'ا', 'ة': 'ه', 'ۀ': 'ه', 'ؤ': 'و','0': '۰','1': '۱', '2': '۲', '3': '۳', '4': '۴',
              '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹', '-': ' ', '/': ' ', '\\': ' ', '_': ' ', 'ـ': ' ','%': "درصد", '٪': "درصد",


              '\u0020': space, '\u00a0': space, '\u0009': space, '\u000a': space,'\u2002': space, '\u2003': space, 
              '\u2004': space, '\u2005': space,'\u2006': space, '\u2007': space, '\u2008': space, '\u2009': space,
              '\u200a': space,'\u200c': space, '\u200B': space, '\u200D': space, '\u00ad': space,'\xad': space, '\u200f': space,


              '﷽': "بسم-الله-الرحمن-الرحیم", 'ﷻ': "الله-جل-جلاله",
              'ﷺ': "صلی-الله-علیه-وسلم", 'ﷲ': "الله", 'ﷳ': "اکبر",
              'ﷴ': "محمد", 'ﷵ': "صلی-الله-علیه-وسلم", 'ﷶ': "رسول",
              'ﷷ': 'علیه-السلام', 'ﷸ': "صلی-الله-علیه-وسلم", 'ﷹ': "صلی-الله-علیه-وسلم",
              }

lem = Lemmatizer()
stem = Stemmer()


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
    if "".join(word) in abbrs:
        for j in abbrs["".join(word)].split():
            output.append(j)
    else:
        output.append("".join(word))
    return output

def normalize(input:list[str])->list[str]:
    output = []
    for i in range(len(input)):
        if '@' not in input[i]:
            k=0
            number_flag = False
            word = []
            for j in range(len(input[i])):
                if input[i][j] in should_change_to:
                    word.append(should_change_to[input[i][j]])
                else:
                    word.append(input[i][j])
                if word[j] in to_be_deleted_chars or (number_flag and word[j] not in numbers):
                    output.append("".join(word[k:j]))
                    k = j + 1
                    number_flag = False
                elif word[j] in numbers and not number_flag:
                    output.append("".join(word[k:j]))
                    k = j + 1
                    number_flag = True 

            if len(word[k:]) > 0:
                output.append("".join(word[k:]))

            if input[i] in special_subwords_after:
                temp = output.pop()
                temp2 = output.pop()
                output.append(temp2 + "|" + temp)
                continue
        
        else:
            output.append(input[i])

    return output

def stemming(input:list[str])->list[str]:
    output = []
    for i in input:
        temp = stem.stem(i)
        if len(temp) < 3:
            temp = i
        output.append(lem.lemmatize(temp, 'V'))
    return output

def preproccess(input : str)->list[str]:
    tokenized = tokenize(input)
    normalized = normalize(tokenized)
    output = stemming(normalized)
    return output