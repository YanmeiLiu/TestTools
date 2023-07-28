import unittest
from case01 import ApiTest01
from case02 import ApiTest02
from BeautifulReport import BeautifulReport

suit01 = unittest.TestSuite()
suit01.addTest(ApiTest01('test_a'))
suit01.addTest(ApiTest01('test_01'))
br = BeautifulReport(suit01)
br.report(filename='test_report.html', description='测试报告', report_dir='report/')
# runner = unittest.TextTestRunner()
# runner.run(suit01)
