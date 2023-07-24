#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 该模块的功能是 比较列表中的元素是否一致

# 列表中的元素相同
def equalLists(list1, list2):
    both_exist = [x for x in list1 if x in list2]
    # 两个列表中的不同元素
    either_exist = [y for y in (list1 + list2) if y not in both_exist]
    if len(both_exist) == len(list1) == len(list2):
        return True
    else:
        return False


# 列表1的元素是列表2的部分元素
def ltLists(list1, list2):
    if not isinstance(list1, list):  # 判断两个都是list类型，如果不是则转为list
        list1 = list1.split(',')
    if not isinstance(list2, list):
        list1 = list1.split(',')
    # 两个列表表都存在
    both_exist = [x for x in list1 if x in list2]
    # 两个列表中的不同元素
    neither_exist = [y for y in (list1 + list2) if y not in both_exist]
    if len(list2) >= len(both_exist) >= len(list1):
        return True
    else:
        return False


if __name__ == '__main__':
    # bb = ltLists([2, 3], [2, 3, 4, 6, 5])
    bb = equalLists([2, 3], [2, 3, 4, 6, 5])

    print(bb)
