import threading

from TestTools.config.setconfig import get_dir
from TestTools.tools.cutword.cut_word import use_jiaba, remove_stopword, CountWords, use_pkuseg, use_doubleMax, getsynonyms

from TestTools.tools.opt_file.optFiles import writeToExcelFile, ReadFileAsDF


def run_cut_word(from_read, to_write, sheet_name):
    userdict_file = get_dir('config', 'userdict.txt')  # 自定义的词典
    stopword_file = get_dir('config', 'stopwords.txt')  # 停用词文件
    sy_file = get_dir('config', 'synonymWords.txt')  # 自定义同义词库

    df = ReadFileAsDF(from_read, sheet_name)
    # jieba 分词
    # df = use_jiaba(df, 'good_function', 'cut_for_search', userdict_file)
    # pkuesg 分词 model_name 网络分词
    df = use_pkuseg(df, 'good_function', 'web', userdict_file, True)

    # 双向分词
    # df = use_doubleMax(df, 'good_function', userdict_file)
    writeToExcelFile(df, to_write, sheet_name='after_cut')
    # 去掉不需要的词
    df = remove_stopword(df, 'good_function_seg', stopword_file, True)
    writeToExcelFile(df, to_write, sheet_name='remove_stopwords')
    df = CountWords(df, 'good_function_seg_remove')
    writeToExcelFile(df, to_write, sheet_name='count_terms')
    # 归纳同义词
    # final_df = getsynonyms(df, sy_file)
    # writeToExcelFile(final_df, to_write, sheet_name='final')


def many_thread():
    from_read = get_dir('data_files/user_event', '点评1.xlsx')
    # kind_list = ['社交客户管理（SCRM）', '项目协作', '客户关系管理（CRM）', '商业智能（BI）', '协作文档', '企业直播',
    #              '在线作图', '人事管理（eHR）', '研发项目管理']
    kind_list = ['人事管理（eHR）']

    threads = []
    for _ in range(len(kind_list)):  # 创建9个线程
        print('创建线程{}，运行{}'.format(_, kind_list[_]))
        to_write = get_dir('data_files/user_event/pkuseg', kind_list[_] + '_good.xlsx')
        t = threading.Thread(target=run_cut_word,
                             kwargs={"from_read": from_read, "to_write": to_write, "sheet_name": kind_list[_]})
        threads.append(t)
    for t in threads:  # 启动9个线程
        t.start()


if __name__ == '__main__':
    many_thread()
