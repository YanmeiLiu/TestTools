# Python---正向、逆向和双向最大匹配算法
# 正向最大匹配

class leftMax(object):
    def __init__(self, dict_path):
        self.dictionary = set()  # 定义字典
        self.maximum = 0  # 初始最大匹配长度
        # 获取自定义词典
        with open(dict_path, 'r', encoding="utf-8") as lines:
            for line in lines:
                line = line.strip()
                # print(line.split('\t')[0])
                if not line:
                    continue
                self.dictionary.add(line.split('\t')[0])
                if len(line) > self.maximum:
                    self.maximum = len(line)

    def cut(self, text):
        result = []
        length = len(text)
        index = 0
        while length > 0:
            word = None
            for size in range(self.maximum, 0, -1):
                if length - size < 0:
                    continue
                piece = text[index:index + size]
                if piece in self.dictionary:
                    word = piece
                    result.append(word)
                    length -= size
                    index += size
                    break
            if word is None:
                length -= 1
                result.append(text[index])
                index += 1
        return result


# 逆向最大匹配
class rightMax(object):
    def __init__(self, dict_path):
        self.dictionary = set()  # 定义字典
        self.maximum = 0  # 最大匹配长度

        with open(dict_path, 'r', encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.dictionary.add(line.split('\t')[0])
                if len(line) > self.maximum:
                    self.maximum = len(line)

    def cut(self, text):
        result = []
        index = len(text)
        while index > 0:
            word = None
            for size in range(self.maximum, 0, -1):
                if index - size < 0:
                    continue
                piece = text[(index - size):index]
                if piece in self.dictionary:
                    word = piece
                    result.append(word)
                    index -= size
                    break
            if word is None:
                index -= 1
                result.append(text[(index - 1):index])
        return result[::-1]  # 由于append为添加至末尾，故需反向打印


def doubleMax(text, path):
    left = leftMax(path)
    right = rightMax(path)

    leftMatch = left.cut(text)
    rightMatch = right.cut(text)

    # 返回分词数较少者
    if (len(leftMatch) != len(rightMatch)):
        if (len(leftMatch) < len(rightMatch)):
            return leftMatch
        else:
            return rightMatch
    else:  # 若分词数量相同，进一步判断
        leftsingle = 0
        rightsingle = 0
        isEqual = True  # 用以标志结果是否相同
        for i in range(len(leftMatch)):
            if (leftMatch[i] != rightMatch[i]):
                isEqual = False
            # 统计单字数
            if (len(leftMatch[i]) == 1):
                leftsingle += 1
            if (len(rightMatch[i]) == 1):
                rightsingle += 1
        if (isEqual):
            return leftMatch
        if (leftsingle < rightsingle):
            return leftMatch
        else:
            return rightMatch


# def main():
#     text = "北京大学生前来应聘算法工程师岗位"
#     userdict_file = get_dir('data_files', '30wdict_utf8.txt')  # 自定义的不拆分词典
#     print(doubleMax(text, userdict_file))
#

# if __name__ == '__main__':
#     main()
