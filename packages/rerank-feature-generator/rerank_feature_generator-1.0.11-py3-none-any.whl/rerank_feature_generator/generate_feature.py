# *tf-idf
# *idf的sum, min, max, mean, variance
# *词频数的sum, min, max, mean, variance
# *Query-doc相似度得分（es bm25）
# *doc包含query词数，比例
from collections import Counter
import os
import rerank_feature_generator.utils as utils

_get_module_path = lambda path: os.path.normpath(os.path.join(os.getcwd(),
                                                 os.path.dirname(__file__), path))

class Extractor:
    def __init__(self):
        self.idf = utils.read_file(_get_module_path("idf.txt"))
        self.default_idf = max(self.idf.values())


    def get_tf(self, cut_word):
        if len(cut_word) == 0:
            return [0, 0, 0, 0, 0]
        di = dict(Counter(cut_word))
        v = di.values()
        sum_value = sum(v)
        min_value = min(v)
        max_value = max(v)
        mean_value = sum_value/len(v)
        variance_value = sum([(elem - mean_value)**2 for elem in v])/len(v)
        return [sum_value, min_value, max_value, mean_value, variance_value]


    def get_idf(self, cut_word):
        if len(cut_word) == 0:
            return [0, 0, 0, 0, 0]
        v = [self.idf.get(w, self.default_idf) for w in cut_word]
        sum_value = sum(v)
        min_value = min(v)
        max_value = max(v)
        mean_value = sum_value / len(v)
        variance_value = sum([(elem - mean_value) ** 2 for elem in v]) / len(v)
        return [sum_value, min_value, max_value, mean_value, variance_value]


    def get_tf_idf(self, cut_word):
        if len(cut_word) == 0:
            return [0, 0, 0, 0, 0]
        di = dict(Counter(cut_word))
        v = [self.idf.get(w, self.default_idf) * di[w] for w in cut_word]
        sum_value = sum(v)
        min_value = min(v)
        max_value = max(v)
        mean_value = sum_value / len(v)
        variance_value = sum([(elem - mean_value) ** 2 for elem in v]) / len(v)
        return [sum_value, min_value, max_value, mean_value, variance_value]


    def get_query_doc_sim(self, sim):
        return [sim]


    def get_coverage_ratio(self, query_cut_word, doc_cut_word):
        if len(query_cut_word) == 0 or len(doc_cut_word) == 0:
            return [0, 0, 0, 0]
        q_count, d_count = 0, 0
        for q in query_cut_word:
            if q in doc_cut_word:
                q_count += 1

        for d in doc_cut_word:
            if d in query_cut_word:
                d_count += 1
        return [q_count, d_count, q_count/len(query_cut_word), d_count/len(doc_cut_word)]


    def combine_features(self, query_cut_word, doc_cut_word, doc_content_cut_word, sim):
        query_tf_res = self.get_tf(query_cut_word)
        doc_tf_res = self.get_tf(doc_cut_word)
        doc_content_tf_res = self.get_tf(doc_content_cut_word)
        query_idf_res = self.get_idf(query_cut_word)
        doc_idf_res = self.get_idf(doc_cut_word)
        doc_content_idf_res = self.get_idf(doc_content_cut_word)
        query_tf_idf = self.get_tf_idf(query_cut_word)
        doc_tf_idf = self.get_tf_idf(doc_cut_word)
        doc_content_tf_idf = self.get_tf_idf(doc_content_cut_word)
        query_doc_sim = self.get_query_doc_sim(sim)
        coverage_ratio = self.get_coverage_ratio(query_cut_word, doc_cut_word)
        content_coverage_ratio = self.get_coverage_ratio(query_cut_word, doc_content_cut_word)
        res = query_tf_res + doc_tf_res + doc_content_tf_res + query_idf_res + doc_idf_res +\
              doc_content_idf_res + query_tf_idf + doc_tf_idf + doc_content_tf_idf + query_doc_sim +\
              coverage_ratio + content_coverage_ratio
        return res



# import jieba
# et = Extractor()
# query_cut_word = jieba.lcut("股票市盈率大于苊苊🔥囧")
# doc_cut_word = jieba.lcut("股票市盈率小的股票完2让客人")
# doc_content_cut_word = jieba.lcut("股票市盈率小的股票完2让客人股票市盈率小的股票股票市盈率小的股票股票市盈率小的股票股票市盈率小的股票股票市盈率小的股票,股票市盈率小的股票")
# res = et.combine_features(query_cut_word, doc_cut_word, doc_content_cut_word, 1.2)
# print(res)


