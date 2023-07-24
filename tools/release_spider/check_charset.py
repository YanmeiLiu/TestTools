# 用于windows解决编码问题
import chardet


def check_charset(file_path):
    with open(file_path, 'rb') as f:
        data = f.read(4)
        charset = chardet.detect(data)['encoding']
        return charset
