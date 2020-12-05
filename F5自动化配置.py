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
    #业务名称简写
    Business = alldata[0]
    #VS地址和端口
    vs_ipport = alldata[1]
    #SNAT地址
    snat_ip = alldata[2]
    #保持类型
    session = alldata[3]
    #保持时间
    session_time = alldata[4]
    #活检类型
    moitor = alldata[5]
    #活检动作
    moitor_action = alldata[6]
    #活检目录
    moitor_test = alldata[7]
    #http版本
    http = alldata[8]
    #返回值
    return_value = alldata[9]
    #服务器地址和端口
    server_ip = alldata[10]
    #提取端口
    server_port = server_ip.split(":")[-1]

    #检查对象
    # print(Business)
    # print(vs_ipport)
    # print(snat_ip)
    # print(session)
    # print(session_time)
    # print(moitor)
    # print(moitor_action)
    # print(moitor_test)
    # print(http)
    # print(return_value)
    # print(server_ip)
    # print(server_port)

    #配置SNAT命令
    configuration_commands.append("create ltm snatpool SNAT_" + str(Business) +  "_" + str(server_port) + " members add {" + str(snat_ip) + "}""\n")

    #配置会话保持命令
    if session:
      if session=="source-addr":
        configuration_commands[-1] += "create ltm persistence source-addr Source_addr_" + str(Business) + "_" + str(session_time) + "s match-across-virtuals enable timeout " + str(session_time) + "\n"
      if session == "cookie":
        configuration_commands[-1] += "create ltm persistence cookie-name Cookie_" + str(Business) + "_" + str(session_time) + "s match-across-virtuals enable timeout " + str(session_time) + "\n"

    #配置http活检命令
    if moitor == "http":
      moitor_test = moitor_test.replace("?", "\\?")
      if " " in return_value:
        return_value = "\"" + return_value + "\""
      if moitor_action == "GET":
        if str(http) == "1.0":
          configuration_commands[-1] += "create ltm monitor http Moitor_" + str(Business) + str(server_port) + " interval 5 timeout 15 send \"GET " + str(moitor_test) +" HTTP/1.0\\r\\nConnection: Close\\r\\n recv " + str(return_value) + "\n"
        if str(http) == "1.1":
          configuration_commands[-1] += "create ltm monitor http Moitor_" + str(Business) + str(server_port) + " interval 5 timeout 15 send \"GET " + str(moitor_test) + " HTTP/1.1\\r\\nConnection: Close\\r\\nHost:host.domain.com \\r\\n\\r\\n recv " + str(return_value) + "\n"

        # 配置pool命令
        configuration_commands[-1] += "create ltm pool Pool_" + str(Business) + "_" + str(server_port) + " load-balancing-mode least-connections-member monitor Monitor_" + str(Business) + "_" + str(server_port) + " members add {" +str(server_ip) + "}" + "\n"

    # 配置tcp活检命令
    if moitor == "tcp":

    # 配置pool命令
      configuration_commands[-1] += "create ltm pool Pool_" + str(Business) + "_" + str(server_port) + " load-balancing-mode least-connections-member monitor monitor tcp members add {" +str(server_ip) + "}" + "\n"

    #配置VS命令
    if session:
      if session == "source-addr":
        #配置VS命令
        configuration_commands[-1] += "create ltm virtual VS_" + str(Business) + "_" + str(server_port) + "ip-protocol tcp destination " + str(vs_ipport) \
                                    + " pool Pool_" + str(Business) + "_" + str(server_port) + " source-address-translation {type snatpool SNAT_" + str(Business) + "_" + str(server_port) + "}" + " persist replace-all-with {Source_addr_" + str(Business) + "_" + str(session_time) + "}"
      elif session == "cookie":
        configuration_commands[-1] += "create ltm virtual VS_" + str(Business) + "_" + str(
          server_port) + "ip-protocol tcp destination " + str(vs_ipport) \
                                      + " pool Pool_" + str(Business) + "_" + str(
          server_port) + " source-address-translation {type snatpool SNAT_" + str(Business) + "_" + str(
          server_port) + "}" + " persist replace-all-with {Cookie_" + str(Business) + "_" + str(session_time) + "}"
    else:
      #配置VS命令
      configuration_commands[-1] += "create ltm virtual VS_" + str(Business) + "_" + str(server_port) + " ip-protocol tcp destination " + str(vs_ipport) + " pool Pool_" + str(Business) + "_" + str(server_port) + " source-address-translation {type snatpool SNAT_" + str(Business) + "_" + str(server_port) + "}"

    configuration_commands[-1] += "\n\n\n###########################################################################################################################################################################################"
  for aa in configuration_commands:
    print(aa)
extract(inpath)

