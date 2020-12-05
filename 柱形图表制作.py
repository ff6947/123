import matplotlib.pyplot as plt

y = [5, 20, 15, 25, 10,70,50,14,50,10.5]
x = [1,2,3,4,5,6,7,8,9,10]
# #配置字体为中文仿宋
plt.rcParams['font.sans-serif'] = ['STXihei']
#配置不显示负数
plt.rcParams['axes.unicode_minus'] = False
#Y轴刻度范围0-100
plt.ylim(0,100)
#配置图标标题
plt.title('数据中心巡检',size=30,weight=1,variant="small-caps")
#配置表格显示文本
plt.text(11,97,"A:  ZGCB-ZJB02-MGTYW-CS01")
plt.text(11,93,"B:  ZGCB-ZJB02-OAYW-CS01")
plt.text(11,89,"C:  ZGCB-ZJB02-OPMGT-CS01")

#配置X轴标题
plt.xlabel('设备名称',size=20)
#配置Y轴标题
plt.ylabel("百分比",size=20)
#配置图标网格
plt.grid(linestyle=":",color="r",alpha=0.2)
#配置柱形图
plt.bar(x,y, ec='m', ls='-',color=["m","c","g"],align="center",alpha=0.6,tick_label=["A","B","C","D","E","F","G","H","I","J"])
#配置线性图
plt.plot(x,y,c='b')
#展示图表
plt.show()
