# 进度条
import sys


def progress_bar(current_loc, all_len):
    print("\r", end="")
    print("处理进度: {:.2f}%: ".format( (current_loc + 1) / all_len * 100),
          "▋" * (int((current_loc + 1) / all_len * 100) // 2),
          end="")
    sys.stdout.flush()


if __name__ == '__main__':
    nun = 100
    for i in range(1, nun):
        progress_bar(i, nun)
