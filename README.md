# Typecho_Fonts_Slimming
Typecho网站自定义字体根据数据库中的汉字进行动态瘦身

## 环境：
python3.10
fonttools
pymysql
pandas

通过链接typecho的数据库获取数据库中的中文汉字以及标点符号，然后通过fonttools对字体进行子集化，最后转为woff2替换掉网站现有的woff2文件
