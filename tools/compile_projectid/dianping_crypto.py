#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 加密和解密产品id

from typing import List


def decode_id(num: int, l: int = 10) -> int:
    if num == 0:
        return 0

    if l > 10:
        return -1

    num_str = str(num)

    if len(num_str) > l:
        return num

    result: List[str] = []
    for i, v in enumerate(num_str):

        if i == 0:
            continue

        index = int(num_str[0:1])

        if i > int(index):
            break

        n = int(num_str[i: i + 1])
        result.append(str(9 - n))

    return int("".join(result))


def encode_id(num: int, l: int = 10) -> int:
    if num == 0:
        return 0

    if l > 10:
        return -1

    num_str = str(num)

    if len(num_str) >= l:
        return num

    result: List[str] = []

    result.append(str(len(num_str)))

    for i, __ in enumerate(num_str):
        n = int(num_str[i:i + 1])
        result.append(str(9 - n))

    # for i = 0; i < 9 - len(num_str); i++ :

    for i in range(0, 9 - len(num_str)):
        result.append(str(num % (i + 1)))

    return int("".join(result))


if __name__ == '__main__':
    encode = encode_id(2925)
    print(encode)

    decode = decode_id(5869630010)
    print(decode)
