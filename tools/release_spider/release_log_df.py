from TestTools.config.setconfig import get_dir
from TestTools.tools.opt_file.optFiles import writeToExcelFile
from TestTools.tools.release_spider.check_charset import check_charset
import pandas as pd

# df = pd.DataFrame(columns=("remote_addr", "time_local",
#                                "body_bytes_sent", "request_time",
#                                "upstream_response_time", "upstream_addr",
#                                "host", "request_method", "request_uri",
#                                "request_method_0", "request_uri_0", "http_x_forwarded_for",
#                                "http_referer", "http_user_agent",
#                                "status", "request_body", "__topic__", "__source__",
#                                "__tag__:__hostname__", "__tag__:__path__",
#                                "__tag__:__pack_id__", "__tag__:__receive_time__", "__time__"))
from TestTools.tools.release_spider.logAnalysis import log_process, make_spider, count_and_save

file_path = get_dir('data_files/user_events', 'downloaded_data.txt')
all, allcsv, allfile = make_spider("")

with open(file_path, 'r', encoding=check_charset(file_path)) as logfile:
    print("开始")
    for line in logfile:
        print(line)
        log_process(line, all)

    print('end')
    count_and_save(all, allcsv)
    allfile.close()
