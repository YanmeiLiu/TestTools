import difflib


def comStr(str1, str2):
    matcher = difflib.SequenceMatcher(None, str1, str2)

    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'insert':
            print("Insert:", str2[j1:j2])
        elif op == 'delete':
            print("Delete:", str1[i1:i2])
        elif op == 'replace':
            print("Replace:", str1[i1:i2], "with", str2[j1:j2])
        elif op == 'equal':
            print("Equal:", str1[i1:i2])


if __name__ == '__main__':
    str1 = "sdskdsdh" \
           "dshdkjasdhsadkh"
    str2 = "hell0 we\"" \
           "dsdksdsdksd "
    comStr(str1, str2)
