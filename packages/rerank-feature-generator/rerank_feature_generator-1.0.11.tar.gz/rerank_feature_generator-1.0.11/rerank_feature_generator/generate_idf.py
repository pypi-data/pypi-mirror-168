import re
import jieba
import math




def _read_txt(filename):
    sentences = []
    with open(filename, "r") as f:
        for line in f:
            res = re.split("[,，。.、;；\'\"\(\)“（）【】\[\]\?？:：!！\\s+]", line)
            sentences.extend(res)
    sentences = list(set(sentences))
    return sentences



filename = "tmp.txt"
#utils.json2txt(output_file=filename)
sentences = set()
for i in range(0, 30):
    f_n = str(i) + "_" + filename
    print(f_n)
    tmp = _read_txt(f_n)
    sentences = sentences.union(set(tmp))

di = dict()
for i, sentence in enumerate(sentences):
    if i % 100000 == 0:
        print(i)
    word_cut = set(jieba.lcut(sentence))
    for word in word_cut:
        di[word] = di.get(word, 0) + 1

with open("idf.txt", "w") as f:
    for word in di:
        f.write(str(word) + "\t" + str(math.log(len(sentences) / (di[word] + 1))) + "\n")





