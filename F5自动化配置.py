import sys
import os
import time
import xlrd

#设置时间对象
now = time.localtime()
nowt = time.strftime("%Y%m%d%H%M%S",now)  #这一步就是对时间进行格式化
#输出文本文件
class Logger(object):
  def __init__(self,filename="Default.log"):
    self.terminal = sys.stdout
    self.log = open(filename,"a")
  def write(self,message):
    self.terminal.write(message)
    self.log.write(message)
  def flush(self):
    pass
path = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
sys.stdout = Logger(str(nowt)+'中关村银行网络配置方案.txt')

inpath = '负载均衡申请表.xlsx'
def extract(inpath):
  data = xlrd.open_workbook(inpath,encoding_override='utf-8')
  table = data.sheets()[0]  # 选定表
  nrows = table.nrows  # 获取行号
  ncols = table.ncols  # 获取列号
  configuration_commands = []

  for xle in range(1,nrows):  # 第0行为表头
    alldata = table.row_values(xle)  # 循环输出excel表中每一行，即所有数据
    Business = alldata[0]
    vs_ipport = alldata[1]
    snat_ip = alldata[2]
    session = alldata[3]
    session_time = alldata[4]
    moitor = alldata[5]
    moitor_test = alldata[6]
    http = alldata[7]
    return_value = alldata[8]
    server_ip = alldata[9]
    configuration_commands[xle] += "create ltm snatpool SNAT_"+str(Business)+" members add {" + str(snat_ip) + "}""\n"
    print(configuration_commands)
    if moitor=="http":
      if http == "1.0":
      configuration_commands[xle] += "create ltm monitor http Moitor_" + str(Business) + " interval 5 timeout 15 send \"GET "+str(moitor_test) +"HTTP/1.0\\r\\nConnection: Close\\r\\n recv " + str(return_value) + "\n"
      elif http == "1.1":
      configuration_commands[xle] += "create ltm monitor http Moitor_" + str(Business) + " interval 5 timeout 15 send \"GET " + str(moitor_test) + "HTTP/1.1\\r\\nConnection: Close\\r\\nHost:host.domain.com \\r\\n\\r\\n recv " + str(return_value) + "\n"
      print(configuration_commands)





extract(inpath)
