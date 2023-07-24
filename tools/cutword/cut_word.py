import re
from pkuseg import pkuseg
import jieba
import pandas
import pandas as pd
from collections import Counter
# from nltk.corpus import wordnet
from synonyms import synonyms

from TestTools.config.setconfig import get_dir
from TestTools.tools.cutword.cut_word_diy import doubleMax
import progress_bar
from TestTools.tools.opt_file.optFiles import ReadFileAsDF, writeToExcelFile


# jieba.enable_parallel(4) # 开启并行分词模式，参数为并行进程数
# jieba.disable_parallel() # 关闭并行分词模式
# 分词
def use_jiaba(df, col, cut_type=None, userdict_file=None):
    if isinstance(df, pd.DataFrame):
        col_name = df.columns.tolist()
        if col in col_name:
            if userdict_file is not None:
                jieba.load_userdict(userdict_file)  # 加载用户词典
            if cut_type is None or cut_type == 'cut':
                df[col + '_seg'] = df.apply(
                    lambda x: ','.join(jieba.cut(x[col], cut_all=False)), axis=1)
            elif cut_type == 'cut_all':
                df[col + '_seg'] = df.apply(
                    lambda x: ','.join(jieba.cut(str(x[col]).strip(), cut_all=True)), axis=1)
            elif cut_type == 'cut_for_search':
                df[col + '_seg'] = df.apply(
                    lambda x: ','.join(jieba.cut_for_search(x[col])), axis=1)
            elif cut_type == 'psg_cut':
                df[col + '_seg'] = df.apply(
                    lambda x: ','.join(jieba.posseg.cut(str(x[col]).strip(), cut_all=True)), axis=1)
            return df
        else:
            return 'df的列名错误'
    else:
        return 'df错啦！'


def use_pkuseg(df, col, model_name='defalut', userdict_file='defalut', postag=False):
    """
    :param df:
    :param col:
    :param model_name: "default"，默认参数，表示使用我们预训练好的混合领域模型(仅对pip下载的用户)。
					"news", 使用新闻领域模型。
					"web", 使用网络领域模型。
					"medicine", 使用医药领域模型。
					"tourism", 使用旅游领域模型。
			        model_path, 从用户指定路径加载模型。
    :param userdict_file:
    :return:
    """
    if isinstance(df, pd.DataFrame):
        col_name = df.columns.tolist()
        if col in col_name:
            seg = pkuseg(model_name=model_name, user_dict=userdict_file, postag=postag)  # 加载模型，给定用户词典
            if not postag:
                df[col + '_seg'] = df.apply(
                    lambda x: ','.join(seg.cut(str(x[col]).strip())), axis=1)
            else:
                df[col + '_seg'] = df.apply(
                    lambda x: seg.cut(str(x[col]).strip()), axis=1)
            return df
        else:
            return 'df的列名错误'
    else:
        return 'df错啦！'


# 双向最大匹配
def use_doubleMax(df, col, userdict_file=None):
    if isinstance(df, pd.DataFrame):
        col_name = df.columns.tolist()
        if col in col_name:
            if userdict_file is not None:
                df[col + '_seg'] = df.apply(
                    lambda x: ','.join(doubleMax(str(x[col]).strip(), userdict_file)), axis=1)
            return df
        else:
            return 'df的列名错误'
    else:
        return 'df错啦！'


# 创建固定词列表
def userdict(userdict_file):
    # strip() 方法用于移除字符串头尾指定的字符（默认为空格）
    userdict_words = [line.strip() for line in open(userdict_file, encoding='UTF-8').readlines()]
    return userdict_words


# 创建停用词列表
def load_stopword(stopword_file):
    # strip() 方法用于移除字符串头尾指定的字符（默认为空格）
    stopwords = [line.strip() for line in open(stopword_file, encoding='UTF-8').readlines()]
    return stopwords


# 创建同义词字典
def replaceSynonymWords(sy_file):
    # 读取同义词表，并生成字典。
    combine_dict = {}
    # sy_file是同义词表，每行是一系列同义词，用空格分割
    for line in open(sy_file, "r", encoding='utf-8'):
        seperate_word = line.strip().split(" ")
        num = len(seperate_word)
        for i in range(0, num):
            combine_dict[seperate_word[i]] = seperate_word[0]
    return combine_dict


# 英文单词分词
# def get_word_synonyms_from_sent(word, sent):
#     word_synonyms = []
#     for synset in wordnet.synsets(word):
#         for lemma in synset.lemma_names():
#             if lemma in sent and lemma != word:
#                 word_synonyms.append(lemma)
#     return word_synonyms


# # 2提升某些词的词频，使其能够被jieba识别出来
# jieba.suggest_freq("年休假", tune=True)


# 处理分词第一步：去掉单个词 和 停用词（标点符号在停用词表中)
def remove_stopword(df, col, stopword_file=None, postag=False):
    if isinstance(df, pd.DataFrame):
        col_name = df.columns.tolist()
        if col in col_name:
            if stopword_file is not None:
                # 去掉停用词 和长度小于2的分词
                stopwords = load_stopword(stopword_file)  # 停用词列表

            # pattern = "[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+"
            # num_pattern = "^([0-9]|几|一|二|三|四|五|六|七|八|九|十|百|千|万|亿|第|这|多|上百|上千|上万)+(" \
            #               "小时|分钟|秒|毫秒|颗|棵|是|篇|本|边|遍|部分|组|员|页|行|列|眼|条|种|人民币|美金|天|面|日|月|个|人|次|列|头|圈|年|世纪|米|厘米|毫米|微米|斤|千克|班级|匹|款|点)* "
            if postag:
                # 根据词性过滤
                filter_flag = ['n', 'nz', 'vn', 'm', 'i', 'z', 'j', 'nt', 'an', 'v']
                df[col + '_remove'] = df.apply(
                    lambda x: ' '.join(
                        x[0] if x[0] not in stopwords  # 分词不再在停用词库
                                and len(x[0]) >= 2  # 分词长度大于等于2
                                and x[1] in filter_flag
                        # and not re.match(num_pattern, x[0])  # 去掉量词
                        else '' for
                        x in
                        x[col]),
                    axis=1)
            else:
                df[col + '_remove'] = df.apply(
                    lambda x: ' '.join(
                        x if x not in stopwords  # 分词不再在停用词库
                             and len(x) >= 2  # 分词长度大于等于2
                             # and not re.match(num_pattern, x)  # 去掉量词
                        else '' for
                        x in
                        str(x[col]).split(',')),
                    axis=1)

            return df
        else:
            return 'df的列名错误'

    else:
        return 'df错啦！'


# 处理分词第二步：统计频次
def CountWords(df, col):
    if isinstance(df, pd.DataFrame):
        col_name = df.columns.tolist()
        if col in col_name:
            # 统计分词频次
            words_num = Counter()
            df.apply(
                lambda x: words_num.update(str(x[col].strip()).split()), axis=1)
            sort_word_num = sorted(words_num.items(), key=lambda x: x[1], reverse=True)  # 按照值从大到小排序
            word_df = pd.DataFrame(sort_word_num)
            word_df.columns = ['words', 'num']
            df = word_df.dropna(axis=0, how='any', subset=None, inplace=False)
            return df
        else:
            return 'df的列名错误'

    else:
        return 'df错啦！'


# 处理分词第三步：处理近义词
def getsynonyms(df, sy_file):
    final_df = pd.DataFrame(columns=('key_word', 'words', 'count'))
    combine_dict = replaceSynonymWords(sy_file)
    # 如果列表中的词语在同义词列表中，则该词纳入列表，频次+
    len_all = df.shape[0]
    for index2, row in df.iterrows():
        progress_bar(int(index2), len_all)
        word = str(row['words'])
        num = int(row['num'])
        if word in combine_dict:  # 分词在近义词库中，则
            key_word = combine_dict[word]
            if key_word not in list(final_df['key_word']):  # 如果同义词还未入final_dict ,则加入
                temp_df = pd.DataFrame([{'key_word': key_word, 'words': word, 'count': num}])
                final_df = pandas.concat([final_df, temp_df], ignore_index=True)  # ignore_index=True忽略temp_df的索引
            else:
                # 得到这列数据
                key_line = final_df.loc[final_df['key_word'] == key_word, ['words', 'count']]
                key_line['words'] += ',' + word
                key_line['count'] += num

                final_df.loc[final_df['key_word'] == key_word, 'words'] = key_line['words']
                final_df.loc[final_df['key_word'] == key_word, 'count'] = key_line['count']
                # print('3final_df:', final_df)

        else:  # 不在自定义的近义词库
            # 如果与final中的key_word是90%的近义词，则也加上
            # print('other:', word)
            i_count = 0
            if not list(final_df['key_word']):
                temp_df = pd.DataFrame([{'key_word': word, 'words': word, 'count': num}])
                final_df = pandas.concat([final_df, temp_df],
                                         ignore_index=True)  # ignore_index=True忽略temp_df的索引
            else:
                for i in list(final_df['key_word']):
                    r = synonyms.compare(word, i, seg=False)
                    if r >= 1:
                        # 得到这列数据
                        key_line = final_df.loc[final_df['key_word'] == i, ['words', 'count']]
                        key_line['words'] += ',' + word
                        key_line['count'] += num
                        final_df.loc[final_df['key_word'] == i, 'words'] = key_line['words']
                        final_df.loc[final_df['key_word'] == i, 'count'] = key_line['count']
                        break
                    else:
                        i_count += 1
                        if i_count == len(list(final_df['key_word'])):
                            temp_df = pd.DataFrame([{'key_word': word, 'words': word, 'count': num}])
                            final_df = pandas.concat([final_df, temp_df],
                                                     ignore_index=True)  # ignore_index=True忽略temp_df的索引
                        else:
                            continue
    return final_df


if __name__ == '__main__':
    from_read = get_dir('data_files/user_event', '在线作图.xlsx')

    kind_list = ['社交客户管理（SCRM）', '项目协作', '客户关系管理（CRM）', '商业智能（BI）', '协作文档', '企业直播',
                 '在线作图', '人事管理（eHR）', '研发项目管理']
    for i in kind_list:
        to_write = get_dir('data_files/user_event/comment', i + '.xlsx')
        df = ReadFileAsDF(from_read, i)
        df = use_jiaba(df, 'good_function', 'cut')
        writeToExcelFile(df, to_write, sheet_name='sheet')
        df = remove_stopword(df, 'good_function_seg')
        writeToExcelFile(df, to_write, sheet_name='sheet')
        df = CountWords(df, 'good_function_seg_remove')
        writeToExcelFile(df, to_write, sheet_name='sheet')
        final_df = getsynonyms(df)
        writeToExcelFile(final_df, to_write, sheet_name='sheet')
    for i in kind_list:
        to_write = get_dir('data_files/user_event/comment', i + '1.xlsx')
        df = ReadFileAsDF(from_read, i)
        df = use_jiaba(df, 'bad_function', 'cut')
        writeToExcelFile(df, to_write, sheet_name='sheet')
        df = remove_stopword(df, 'bad_function_seg')
        writeToExcelFile(df, to_write, sheet_name='sheet')
        df = CountWords(df, 'bad_function_seg_remove')
        writeToExcelFile(df, to_write, sheet_name='sheet')
        final_df = getsynonyms(df)
        writeToExcelFile(final_df, to_write, sheet_name='sheet')
