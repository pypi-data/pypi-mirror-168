import jieba
import jieba.analyse
# import numpy as np
import re
from simhash import Simhash, SimhashIndex
# import nltk
from collections import Counter
# from nltk.corpus import stopwords
# # 分词
# from nltk.tokenize import word_tokenize
# nltk.download('stopwords')
# stopwords.words('english')
def tosrt(x):
    """
    16进制数字转换成字符串

    :param x:
    :return:
    """
    b = bin(x)[2:].zfill(64)
    return b


def pre_clear_text(text):
    """
    The pre_clear_text function removes stop words from a text.
    It takes in a string and returns the cleaned string.

    :param text: Used to Pass the text that needs to be pre-cleared.
    :return: A list of words in the text.

    :doc-author: Trelent
    """
    """
    预先清理文本，英文


    """
    # stop_words = stopwords.words('english')
    # stopwords_dict = Counter(stop_words)
    text=text.lower()

    # text = ' '.join([word for word in word_tokenize(text) if word not in stopwords_dict])
    # words=[word for word in word_tokenize(text) if word not in stopwords_dict]
    # words=word_tokenize(text)
    words=text.split(" ")

    return words


    pass

class simHash(object):
    """
    simhash包含分词、hash、加权、合并、降维五大步骤
    https://www.notion.so/terrychanorg/python-Simhash-_Python_-6b394a0d452340a8938b08c16ce15a41
    ## 降维比较
    MySQL存储索引方案

    - 将simhash等分4份，每份16位，为subCode
    - 将sub_code存储到mysql
    - 对于新SimHash，等分4份subCode，通过subCode查询集合
    - 遍历结果，计算最终汉明距离

    ## 9 SimHash的利弊

    - **优点：**
        - 速度快，效率高。通过分割鸽笼的方式能将相似的数据快速定位在某个区域内，减少99%数据的相似对比。
        - 通过大量测试，SimHash用于比较大文本，效果很好，距离小于3的基本都是相似，误判率也比较低。
    - **缺点:**
        - 对短文本召回效果不太好。
        - 在测试短文本的时候看起来相似的一些文本海明距离达到了10,导致较多的漏召回。
    https://www.notion.so/terrychanorg/c59bb535b95947419eae79b5f2ea75f4#c71767fc4a9f405f9959817dac7cdfb4
    """

    def __init__(self, topK=100,lang="en", **kwargs):
        # 限制关键词数目
        self.topK = topK
        self.lang = lang
        pass

    def simhash(self, content: str) -> str:
        """
        获取海明编码


        :param content:
        :return:
        """
        # print("Simhash(words).tosrt", tosrt(Simhash(words).value))
        # 对中文进行分词
        if self.lang=="zh":
            seg = jieba.cut_for_search(content)  # 搜索引擎模式
            # words = (", ".join(seg)).split(", ")
            words =" ".join(seg)
        else:
            # 对英文进行 切割单词处理
            # words=content.replace("\n"," ").repalce("\t"," ").split(" ")
            # 做批量小写处理
            # words=content.lower().split(" ")
            # 清理停用词等
            words=pre_clear_text(content)
            # words=content
            words=" ".join(words)
        simhash = tosrt(Simhash(words).value)
        return simhash

    #
    #     def autohash(self, content_list: list) -> str:
    #         """
    #         获取列表的海明编码
    #
    #
    #         :param content:
    #         :return:
    #         """
    #         for it in content_list:
    #             yield self.simhash(it)
    #
    #     def string_hash(self, source: str) -> str:
    #         if source == "":
    #             return 0
    #         else:
    #             temp = source[0]
    #             temp1 = ord(temp)
    #             x = ord(source[0]) << 7
    #             m = 1000003
    #             mask = 2 ** 128 - 1
    #             for c in source:
    #                 x = ((x * m) ^ ord(c)) & mask
    #             x ^= len(source)
    #             if x == -1:
    #                 x = -2
    #             x = bin(x).replace('0b', '').zfill(64)[-64:]
    #
    #             return str(x)
    #
    def getdistance(self, hashstr1: str, hashstr2: str) -> int:
        '''
        计算两个simhash的汉明距离
        根据经验，一般当两个文档特征字之间的汉明距离小于 3， 就可以判定两个文档相似。《数学之美》一书中，在讲述信息指纹时对这种算法有详细的介绍。

        3< 相似
        10 <相似度极高
        '''
        length = 0
        for index, char in enumerate(hashstr1):
            if char == hashstr2[index]:
                continue
            else:
                length += 1

        return length

    def similarity(self, a: str, b: str):
        """
        # 求相似度

        :param otherhash:
        :return:
        """
        a = float(a)
        b = float(b)
        try:
            if a > b:
                return b / a
            else:
                return a / b
        except:
            return 0

    def subcode(self, myhash: str) -> list:
        """
        生成subCode，用于检索

        MySQL存储索引方案

        - 将simhash等分4份，每份16位，为subCode
        - 将sub_code存储到mysql
        - 对于新SimHash，等分4份subCode，通过subCode查询集合
        - 遍历结果，计算最终汉明距离

        将hash分成四段
        但问题是，我怎么知道差异位点分布在哪一部分？

        所以，一段文本的Simhash指纹，我们需要复制成四次存储，以text1为例，simhash 成64位之后，我们分成四个部分，A1-A2-A3-A4。我们把这段存储四份，以使得每一部分都做一次K，剩下其他三个为V：

        ① K: A1, V: A2-A3-A4

        ② K: A2, V: A1-A3-A4

        ③ K: A3, V: A1-A2-A4

        ④ K: A4, V: A1-A2-A3

        对于两段文本，我们分别映射成64位hash指纹之后，再每个文本分为四份，每个部分16位。对于这两段文本，如果海明距离在3以内，则它们对应的4个部分，至少有一个部分是一样的。

        因为，海明距离小于3，意味着，最多有3个位点有区别，而3个差异位点分布在四个部分，至少有一个部分是没有相同的。


        这就好比把3个球放到4个抽屉里面，一定有一个抽屉是空的，所以叫“抽屉原理”。



        这样就可以保证不会有遗漏。
        https://www.notion.so/terrychanorg/Simhash-2-4-2-0ce054d237cd4c2d86a5a385a36a6f8c
        https://cloud.tencent.com/developer/article/1189493

        :param myhash:
        :return:
        """
        out = []
        for i in range(0, 4):
            # print(i*16)
            # print(a[i * 16:(i + 1) * 16])
            out.append(myhash[i * 16:(i + 1) * 16])
        return out

    def autoencode(self,text_list: list) -> list:
        """
        自动获取simhash 用于存储索引
        The autoencode function takes a string as input and returns a dictionary with two keys:
        subcode, which is the sub-hash code of the simhash, and code, which is the full hash.

        :param self: Used to Access the class attributes.
        :param text:str: Used to Pass the text that will be encoded.
        :return: A dictionary with two keys: subcode and code.

        :doc-author: Trelent
        """
        items=[]
        for text in text_list:
            code=self.simhash(text)
            subcode=self.subcode(code)
            items.append(dict(subcode=subcode,code=code))
        return items



#
# #
# # text1 = '我很想要打游戏，但是女朋友会生气！'
# # text2 = '我很想要打游戏，但是女朋友非常生气！'
# # a = simHash().simhash(text1)
# # b = simHash().simhash(text2)
# # print(a)
# # print(b)
# # print(simHash().getdistance(a, b))


# text1 = '我很想要打游戏，但是女朋友会生气！'
# sim = simHash()
# print(sim.simhash(text1))
