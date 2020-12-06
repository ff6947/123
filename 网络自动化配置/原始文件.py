#安装相关插件
import sys
import os
import time
import xlrd

#判断区域并赋值1或者0或者-1
def as0_1(as_ip,src,drc):
  global as_x
  as_x = 0
  for a in as_ip:
    if a in src:
      as_x = as_x+1
    if a in drc:
      as_x = as_x-1
  return as_x

#华三交换机acl in方向源地址配置策略
def h3c_acl_in_src(src,drc,dxy,dport):
  h3c_acl_in_src_x = 'rule ' + '***' + ' permit ' + str(dxy) + ' source ' + str(drc) + ' 0 destination ' + str(
    src) + ' 0 source-port eq ' + str(dport)
  return h3c_acl_in_src_x

#华三交换机acl in方向目的地址配置策略
def h3c_acl_in_drc(src,drc,dxy,dport):
  h3c_acl_in_drc_x = 'rule ' + '***' + ' permit ' + str(dxy) + ' source ' + str(drc) + ' 0 destination ' + str(
    src) + ' 0 destination-port eq ' + str(dport)
  return h3c_acl_in_drc_x

#华三交换机acl out方向源地址配置策略
def h3c_acl_out_src(src,drc,dxy,dport):
  h3c_acl_out_src_x = 'rule ' + '***' + ' permit ' + str(dxy) + ' source ' + str(drc) + ' 0 destination ' + str(
    src) + ' 0 destination-port eq ' + str(dport)
  return h3c_acl_out_src_x

#华三交换机acl out方向目的地址配置策略
def h3c_acl_out_drc(src,drc,dxy,dport):
  h3c_acl_out_drc_x = 'rule ' + '***' + ' permit ' + str(dxy) + ' source ' + str(drc) + ' 0 destination ' + str(
    src) + ' 0 source-port eq ' + str(dport)
  return h3c_acl_out_drc_x

#思科asa防火墙源地址区域为inside配置策略
def cisco_asa_inside_src(src,drc,dxy,dport):
  cisco_asa_inside_src_x = 'access-list acl-inside extended permit ' + str(dxy) + ' host ' + str(src) + ' host ' + str(drc) + ' eq ' + str(dport)
  return cisco_asa_inside_src_x

#思科asa防火墙源地址区域为outside配置策略
def cisco_asa_outside_src(src,drc,dxy,dport):
  cisco_asa_inside_src_x = 'access-list acl-outside extended permit ' + str(dxy) + ' host ' + str(src) + ' host ' + str(drc) + ' eq ' + str(dport)
  return cisco_asa_inside_src_x

#迈普交换机acl in方向源地址配置策略
def maipu_acl_in_src(src,drc,dxy,dport):
  maipu_acl_in_src ='*** permit '+str(dxy)+' host '+str(src)+' host '+str(drc)+' eq '+str(dport)
  return maipu_acl_in_src

#迈普交换机acl in方向目的地址配置策略
def maipu_acl_in_drc(src,drc,dxy,dport):
  maipu_acl_in_drc ='*** permit '+str(dxy)+' host '+str(src)+' eq '+str(dport)+' host '+str(drc)
  return maipu_acl_in_drc

#迈普交换机acl out方向目的地址配置策略
def maipu_acl_out_src(src,drc,dxy,dport):
  maipu_acl_out_src = '*** permit '+str(dxy)+' host '+str(src)+' eq '+str(dport)+' host '+str(drc)
  return maipu_acl_out_src

#迈普交换机acl in方向源地址配置策略
def maipu_acl_out_drc(src,drc,dxy,dport):
  maipu_acl_out_drc ='*** permit '+str(dxy)+' host '+str(src)+' host '+str(drc)+' eq '+str(dport)
  return maipu_acl_out_drc

#山石网科防火墙配置策略
def hillstone_fw_src(a,src,drc,dxy,dport):
  dxy_dport = str(dxy.upper()) + '-' + str(dport)
  for b in range(len(a)):
    if src in a[b]["src: "]:
      if dxy_dport in a[b]["dport: "]:
        a[b]["src: "].append(src)
        a[b]["drc: "].append(drc)
        a[b]["dport: "].append(dxy_dport)
        a[b]["area: "].append("s")
        break
      if drc in a[b]["drc: "]:
        a[b]["src: "].append(src)
        a[b]["drc: "].append(drc)
        a[b]["dport: "].append(dxy_dport)
        a[b]["area: "].append("s")
        break
    if drc in a[b]["drc: "]:
      if dxy in a[b]["dxy: "]:
        if dport in a[b]["dport: "]:
          a[b]["src: "].append(src)
          a[b]["drc: "].append(drc)
          a[b]["dport: "].append(dxy_dport)
          a[b]["area: "].append("s")
          break
  else:
    a.append({
      "src: ": [src],
      "drc: ": [drc],
      "dport: ": [dxy_dport],
      "area: ": ["s"]})

  for b in range(len(a)):
    for c in a[b]:
      a[b][c] = set(a[b][c])
      a[b][c] = list(a[b][c])
  return a

#山石网科防火墙配置策略
def hillstone_fw_drc(a,src,drc,dxy,dport):
  dxy_dport = str(dxy.upper()) + '-' + str(dport)
  for b in range(len(a)):
    if src in a[b]["src: "]:
      if dxy_dport in a[b]["dport: "]:
        a[b]["src: "].append(src)
        a[b]["drc: "].append(drc)
        a[b]["dport: "].append(dxy_dport)
        a[b]["area: "].append("d")
        break
      if drc in a[b]["drc: "]:
        a[b]["src: "].append(src)
        a[b]["drc: "].append(drc)
        a[b]["dport: "].append(dxy_dport)
        a[b]["area: "].append("d")
        break
    if drc in a[b]["drc: "]:
      if dxy in a[b]["dxy: "]:
        if dport in a[b]["dport: "]:
          a[b]["src: "].append(src)
          a[b]["drc: "].append(drc)
          a[b]["dport: "].append(dxy_dport)
          a[b]["area: "].append("d")
          break
  else:
    a.append({
      "src: ": [src],
      "drc: ": [drc],
      "dport: ": [dxy_dport],
      "area: ": ["d"]})

  for b in range(len(a)):
    for c in a[b]:
      a[b][c] = set(a[b][c])
      a[b][c] = list(a[b][c])
  return a

#深信服防火墙原地址策略配置
def songfor_fw_src(a,src,drc,dxy,dport):
  dxy_dport = str(dxy.upper()) + '-' + str(dport)
  for b in range(len(a)):
    if src in a[b]["src: "]:
      if dxy_dport in a[b]["dport: "]:
        a[b]["src: "].append(src)
        a[b]["drc: "].append(drc)
        a[b]["dport: "].append(dxy_dport)
        a[b]["area: "].append("s")
        break
      if drc in a[b]["drc: "]:
        a[b]["src: "].append(src)
        a[b]["drc: "].append(drc)
        a[b]["dport: "].append(dxy_dport)
        a[b]["area: "].append("s")
        break
    if drc in a[b]["drc: "]:
      if dxy in a[b]["dxy: "]:
        if dport in a[b]["dport: "]:
          a[b]["src: "].append(src)
          a[b]["drc: "].append(drc)
          a[b]["dport: "].append(dxy_dport)
          a[b]["area: "].append("s")
          break
  else:
    a.append({
      "src: ": [src],
      "drc: ": [drc],
      "dport: ": [dxy_dport],
      "area: ":["s"]})

  for b in range(len(a)):
    for c in a[b]:
      a[b][c] = set(a[b][c])
      a[b][c] = list(a[b][c])
  return a

#深信服防火墙原地址策略配置
def songfor_fw_drc(a,src,drc,dxy,dport):
  dxy_dport = str(dxy.upper()) + '-' + str(dport)
  for b in range(len(a)):
    if src in a[b]["src: "]:
      if dxy_dport in a[b]["dport: "]:
        a[b]["src: "].append(src)
        a[b]["drc: "].append(drc)
        a[b]["dport: "].append(dxy_dport)
        a[b]["area: "].append("d")
        break
      if drc in a[b]["drc: "]:
        a[b]["src: "].append(src)
        a[b]["drc: "].append(drc)
        a[b]["dport: "].append(dxy_dport)
        a[b]["area: "].append("d")
        break
    if drc in a[b]["drc: "]:
      if dxy in a[b]["dxy: "]:
        if dport in a[b]["dport: "]:
          a[b]["src: "].append(src)
          a[b]["drc: "].append(drc)
          a[b]["dport: "].append(dxy_dport)
          a[b]["area: "].append("d")
          break
  else:
    a.append({
      "src: ": [src],
      "drc: ": [drc],
      "dport: ": [dxy_dport],
      "area: ":["d"]})

  for b in range(len(a)):
    for c in a[b]:
      a[b][c] = set(a[b][c])
      a[b][c] = list(a[b][c])
  return a

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

##########以下为中金网段
#匹配核心业务区 1
zj_hx_ip=["10.0.0.","10.0.1.","10.0.2.","10.0.3.","10.0.24.""10.0.100."]
zj_hx_3000ip=["10.0.1."]         ##有acl 3000  out
zj_hx_3124ip=["10.0.24."]       ##有acl 3124  out

#匹配互金业务区 2
zj_hj_ip= ["10.0.4.","10.0.5.","10.0.6.","10.0.7.","10.0.102."]
zj_hj_3000ip= ["10.0.5."]         ##有acl 3000  out

#匹配管理业务区 3
zj_gl_ip= ["10.0.128.","10.0.129.","10.0.130.","10.0.131.","10.0.200."]
zj_gl_3000ip= ["10.0.129."]         ##有acl 3000  out
zj_gl_3230ip= ["10.0.130."]         ##有acl 3230  in

#匹配互联网接入区 4
zj_hl_ip= ["10.0.12.","10.0.13.","10.0.14.","10.0.16.","10.0.17.","10.0.106."]
zj_hl_3114ip= ["10.0.14."]           ##有acl 3114  out
zj_hl_3115ip= ["10.0.15."]           ##有acl 3115  out

#匹配办公业务区 5
zj_bg_ip=["10.0.132.","10.0.133.","10.0.134.","10.0.135.","10.0.202."]
zj_bg_3234ip = ["10.0.134."]           ##有acl 3234    out

#匹配运维管理区 6
zj_yg_ip=["10.0.144.","10.0.145.","10.0.146.","10.0.147.","10.0.72.","10.0.148."]
zj_yg_3172ip=["10.0.72."]           ##有acl 3172  out
zj_yg_3000ip=["10.0.148."]             ##有acl 3000   out

#配置外联区 7
zj_wl_ip=["10.0.8.","10.0.9.","10.0.56.","10.0.10.","10.0.11","10.0.104."]
zj_wl_3156ip=["10.0.56."]           ##有acl 3156   out

#测试区
sjhl_cs_ip = ["10.0.16.","10.0.247.","10.0.248.","10.0.249.","10.0.250.","10.4."]
sjhl_cs_uattosit1_ip = ["10.4.8.","10.4.9.","10.4.10.","10.4.11."]
sjhl_cs_uattosit2_ip = ["10.4.12.","10.4.13.","10.4.14."]
sjhl_cs_dashuju_ip = ["10.4.15."]

#卫通办公区
wt_oa_acl3250_ip = ["10.2.150."]
wt_oa_acl3251_ip = ["10.2.151."]
wt_oa_acl3253_ip = ["10.2.153."]
wt_oa_acl3157_ip = ["10.2.157."]
wt_oa_acl3258_ip = ["10.2.158."]
wt_oa_acl3259_ip = ["10.2.159."]
wt_oa_acl3260_ip = ["10.2.160."]
wt_oa_acl3261_ip = ["10.2.161."]
wt_oa_acl3262_ip = ["10.2.162."]
wt_oa_acl3263_ip = ["10.2.163."]
wt_oa_acl3307_ip = ["10.2.207."]
wt_oa_acl3308_ip = ["10.2.208."]
wt_oa_acl3335_ip = ["10.2.235."]
wt_oa_acl3344_ip = ["10.2.244."]
wt_oa_acl3345_ip = ["10.2.245."]
wt_oa_acl3347_ip = ["10.2.247."]

#裕惠办公区
yh_oa_ip = ["10.2.152.","10.2.155.","10.2.156.","10.2.228.","10.2.232.","10.2.236.","10.2.165.","10.2.164."]
yh_oa_aclceshi152_ip = ["10.2.152."]
yh_oa_aclwaixie_ip = ["10.2.165."]
yh_oa_aclshipinhuiyi_ip = ["10.2.152."]

##########以下为同城网段
##核心业务区
sjhl_hx_ip = ["10.10.9.","10.10.10.","10.10.13.","10.10.14.","10.10.15.","10.10.16.","10.10.17.","10.10.62."]
sjhl_hx_3000ip = ["10.10.9."]

#互金业务区
sjhl_hj_ip = ["10.10.73.","10.10.74.","10.10.77.","10.10.78."]
sjhl_hj_3000ip = ["10.10.73."]

#管理业务区
sjhl_gl_ip = ["10.10.137.","10.10.138.","10.10.141.","10.10.142."]
sjhl_gl_3000ip = ["10.10.137."]
sjhl_gl_3001ip = ["10.10.138."]

#办公业务区
sjhl_bg_ip = ["10.15.9.","10.15.10.","10.15.13.","10.15.14."]
sjhl_bg_3000ip = ["10.15.9."]

#运维管理区
sjhl_yg_ip = ["10.10.193.","10.10.194.","10.10.195.","10.10.196.","10.10.197.","10.10.198.","10.10.199.","10.10.224.","10.10.223."]
sjhl_yg_3697ip = ["10.10.224."]

#外联区
sjhl_wl_ip = ["10.11.17.","10.11.18.","10.11.19.","10.11.62."]

#互联网接入区
sjhl_hl_ip = ["10.11.73.","10.11.74.","10.11.75.","10.11.102.","10.11.127."]

#给对应设备赋值
ZJHX3000a=[]
ZJHX3124a=[]
ZJHJ3000a=[]
ZJGL3000a=[]
ZJGL3230a=[]
ZJBG3234a=[]
ZJYW3172a=[]
ZJYW3000a=[]
ZJHL3114a=[]
ZJHL3115a=[]
ZHWL3156a=[]
ZJHXASAa=[]
ZJHJASAa=[]
ZJGLASAa=[]
ZJBGASAa=[]
ZJYWASAa=[]
ZJHLASAa=[]
ZHWLASAa=[]
SJHLCSa = []
SJHLUAT1a = []
SJHLUAT2a = []
SJHLSHUJa = []
WTOA3250a = []
WTOA3251a = []
WTOA3253a = []
WTOA3157a = []
WTOA3258a = []
WTOA3259a = []
WTOA3260a = []
WTOA3261a = []
WTOA3262a = []
WTOA3263a = []
WTOA3307a = []
WTOA3308a = []
WTOA3335a = []
WTOA3344a = []
WTOA3345a = []
WTOA3347a = []
YHOAIPa = []
YHOA152a = []
YHOA165a = []
YHOASHIPINa = []
SJHLHXHILLa = []
SJHLHX3000a = []
SJHLHJHILLa = []
SJHLHJ3000a = []
SJHLGLHILLa = []
SJHLGL3000a = []
SJHLGL3001a = []
SJHLBGHILLa = []
SJHLBG3000a = []
SJHLYGHILLa = []
SJHLYG3697a = []
SJHLWLHILLa = []
SJHLHLHILLa = []

inpath = '网络策略.xlsx'
def extract(inpath):
  data = xlrd.open_workbook(inpath,encoding_override='utf-8')
  table = data.sheets()[0]  # 选定表
  nrows = table.nrows  # 获取行号
  ncols = table.ncols  # 获取列号

  for xle in range(1,nrows):  # 第0行为表头
    alldata = table.row_values(xle)  # 循环输出excel表中每一行，即所有数据
    src= alldata[0]
    drc= alldata[1]
    dxy= alldata[2]
    dport=int(alldata[3])
    # 判断区域
    # 判断通过核心业务区acl3000
    ZJHX3000 = as0_1(zj_hx_3000ip,src,drc)
    # 判断通过核心业务区acl3124
    ZJHX3124 = as0_1(zj_hx_3000ip,src,drc)
    # 判断通过互金业务区acl3000
    ZJHJ3000 = as0_1(zj_hx_3000ip,src,drc)
    # 判断通过管理业务acl3000
    ZJGL3000 = as0_1(zj_hx_3000ip,src,drc)
    # 判断通过管理业务区acl3230
    ZJGL3230 = as0_1(zj_hx_3000ip,src,drc)
    # 判断通过办公业务区acl3234
    ZJBG3234 = as0_1(zj_hx_3000ip,src,drc)
    # 判断通过运维管理区acl 3172
    ZJYW3172 = as0_1(zj_yg_3172ip,src,drc)
    # 判断通过运维管理区acl 3000
    ZJYW3000 = as0_1(zj_yg_3000ip,src,drc)
    # 判断通过互联网接入区acl3114
    ZJHL3114 = as0_1(zj_hl_3114ip,src,drc)
    # 判断通过互联网接入区acl3115
    ZJHL3115 = as0_1(zj_hl_3115ip,src,drc)
    # 判断通过外联区acl 3156
    ZHWL3156 = as0_1(zj_wl_3156ip,src,drc)
    # 判断通过测试区深信服
    ZJCSSXF = "@"
    # 判断通过核心业务区思科
    ZJHXASA = as0_1(zj_hx_ip,src,drc)
    # 判断通过互金业务区思科
    ZJHJASA = as0_1(zj_hj_ip,src,drc)
    # 判断通过管理业务区思科
    ZJGLASA = as0_1(zj_gl_ip,src,drc)
    # 判断通过办公业务区思科
    ZJBGASA = as0_1(zj_bg_ip,src,drc)
    # 判断通过运维管理区思科
    ZJYWASA = as0_1(zj_yg_ip,src,drc)
    # 判断通过互联网接入区思科
    ZJHLASA = as0_1(zj_hl_ip,src,drc)
    # 判断通过外联区思科
    ZHWLASA = as0_1(zj_wl_ip,src,drc)

    SJHLCS = as0_1(sjhl_cs_ip,src,drc)
    SJHLUAT1 = as0_1(sjhl_cs_uattosit1_ip,src,drc)
    SJHLUAT2 = as0_1(sjhl_cs_uattosit2_ip,src,drc)
    SJHLSHUJ = as0_1(sjhl_cs_dashuju_ip,src,drc)
    WTOA3250 = as0_1(wt_oa_acl3250_ip,src,drc)
    WTOA3251 = as0_1(wt_oa_acl3251_ip,src,drc)
    WTOA3253 = as0_1(wt_oa_acl3253_ip,src,drc)
    WTOA3157 = as0_1(wt_oa_acl3157_ip,src,drc)
    WTOA3258 = as0_1(wt_oa_acl3258_ip,src,drc)
    WTOA3259 = as0_1(wt_oa_acl3259_ip,src,drc)
    WTOA3260 = as0_1(wt_oa_acl3260_ip,src,drc)
    WTOA3261 = as0_1(wt_oa_acl3261_ip,src,drc)
    WTOA3262 = as0_1(wt_oa_acl3262_ip,src,drc)
    WTOA3263 = as0_1(wt_oa_acl3263_ip,src,drc)
    WTOA3307 = as0_1(wt_oa_acl3307_ip,src,drc)
    WTOA3308 = as0_1(wt_oa_acl3308_ip,src,drc)
    WTOA3335 = as0_1(wt_oa_acl3335_ip,src,drc)
    WTOA3344 = as0_1(wt_oa_acl3344_ip,src,drc)
    WTOA3345 = as0_1(wt_oa_acl3345_ip,src,drc)
    WTOA3347 = as0_1(wt_oa_acl3347_ip,src,drc)
    YHOAIP = as0_1(yh_oa_ip,src,drc)
    YHOA152 = as0_1(yh_oa_aclceshi152_ip,src,drc)
    YHOA165 = as0_1(yh_oa_aclwaixie_ip,src,drc)
    YHOASHIPIN = as0_1(yh_oa_aclshipinhuiyi_ip,src,drc)
    SJHLHXHILL = as0_1(sjhl_hx_ip,src,drc)
    SJHLHX3000 = as0_1(sjhl_hx_3000ip,src,drc)
    SJHLHJHILL = as0_1(sjhl_hj_ip,src,drc)
    SJHLHJ3000 = as0_1(sjhl_hj_3000ip,src,drc)
    SJHLGLHILL = as0_1(sjhl_gl_ip,src,drc)
    SJHLGL3000 = as0_1(sjhl_gl_3000ip,src,drc)
    SJHLGL3001 = as0_1(sjhl_gl_3001ip,src,drc)
    SJHLBGHILL = as0_1(sjhl_bg_ip,src,drc)
    SJHLBG3000 = as0_1(sjhl_bg_3000ip,src,drc)
    SJHLYGHILL = as0_1(sjhl_yg_ip,src,drc)
    SJHLYG3697 = as0_1(sjhl_yg_3697ip,src,drc)
    SJHLWLHILL = as0_1(sjhl_wl_ip,src,drc)
    SJHLHLHILL = as0_1(sjhl_hl_ip,src,drc)

    # 根据源地址编写方案
    if ZJHX3000 == 1:
      ZJHX3000a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if ZJHX3124 == 1:
      ZJHX3124a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if ZJHJ3000 == 1:
      ZJHJ3000a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if ZJGL3000 == 1:
      ZJGL3000a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if ZJGL3230 == 1:
      ZJGL3230a.append(h3c_acl_out_src(src,drc,dxy,dport))
    if ZJBG3234 == 1:
      ZJBG3234a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if ZJYW3172 == 1:
      ZJYW3172a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if ZJYW3000 == 1:
      ZJYW3000a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if ZJHL3114 == 1:
      ZJHL3114a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if ZJHL3115 == 1:
      ZJHL3115a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if ZHWL3156 == 1:
      ZHWL3156a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if SJHLUAT1 == 1:
      SJHLUAT1a.append(maipu_acl_in_src(src,drc,dxy,dport))
    if SJHLUAT2 == 1:
      SJHLUAT2a.append(maipu_acl_in_src(src,drc,dxy,dport))
    if SJHLSHUJ == 1:
      SJHLSHUJa.append(maipu_acl_in_src(src,drc,dxy,dport))
    if WTOA3250 == 1:
      WTOA3250a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if WTOA3251 == 1:
      WTOA3251a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if WTOA3253 == 1:
      WTOA3253a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if WTOA3157 == 1:
      WTOA3157a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if WTOA3258 == 1:
      WTOA3258a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if WTOA3259 == 1:
      WTOA3259a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if WTOA3260 == 1:
      WTOA3260a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if WTOA3261 == 1:
      WTOA3261a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if WTOA3262 == 1:
      WTOA3262a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if WTOA3263 == 1:
      WTOA3263a.append(h3c_acl_out_drc(src,drc,dxy,dport))
    if WTOA3307 == 1:
      WTOA3307a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if WTOA3308 == 1:
      WTOA3308a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if WTOA3335 == 1:
      WTOA3335a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if WTOA3344 == 1:
      WTOA3344a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if WTOA3345 == 1:
      WTOA3345a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if WTOA3347 == 1:
      WTOA3347a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if YHOA152 == 1:
      YHOA152a.append(maipu_acl_out_drc(src,drc,dxy,dport))
    if YHOA165 == 1:
      YHOA165a.append(maipu_acl_in_drc(src,drc,dxy,dport))
    if YHOASHIPIN == 1:
      YHOASHIPINa.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if SJHLHX3000 == 1:
      SJHLHX3000a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if SJHLHJ3000 == 1:
      SJHLHJ3000a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if SJHLGL3000 == 1:
      SJHLGL3000a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if SJHLGL3001 == 1:
      SJHLGL3001a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if SJHLBG3000 == 1:
      SJHLBG3000a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if SJHLYG3697 == 1:
      SJHLYG3697a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if ZJHXASA == 1:
      ZJHXASAa.append(cisco_asa_inside_src(src,drc,dxy,dport))
    if ZJHJASA == 1:
      ZJHJASAa.append(cisco_asa_inside_src(src,drc,dxy,dport))
    if ZJGLASA == 1:
      ZJGLASAa.append(cisco_asa_inside_src(src,drc,dxy,dport))
    if ZJBGASA == 1:
      ZJBGASAa.append(cisco_asa_inside_src(src,drc,dxy,dport))
    if ZJYWASA == 1:
      ZJYWASAa.append(cisco_asa_inside_src(src,drc,dxy,dport))
    if ZJHLASA == 1:
      ZJHLASAa.append(cisco_asa_outside_src(src,drc,dxy,dport))
    if ZHWLASA == 1:
      ZHWLASAa.append(cisco_asa_outside_src(src,drc,dxy,dport))
    if SJHLCS == 1:
      songfor_fw_src(SJHLCSa,src,drc,dxy,dport)
    if YHOAIP == 1:
      hillstone_fw_src(YHOAIPa,src,drc,dxy,dport)
    if SJHLHXHILL == 1:
      hillstone_fw_src(YHOAIPa,src,drc,dxy,dport)
    if SJHLHJHILL == 1:
      hillstone_fw_src(YHOAIPa,src,drc,dxy,dport)
    if SJHLGLHILL == 1:
      hillstone_fw_src(YHOAIPa,src,drc,dxy,dport)
    if SJHLBGHILL == 1:
      hillstone_fw_src(YHOAIPa,src,drc,dxy,dport)
    if SJHLYGHILL == 1:
      hillstone_fw_src(YHOAIPa,src,drc,dxy,dport)
    if SJHLWLHILL == 1:
      hillstone_fw_src(YHOAIPa,src,drc,dxy,dport)
    if SJHLHLHILL == 1:
      hillstone_fw_src(YHOAIPa,src,drc,dxy,dport)




    #根据目的地址编写方案
    if ZJHX3000 == -1:
      ZJHX3000a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if ZJHX3124 == -1:
      ZJHX3124a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if ZJHJ3000 == -1:
      ZJHJ3000a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if ZJGL3000 == -1:
      ZJGL3000a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if ZJGL3230 == -1:
      ZJGL3230a.append(h3c_acl_out_drc(src,drc,dxy,dport))
    if ZJBG3234 == -1:
      ZJBG3234a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if ZJYW3172 == -1:
      ZJYW3172a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if ZJYW3000 == -1:
      ZJYW3000a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if ZJHL3114 == -1:
      ZJHL3114a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if ZJHL3115 == -1:
      ZJHL3115a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if ZHWL3156 == -1:
      ZHWL3156a.append(h3c_acl_in_drc(src,drc,dxy,dport))
    if SJHLUAT1 == -1:
      SJHLUAT1a.append(maipu_acl_in_drc(src,drc,dxy,dport))
    if SJHLUAT2 == -1:
      SJHLUAT2a.append(maipu_acl_in_drc(src,drc,dxy,dport))
    if SJHLSHUJ == -1:
      SJHLSHUJa.append(maipu_acl_in_drc(src,drc,dxy,dport))
    if WTOA3250 == -1:
      WTOA3250a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if WTOA3251 == -1:
      WTOA3251a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if WTOA3253 == -1:
      WTOA3253a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if WTOA3157 == -1:
      WTOA3157a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if WTOA3258 == -1:
      WTOA3258a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if WTOA3259 == -1:
      WTOA3259a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if WTOA3260 == -1:
      WTOA3260a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if WTOA3261 == -1:
      WTOA3261a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if WTOA3262 == -1:
      WTOA3262a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if WTOA3263 == -1:
      WTOA3263a.append(h3c_acl_out_src(src,drc,dxy,dport))
    if WTOA3307 == -1:
      WTOA3307a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if WTOA3308 == -1:
      WTOA3308a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if WTOA3335 == -1:
      WTOA3335a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if WTOA3344 == -1:
      WTOA3344a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if WTOA3345 == -1:
      WTOA3345a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if WTOA3347 == -1:
      WTOA3347a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if YHOA152 == -1:
      YHOA152a.append(maipu_acl_out_src(src,drc,dxy,dport))
    if YHOA165 == -1:
      YHOA165a.append(maipu_acl_in_src(src,drc,dxy,dport))
    if YHOASHIPIN == -1:
      YHOASHIPINa.append(h3c_acl_in_src(src,drc,dxy,dport))
    if SJHLHX3000 == -1:
      SJHLHX3000a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if SJHLHJ3000 == -1:
      SJHLHJ3000a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if SJHLGL3000 == -1:
      SJHLGL3000a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if SJHLGL3001 == -1:
      SJHLGL3001a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if SJHLBG3000 == -1:
      SJHLBG3000a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if SJHLYG3697 == -1:
      SJHLYG3697a.append(h3c_acl_in_src(src,drc,dxy,dport))
    if ZJHXASA == -1:
      ZJHXASAa.append(cisco_asa_outside_src(src,drc,dxy,dport))
    if ZJHJASA == -1:
      ZJHJASAa.append(cisco_asa_outside_src(src,drc,dxy,dport))
    if ZJGLASA == -1:
      ZJGLASAa.append(cisco_asa_outside_src(src,drc,dxy,dport))
    if ZJBGASA == -1:
      ZJBGASAa.append(cisco_asa_outside_src(src,drc,dxy,dport))
    if ZJYWASA == -1:
      ZJYWASAa.append(cisco_asa_outside_src(src,drc,dxy,dport))
    if ZJHLASA == -1:
      ZJHLASAa.append(cisco_asa_inside_src(src,drc,dxy,dport))
    if ZHWLASA == -1:
      ZHWLASAa.append(cisco_asa_inside_src(src,drc,dxy,dport))
    if SJHLCS == -1:
      songfor_fw_drc(SJHLCSa,src,drc,dxy,dport)
    if YHOAIP == -1:
      hillstone_fw_drc(YHOAIPa,src,drc,dxy,dport)
    if SJHLHXHILL == -1:
      hillstone_fw_drc(YHOAIPa,src,drc,dxy,dport)
    if SJHLHJHILL == -1:
      hillstone_fw_drc(YHOAIPa,src,drc,dxy,dport)
    if SJHLGLHILL == -1:
      hillstone_fw_drc(YHOAIPa,src,drc,dxy,dport)
    if SJHLBGHILL == -1:
      hillstone_fw_drc(YHOAIPa,src,drc,dxy,dport)
    if SJHLYGHILL == -1:
      hillstone_fw_drc(YHOAIPa,src,drc,dxy,dport)
    if SJHLWLHILL == -1:
      hillstone_fw_drc(YHOAIPa,src,drc,dxy,dport)
    if SJHLHLHILL == -1:
      hillstone_fw_drc(YHOAIPa,src,drc,dxy,dport)
extract(inpath)

#打印方案
if ZJHX3000a != []:
  ZJHX3000a.insert(0,'配置中金核心业务区核心交换机ZGCB-ZJB02-COREYW-CS01')
  ZJHX3000a.insert(1,'acl advanced 3000')
  ZJHX3000a+=["save force"]
  for pan in range(len(ZJHX3000a)):
    print(ZJHX3000a[pan])
  print('\n')
if ZJHX3124a != []:
  ZJHX3124a.insert(0,'配置中金核心业务区核心交换机ZGCB-ZJB02-COREYW-CS01')
  ZJHX3124a.insert(1,'acl advanced 3124')
  ZJHX3124a+=['save force']
  for pan in range(len(ZJHX3124a)):
    print(ZJHX3124a[pan])
  print('\n')
if ZJHJ3000a != []:
  ZJHJ3000a.insert(0,'配置中金互金业务区核心交换机ZGCB-ZJB02-INTYW-CS01')
  ZJHJ3000a.insert(1,'acl advanced 3000')
  ZJHJ3000a+=['save force']
  for pan in range(len(ZJHJ3000a)):
    print(ZJHJ3000a[pan])
  print('\n')
if ZJGL3000a != []:
  ZJGL3000a.insert(0,'配置中金管理业务区核心交换机ZGCB-ZJB02-MGTYW-CS01')
  ZJGL3000a.insert(1,'acl advanced 3000')
  ZJGL3000a+=['save force']
  for pan in range(len(ZJGL3000a)):
    print(ZJGL3000a[pan])
  print('\n')
if ZJGL3230a != []:
  ZJGL3230a.insert(0,'配置中金管理业务区核心交换机ZGCB-ZJB02-MGTYW-CS01')
  ZJGL3230a.insert(1,'acl advanced 3230')
  ZJGL3230a+=['save force']
  for pan in range(len(ZJGL3230a)):
    print(ZJGL3230a[pan])
  print('\n')
if ZJBG3234a != []:
  ZJBG3234a.insert(0,'配置中金办公业务区核心交换机ZGCB-ZJB02-OAYW-CS01')
  ZJBG3234a.insert(1,'acl advanced 3234')
  ZJBG3234a+=['save force']
  for pan in range(len(ZJHX3124a)):
    print(ZJHX3124a[pan])
  print('\n')
if ZJYW3172a != []:
  ZJYW3172a.insert(0,'配置中金运维管理区核心交换机ZGCB-ZJB02-OPMGT-CS01')
  ZJYW3172a.insert(1,'acl advanced 3172')
  ZJYW3172a+=['save force']
  for pan in range(len(ZJYW3172a)):
    print(ZJYW3172a[pan])
  print('\n')
if ZJYW3000a != []:
  ZJYW3000a.insert(0,'配置中金运维管理区核心交换机ZGCB-ZJB02-OPMGT-CS01')
  ZJYW3000a.insert(1,'acl advanced 3000')
  ZJYW3000a+=['save force']
  for pan in range(len(ZJYW3000a)):
    print(ZJYW3000a[pan])
  print('\n')
if ZJHL3114a != []:
  ZJHL3114a.insert(0,'配置中金互联网接入区核心交换机ZGCB-ZJB04-INT-DMZDS01')
  ZJHL3114a.insert(1,'acl advanced 3114')
  ZJHL3114a+=['save force']
  for pan in range(len(ZJHL3114a)):
    print(ZJHL3114a[pan])
  print('\n')
if ZJHL3115a != []:
  ZJHL3115a.insert(0,'配置中金互联网接入区核心交换机ZGCB-ZJB04-INT-DMZDS01')
  ZJHL3115a.insert(1,'acl advanced 3115')
  ZJHL3115a+=['save force']
  for pan in range(len(ZJHL3115a)):
    print(ZJHL3115a[pan])
  print('\n')
if ZHWL3156a != []:
  ZHWL3156a.insert(0,'配置中金外联区核心交换机ZGCB-ZJB06-EXT-DMZDS01')
  ZHWL3156a.insert(1,'acl number 3156')
  ZHWL3156a+=['save force']
  for pan in range(len(ZHWL3156a)):
    print(ZHWL3156a[pan])
  print('\n')
if ZJHXASAa != []:
  ZJHXASAa.insert(0,'配置中金核心业务区思科墙ZGCB-ZJB02-COREYW-FW01')
  ZJHXASAa.insert(1,'config t')
  ZJHXASAa+=['write']
  for pan in range(len(ZJHXASAa)):
    print(ZJHXASAa[pan])
  print('\n')
if ZJHJASAa !=[] :
  ZJHJASAa.insert(0,'配置中金互金业务区思科墙ZGCB-ZJB02-INTYW-FW01')
  ZJHJASAa.insert(1,'config t')
  ZJHJASAa+=['write']
  for pan in range(len(ZJHJASAa)):
    print(ZJHJASAa[pan])
  print('\n')
if ZJGLASAa !=[] :
  ZJGLASAa.insert(0,'配置中金管理业务区思科墙ZGCB-ZJB02-MGTYW-FW01')
  ZJGLASAa.insert(1,'config t')
  ZJGLASAa+=['write']
  for pan in range(len(ZJGLASAa)):
    print(ZJGLASAa[pan])
  print('\n')
if ZJBGASAa !=[] :
  ZJBGASAa.insert(0,'配置中金办公业务区思科墙ZGCB-ZJB02-OAYW-FW01')
  ZJBGASAa.insert(1,'config t')
  ZJBGASAa+=['write']
  for pan in range(len(ZJBGASAa)):
    print(ZJBGASAa[pan])
  print('\n')
if ZJYWASAa !=[] :
  ZJYWASAa.insert(0,'配置中金运维管理区思科墙ZGCB-ZJB02-OPMGT-FW01')
  ZJYWASAa.insert(1,'config t')
  ZJYWASAa+=['write']
  for pan in range(len(ZJYWASAa)):
    print(ZJYWASAa[pan])
  print('\n')
if ZJHLASAa !=[] :
  ZJHLASAa.insert(0,'配置中金互联网接入区思科墙ZGCB-ZJB04-INT-FW01')
  ZJHLASAa.insert(1,'config t')
  ZJHLASAa+=['write']
  for pan in range(len(ZJHLASAa)):
    print(ZJHLASAa[pan])
  print('\n')
if ZHWLASAa !=[] :
  ZHWLASAa.insert(0,'配置中金外联区思科墙ZGCB-ZJB06-EXT-FW01')
  ZHWLASAa.insert(1,'config t')
  ZHWLASAa+=['write']
  for pan in range(len(ZHWLASAa)):
    print(ZHWLASAa[pan])
  print('\n')

if  SJHLCSa!=[] :
  SJHLCS_celue = ['配置同城测试区深信服防火墙ZGCB-JXQA06-TEST-FW01']
  for b in range(len(SJHLCSa)):
    if SJHLCSa[b]["area: "] == ['s']:
      SJHLCS_celue[b] += ('\n源区域：test\n目的区域：core')
    if a[b]["area: "] == ['d']:
      SJHLCS_celue[b] += ('目的区域：core\n源区域：test')
    for c in SJHLCSa[b]["src: "]:
      test1 = '\n源地址：' + str(c) + '/32'
      SJHLCS_celue[b] += test1
    for c in SJHLCSa[b]["drc: "]:
      test2 = '\n目的地址 ' + str(c) + '/32'
      SJHLCS_celue[b] += test2
    for d in SJHLCSa[b]["dport: "]:
      test3 = '\n目的端口：' +d
      SJHLCS_celue[b] += test3

  for b in range(len(SJHLCS_celue)):
    print(SJHLCS_celue[b])
  print('\n')


if  SJHLUAT1a!=[] :
  SJHLUAT1a.insert(0,'配置同城测试区核心交换机ZGCB-JQXA06-TEST-CS01')
  SJHLUAT1a.insert(1,'config t')
  SJHLUAT1a.insert(2,'ip access-list extended uat-to-sit')
  SJHLUAT1a+=['write']
  for pan in range(len(SJHLUAT1a)):
    print(SJHLUAT1a[pan])
  print('\n')

if  SJHLUAT2a!=[] :
  SJHLUAT2a.insert(0,'配置同城测试区核心交换机ZGCB-JQXA06-TEST-CS01')
  SJHLUAT2a.insert(1,'config t')
  SJHLUAT2a.insert(2,'ip access-list extended uat-to-sit')
  SJHLUAT2a+=['write']
  for pan in range(len(SJHLUAT2a)):
    print(SJHLUAT2a[pan])
  print('\n')

if  SJHLSHUJa!=[] :
  SJHLSHUJa.insert(0,'配置同城测试区核心交换机ZGCB-JQXA06-TEST-CS01')
  SJHLSHUJa.insert(1,'config t')
  SJHLSHUJa.insert(2,'ip access-list extended dashuju')
  SJHLSHUJa+=['write']
  for pan in range(len(SJHLSHUJa)):
    print(SJHLSHUJa[pan])
  print('\n')

if  WTOA3250a!=[] :
  WTOA3250a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3250a.insert(1,'acl advanced 3250')
  WTOA3250a+=['save force']
  for pan in range(len(WTOA3250a)):
    print(WTOA3250a[pan])
  print('\n')

if  WTOA3251a!=[] :
  WTOA3250a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3250a.insert(1,'acl advanced 3250')
  WTOA3250a+=['save force']
  for pan in range(len(WTOA3250a)):
    print(WTOA3250a[pan])
  print('\n')

if  WTOA3253a!=[] :
  WTOA3253a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3253a.insert(1,'acl advanced 3253')
  WTOA3253a+=['save force']
  for pan in range(len(WTOA3253a)):
    print(WTOA3253a[pan])
  print('\n')

if  WTOA3157a!=[] :
  WTOA3157a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3157a.insert(1,'acl advanced 3250')
  WTOA3157a+=['save force']
  for pan in range(len(WTOA3157a)):
    print(WTOA3157a[pan])
  print('\n')

if  WTOA3258a!=[] :
  WTOA3258a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3258a.insert(1,'acl advanced 3258')
  WTOA3258a+=['save force']
  for pan in range(len(WTOA3258a)):
    print(WTOA3258a[pan])
  print('\n')

if  WTOA3259a!=[] :
  WTOA3259a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3259a.insert(1,'acl advanced 3259')
  WTOA3259a+=['save force']
  for pan in range(len(WTOA3259a)):
    print(WTOA3259a[pan])
  print('\n')

if  WTOA3260a!=[] :
  WTOA3260a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3260a.insert(1,'acl advanced 3260')
  WTOA3260a+=['save force']
  for pan in range(len(WTOA3260a)):
    print(WTOA3260a[pan])
  print('\n')

if  WTOA3261a!=[] :
  WTOA3261a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3261a.insert(1,'acl advanced 3261')
  WTOA3261a+=['save force']
  for pan in range(len(WTOA3261a)):
    print(WTOA3261a[pan])
  print('\n')

if  WTOA3262a!=[] :
  WTOA3262a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3262a.insert(1,'acl advanced 3262')
  WTOA3262a+=['save force']
  for pan in range(len(WTOA3262a)):
    print(WTOA3262a[pan])
  print('\n')

if  WTOA3263a!=[] :
  WTOA3263a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3263a.insert(1,'acl advanced 3263')
  WTOA3263a+=['save force']
  for pan in range(len(WTOA3263a)):
    print(WTOA3263a[pan])
  print('\n')

if  WTOA3307a!=[] :
  WTOA3307a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3307a.insert(1,'acl advanced 3307')
  WTOA3307a+=['save force']
  for pan in range(len(WTOA3307a)):
    print(WTOA3307a[pan])
  print('\n')

if  WTOA3308a!=[] :
  WTOA3308a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3308a.insert(1,'acl advanced 3308')
  WTOA3308a+=['save force']
  for pan in range(len(WTOA3308a)):
    print(WTOA3308a[pan])
  print('\n')

if  WTOA3335a!=[] :
  WTOA3335a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3335a.insert(1,'acl advanced 3335')
  WTOA3335a+=['save force']
  for pan in range(len(WTOA3335a)):
    print(WTOA3335a[pan])
  print('\n')

if  WTOA3344a!=[] :
  WTOA3344a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3344a.insert(1,'acl advanced 3344')
  WTOA3344a+=['save force']
  for pan in range(len(WTOA3344a)):
    print(WTOA3344a[pan])
  print('\n')

if  WTOA3345a!=[] :
  WTOA3345a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3345a.insert(1,'acl advanced 3345')
  WTOA3345a+=['save force']
  for pan in range(len(WTOA3345a)):
    print(WTOA3345a[pan])
  print('\n')

if  WTOA3347a!=[] :
  WTOA3347a.insert(0,'配置卫通核心交换机ZGCB-WT26F-CORE-CS01')
  WTOA3347a.insert(1,'acl advanced 3347')
  WTOA3347a+=['save force']
  for pan in range(len(WTOA3347a)):
    print(WTOA3347a[pan])
  print('\n')

if  YHOAIPa!=[] :
  YHOAIP_celue = []
  for b in range(len(YHOAIPa)):
    YHOAIP_celue.append('\nrule\n action permit\n log policy-deny\n log session-start\n log session-end')
    if YHOAIPa[b]["area: "] == ['s']:
      YHOAIP_celue[b] += ('\n src-zone trust\n drc-zone untrust')
    if YHOAIPa[b]["area: "] == ['d']:
      YHOAIP_celue[b] += ('\n src-zone untrust\n drc-zone trust')
    for c in YHOAIPa[b]["src: "]:
      test1 = '\n src-ip ' + str(c) + '/32'
      YHOAIP_celue[b] += test1
    for c in YHOAIPa[b]["drc: "]:
      test2 = '\n dst-ip ' + str(c) + '/32'
      YHOAIP_celue[b] += test2
    for d in YHOAIPa[b]["dport: "]:
      test3 = '\n service ' + '"' + d + '"'
      YHOAIP_celue[b] += test3
    YHOAIP_celue[b] += '\n exit\n'

  for b in range(len(YHOAIPa)):
    for d in YHOAIPa[b]["dport: "]:
      test4 = 'service ' + '"' + d + '"'
      test5 = '\n ' + str.lower(d[:3]) + ' dst-port ' + d[4:]
      test6 = '\nexit'
      test7 = test4 + test5 + test6
      YHOAIP_celue.insert(0,test7)
  YHOAIP_celue.insert(0,'配置卫通办公区山石防火墙ZGCB-WT26F-NGFW01')
  for b in range(len(YHOAIP_celue)):
    print(YHOAIP_celue[b])

if  YHOA152a!=[] :
  YHOA152a.insert(0,'配置裕惠迈普核心交换机YHDS-9F-HXSW01')
  YHOA152a.insert(1,'config t')
  YHOA152a.insert(2,'ip access-list extended ceshi-152')
  YHOA152a+=['write']
  for pan in range(len(YHOA152a)):
    print(YHOA152a[pan])
  print('\n')

if  YHOA165a!=[] :
  YHOA165a.insert(0,'配置裕惠迈普核心交换机YHDS-9F-HXSW01')
  YHOA165a.insert(1,'config t')
  YHOA165a.insert(2,'ip access-list extended waixie')
  YHOA165a+=['write']
  for pan in range(len(YHOA165a)):
    print(YHOA165a[pan])
  print('\n')

if  YHOASHIPINa!=[] :
  YHOA165a.insert(0,'配置裕惠迈普核心交换机YHDS-9F-HXSW01')
  YHOA165a.insert(1,'config t')
  YHOA165a.insert(2,'ip access-list extended shipinhuiyi')
  YHOA165a+=['write']
  for pan in range(len(YHOA165a)):
    print(YHOA165a[pan])
  print('\n')

if  SJHLHXHILLa!=[] :
  SJHLHXHILLA_celue = []
  for b in range(len(SJHLHXHILLa)):
    SJHLHXHILLA_celue.append('\nrule\n action permit\n log policy-deny\n log session-start\n log session-end')
    if SJHLHXHILLa[b]["area: "] == ['s']:
      SJHLHXHILLA_celue[b] += ('\n src-zone trust\n drc-zone untrust')
    if SJHLHXHILLa[b]["area: "] == ['d']:
      SJHLHXHILLA_celue[b] += ('\n src-zone untrust\n drc-zone trust')
    for c in SJHLHXHILLa[b]["src: "]:
      test1 = '\n src-ip ' + str(c) + '/32'
      SJHLHXHILLA_celue[b] += test1
    for c in SJHLHXHILLa[b]["drc: "]:
      test2 = '\n dst-ip ' + str(c) + '/32'
      SJHLHXHILLA_celue[b] += test2
    for d in SJHLHXHILLa[b]["dport: "]:
      test3 = '\n service ' + '"' + d + '"'
      SJHLHXHILLA_celue[b] += test3
    SJHLHXHILLA_celue[b] += '\n exit\n'

  for b in range(len(SJHLHXHILLa)):
    for d in SJHLHXHILLa[b]["dport: "]:
      test4 = 'service ' + '"' + d + '"'
      test5 = '\n ' + str.lower(d[:3]) + ' dst-port ' + d[4:]
      test6 = '\nexit'
      test7 = test4 + test5 + test6
      SJHLHXHILLA_celue.insert(0,test7)
  SJHLHXHILLA_celue.insert(0,'配置同城核心业务区山石防火墙ZGCB-JXQB01-COREYW-FW01')
  for b in range(len(SJHLHXHILLA_celue)):
    print(SJHLHXHILLA_celue[b])

if  SJHLHX3000a!=[] :
  WTOA3344a.insert(0,'配置同城核心交换机ZGCB-JXQB01-COREYW-CS01')
  WTOA3344a.insert(1,'acl advanced 3000')
  WTOA3344a+=['save force']
  for pan in range(len(WTOA3344a)):
    print(WTOA3344a[pan])
  print('\n')

if  SJHLHJHILLa!=[] :
  SJHLHJHILLa_celue = []
  for b in range(len(SJHLHJHILLa)):
    SJHLHJHILLa_celue.append('\nrule\n action permit\n log policy-deny\n log session-start\n log session-end')
    if SJHLHJHILLa[b]["area: "] == ['s']:
      SJHLHJHILLa_celue[b] += ('\n src-zone trust\n drc-zone untrust')
    if SJHLHJHILLa[b]["area: "] == ['d']:
      SJHLHJHILLa_celue[b] += ('\n src-zone untrust\n drc-zone trust')
    for c in SJHLHJHILLa[b]["src: "]:
      test1 = '\n src-ip ' + str(c) + '/32'
      SJHLHJHILLa_celue[b] += test1
    for c in SJHLHJHILLa[b]["drc: "]:
      test2 = '\n dst-ip ' + str(c) + '/32'
      SJHLHJHILLa_celue[b] += test2
    for d in SJHLHJHILLa[b]["dport: "]:
      test3 = '\n service ' + '"' + d + '"'
      SJHLHJHILLa_celue[b] += test3
    SJHLHJHILLa_celue[b] += '\n exit\n'

  for b in range(len(SJHLHJHILLa)):
    for d in SJHLHJHILLa[b]["dport: "]:
      test4 = 'service ' + '"' + d + '"'
      test5 = '\n ' + str.lower(d[:3]) + ' dst-port ' + d[4:]
      test6 = '\nexit'
      test7 = test4 + test5 + test6
      SJHLHJHILLa_celue.insert(0,test7)
  SJHLHJHILLa_celue.insert(0,'配置同城互金业务区山石防火墙ZGCB-JXQB01-INTYW-FW01')
  for b in range(len(SJHLHJHILLa_celue)):
    print(SJHLHJHILLa_celue[b])

if  SJHLHJ3000a!=[] :
  SJHLHJ3000a.insert(0,'配置同城互金业务区核心交换机ZGCB-JXQB01-INTYW-CS01')
  SJHLHJ3000a.insert(1,'acl advanced 3000')
  SJHLHJ3000a+=['save force']
  for pan in range(len(SJHLHJ3000a)):
    print(SJHLHJ3000a[pan])
  print('\n')

if  SJHLGLHILLa!=[] :
  SJHLGLHILLA_celue = []
  for b in range(len(SJHLGLHILLa)):
    SJHLGLHILLA_celue.append('\nrule\n action permit\n log policy-deny\n log session-start\n log session-end')
    if SJHLGLHILLa[b]["area: "] == ['s']:
      SJHLGLHILLA_celue[b] += ('\n src-zone trust\n drc-zone untrust')
    if SJHLGLHILLa[b]["area: "] == ['d']:
      SJHLGLHILLA_celue[b] += ('\n src-zone untrust\n drc-zone trust')
    for c in SJHLGLHILLa[b]["src: "]:
      test1 = '\n src-ip ' + str(c) + '/32'
      SJHLGLHILLA_celue[b] += test1
    for c in SJHLGLHILLa[b]["drc: "]:
      test2 = '\n dst-ip ' + str(c) + '/32'
      SJHLGLHILLA_celue[b] += test2
    for d in SJHLGLHILLa[b]["dport: "]:
      test3 = '\n service ' + '"' + d + '"'
      SJHLGLHILLA_celue[b] += test3
    SJHLGLHILLA_celue[b] += '\n exit\n'

  for b in range(len(SJHLGLHILLa)):
    for d in SJHLGLHILLa[b]["dport: "]:
      test4 = 'service ' + '"' + d + '"'
      test5 = '\n ' + str.lower(d[:3]) + ' dst-port ' + d[4:]
      test6 = '\nexit'
      test7 = test4 + test5 + test6
      SJHLGLHILLA_celue.insert(0,test7)
  SJHLGLHILLA_celue.insert(0,'配置同城管理业务区山石防火墙ZGCB-JXQB01-MGTYW-FW01')
  for b in range(len(SJHLGLHILLA_celue)):
    print(SJHLGLHILLA_celue[b])

if  SJHLGL3000a!=[] :
  SJHLGL3000a.insert(0,'配置同城管理业务区核心交换机ZGCB-JXQB01-MGTYW-CS01')
  SJHLGL3000a.insert(1,'acl advanced 3000')
  SJHLGL3000a+=['save force']
  for pan in range(len(SJHLGL3000a)):
    print(SJHLGL3000a[pan])
  print('\n')

if  SJHLGL3001a!=[] :
  SJHLGL3001a.insert(0,'配置同城管理业务区核心交换机ZGCB-JXQB01-MGTYW-CS01')
  SJHLGL3001a.insert(1,'acl advanced 3001')
  SJHLGL3001a+=['save force']
  for pan in range(len(SJHLGL3001a)):
    print(SJHLGL3001a[pan])
  print('\n')

if  SJHLBGHILLa!=[] :
  SJHLBGHILLA_celue = []
  for b in range(len(SJHLBGHILLa)):
    SJHLBGHILLA_celue.append('\nrule\n action permit\n log policy-deny\n log session-start\n log session-end')
    if SJHLBGHILLa[b]["area: "] == ['s']:
      SJHLBGHILLA_celue[b] += ('\n src-zone trust\n drc-zone untrust')
    if SJHLBGHILLa[b]["area: "] == ['d']:
      SJHLBGHILLA_celue[b] += ('\n src-zone untrust\n drc-zone trust')
    for c in SJHLBGHILLa[b]["src: "]:
      test1 = '\n src-ip ' + str(c) + '/32'
      SJHLBGHILLA_celue[b] += test1
    for c in SJHLBGHILLa[b]["drc: "]:
      test2 = '\n dst-ip ' + str(c) + '/32'
      SJHLBGHILLA_celue[b] += test2
    for d in SJHLBGHILLa[b]["dport: "]:
      test3 = '\n service ' + '"' + d + '"'
      SJHLBGHILLA_celue[b] += test3
    SJHLBGHILLA_celue[b] += '\n exit\n'

  for b in range(len(SJHLBGHILLa)):
    for d in SJHLBGHILLa[b]["dport: "]:
      test4 = 'service ' + '"' + d + '"'
      test5 = '\n ' + str.lower(d[:3]) + ' dst-port ' + d[4:]
      test6 = '\nexit'
      test7 = test4 + test5 + test6
      SJHLBGHILLA_celue.insert(0,test7)
  SJHLBGHILLA_celue.insert(0,'配置同城办公业务区山石防火墙ZGCB-JXQB01-0AYW-FW01')
  for b in range(len(SJHLBGHILLA_celue)):
    print(SJHLBGHILLA_celue[b])

if  SJHLBG3000a!=[] :
  SJHLBG3000a.insert(0,'配置办公业务区核心交换机ZGCB-JXQB01-OAYW-CS01')
  SJHLBG3000a.insert(1,'acl advanced 3000')
  SJHLBG3000a+=['save force']
  for pan in range(len(SJHLBG3000a)):
    print(SJHLBG3000a[pan])
  print('\n')

if  SJHLYGHILLa!=[] :
  SJHLYGHILLA_celue = []
  for b in range(len(SJHLYGHILLa)):
    SJHLYGHILLA_celue.append('\nrule\n action permit\n log policy-deny\n log session-start\n log session-end')
    if SJHLYGHILLa[b]["area: "] == ['s']:
      SJHLYGHILLA_celue[b] += ('\n src-zone trust\n drc-zone untrust')
    if SJHLYGHILLa[b]["area: "] == ['d']:
      SJHLYGHILLA_celue[b] += ('\n src-zone untrust\n drc-zone trust')
    for c in SJHLYGHILLa[b]["src: "]:
      test1 = '\n src-ip ' + str(c) + '/32'
      SJHLYGHILLA_celue[b] += test1
    for c in SJHLYGHILLa[b]["drc: "]:
      test2 = '\n dst-ip ' + str(c) + '/32'
      SJHLYGHILLA_celue[b] += test2
    for d in SJHLYGHILLa[b]["dport: "]:
      test3 = '\n service ' + '"' + d + '"'
      SJHLYGHILLA_celue[b] += test3
    SJHLYGHILLA_celue[b] += '\n exit\n'

  for b in range(len(SJHLYGHILLa)):
    for d in SJHLYGHILLa[b]["dport: "]:
      test4 = 'service ' + '"' + d + '"'
      test5 = '\n ' + str.lower(d[:3]) + ' dst-port ' + d[4:]
      test6 = '\nexit'
      test7 = test4 + test5 + test6
      SJHLYGHILLA_celue.insert(0,test7)
  SJHLYGHILLA_celue.insert(0,'配置同城运维管理区山石防火墙ZGCB-JXQB03-OPMGT-FW01')
  for b in range(len(SJHLYGHILLA_celue)):
    print(SJHLYGHILLA_celue[b])

if  SJHLYG3697a!=[] :
  SJHLYG3697a.insert(0,'配置同城运维管理区核心交换机ZGCB-JXQB03-OPMGT-CS01')
  SJHLYG3697a.insert(1,'acl advanced 3697')
  SJHLYG3697a+=['save force']
  for pan in range(len(SJHLYG3697a)):
    print(SJHLYG3697a[pan])
  print('\n')

if  SJHLWLHILLa!=[] :
  SJHLWLHILLA_celue = []
  for b in range(len(SJHLWLHILLa)):
    SJHLWLHILLA_celue.append('\nrule\n action permit\n log policy-deny\n log session-start\n log session-end')
    if SJHLWLHILLa[b]["area: "] == ['s']:
      SJHLWLHILLA_celue[b] += ('\n src-zone untrust\n drc-zone trust')
    if SJHLWLHILLa[b]["area: "] == ['d']:
      SJHLWLHILLA_celue[b] += ('\n src-zone trust\n drc-zone untrust')
    for c in SJHLWLHILLa[b]["src: "]:
      test1 = '\n src-ip ' + str(c) + '/32'
      SJHLWLHILLA_celue[b] += test1
    for c in SJHLWLHILLa[b]["drc: "]:
      test2 = '\n dst-ip ' + str(c) + '/32'
      SJHLWLHILLA_celue[b] += test2
    for d in SJHLWLHILLa[b]["dport: "]:
      test3 = '\n service ' + '"' + d + '"'
      SJHLWLHILLA_celue[b] += test3
    SJHLWLHILLA_celue[b] += '\n exit\n'

  for b in range(len(SJHLWLHILLa)):
    for d in SJHLWLHILLa[b]["dport: "]:
      test4 = 'service ' + '"' + d + '"'
      test5 = '\n ' + str.lower(d[:3]) + ' dst-port ' + d[4:]
      test6 = '\nexit'
      test7 = test4 + test5 + test6
      SJHLWLHILLA_celue.insert(0,test7)
  SJHLWLHILLA_celue.insert(0,'配置同城外联区山石防火墙ZGCB-JXQB03-EXT-FW01')
  for b in range(len(SJHLWLHILLA_celue)):
    print(SJHLWLHILLA_celue[b])

if  SJHLHLHILLa!=[] :
  SJHLHLHILLA_celue = []
  for b in range(len(SJHLHLHILLa)):
    SJHLHLHILLA_celue.append('\nrule\n action permit\n log policy-deny\n log session-start\n log session-end')
    if SJHLHLHILLa[b]["area: "] == ['s']:
      SJHLHLHILLA_celue[b] += ('\n src-zone untrust\n drc-zone trust')
    if SJHLHLHILLa[b]["area: "] == ['d']:
      SJHLHLHILLA_celue[b] += ('\n src-zone trust\n drc-zone untrust')
    for c in SJHLHLHILLa[b]["src: "]:
      test1 = '\n src-ip ' + str(c) + '/32'
      SJHLHLHILLA_celue[b] += test1
    for c in SJHLHLHILLa[b]["drc: "]:
      test2 = '\n dst-ip ' + str(c) + '/32'
      SJHLHLHILLA_celue[b] += test2
    for d in SJHLHLHILLa[b]["dport: "]:
      test3 = '\n service ' + '"' + d + '"'
      SJHLHLHILLA_celue[b] += test3
    SJHLHLHILLA_celue[b] += '\n exit\n'

  for b in range(len(SJHLHLHILLa)):
    for d in SJHLHLHILLa[b]["dport: "]:
      test4 = 'service ' + '"' + d + '"'
      test5 = '\n ' + str.lower(d[:3]) + ' dst-port ' + d[4:]
      test6 = '\nexit'
      test7 = test4 + test5 + test6
      SJHLHLHILLA_celue.insert(0,test7)
  SJHLHLHILLA_celue.insert(0,'配置同城互联网接入区山石防火墙ZGCB-JXQB05-INT-FW01')
  for b in range(len(SJHLHLHILLA_celue)):
    print(SJHLHLHILLA_celue[b])




