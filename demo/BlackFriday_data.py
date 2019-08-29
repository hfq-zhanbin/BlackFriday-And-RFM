import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
pd.set_option('display.width',None)


path = r'C:\Users\Administrator\Desktop\bf.xlsx'
df = pd.read_excel(path)
dt = df.dropna(axis='columns')
del dt['Product_Category_1']

# 销售的画像 ；销售总额，用户总数及用户人均消费金额，商品总量
columns_replace = {"User_ID" : "用户ID" , "Product_ID" : "商品ID" , "Gender" : "性别" , "Age" : "年龄" , "Occupation" : "职业"
                   , "City_Category" : "城市分类" , "Stay_In_Current_City_Years" : "在目前城市的居住的年数" , "Marital_Status" : "婚姻状态" , "Purchase" :"购买金额"}
bf_replace = dt.rename(columns=columns_replace)
print(bf_replace.head())
# 从一个数据集dataframe里选取某几列构成新的dataframe
# b = bf_replace[['用户ID' , '商品ID']]
# print(b)
# print(type(b))

# 销售总额
purchase_sum = bf_replace["购买金额"].sum()

# 用户总数
user_count = bf_replace.drop_duplicates('用户ID')['用户ID'].count()
# print("用户总数:",user_count)

# 用户平均消费金额
user_avg = bf_replace['购买金额'].sum()/bf_replace['用户ID'].count()
# print("用户平均消费金额：" , user_avg)

# 商品总量
product_sum = bf_replace.drop_duplicates("商品ID")["商品ID"].count()
# print("商品总量：" , product_sum)

# 男女消费金额分布情况
consumption_info = bf_replace.groupby("性别")["购买金额"].sum().to_frame().reset_index()
# print(consumption_info)

# 用户性别分布情况(考虑了先把用户ID先去重后再分组)
gender_info = bf_replace.drop_duplicates('用户ID').groupby('性别')['用户ID'].count().to_frame().reset_index()
gender_info["分布比例"] = gender_info['用户ID']/gender_info["用户ID"].sum()
gender_info["消费比例"] = consumption_info["购买金额"]/consumption_info['购买金额'].sum()
del gender_info["用户ID"]
del gender_info["性别"]
arr = {}
fb_list = gender_info['分布比例'].values.tolist()
xf_list = gender_info['消费比例'].values.tolist()
arr['分布比例'] = fb_list
arr['消费比例'] = xf_list
data_info = pd.DataFrame(arr , columns=['分布比例' , '消费比例'] , index=['女性' , '男性'])
# print(data_info.T)


# plt.style.use("fivethirtyeight")
# sns.set_style({'font.sans-serif':['simhei','Arial']}) #设置字体
# data_info.T.plot.barh(alpha=0.5)
# plt.show()
# labels = ['Male','Female']
# x = [consumption_info["M"],consumption_info["F"]]
# x1 = [gender_info['M'] , gender_info['F']]
# explode = (0.1,0)
# plt.pie(x,labels=labels,autopct='%.0f%%',textprops = {'fontsize':10,'color':'k'},
#        explode=explode,shadow=True,startangle=60,pctdistance = 0.5)
# plt.pie(x1,labels=labels,autopct='%.0f%%',textprops = {'fontsize':10,'color':'k'},
#        explode=explode,shadow=True,startangle=60,pctdistance = 0.5)
# plt.axis('equal')
# gender_info.plot.bar()
# plt.title('用户性别分布情况')
# plt.show()

# 用户年龄分布
# age_count = bf_replace.drop_duplicates('用户ID').groupby('年龄')['用户ID'].count().sort_values(ascending=False).to_frame().reset_index()
# print(age_count)
# x = age_count['年龄']
# y = age_count['用户ID']
# plt.plot(figsize=(15,10),c='b')
# plt.bar(x,y , alpha=0.5)
# plt.xlabel('年龄')
# plt.ylabel('个数')
# plt.title('用户年龄分布')
# sns.barplot(x=age_count['年龄'] , y=age_count['用户ID'] , data=age_count , alpha=0.5)
# plt.title('用户年龄分布图')
# plt.show()

# 用户职业分布和消费情况
user_occupation = bf_replace.drop_duplicates("用户ID").groupby("职业")["用户ID"].count().sort_values(ascending=False).to_frame().reset_index()
user_occupation.rename(columns={"用户ID" : "用户数"}, inplace=True)
print(user_occupation)
sns.barplot(x=user_occupation["职业"] , y=user_occupation["用户数"] ,data=user_occupation , alpha=0.5)
for x ,y in zip(user_occupation['职业'] , user_occupation['用户数']):
  plt.text(x , y+0.1,'%s' %y , ha='center' ,va= 'bottom')
plt.title('用户职业分布图')
plt.show()

# 用户婚姻分布和消费情况
# Marital_Status = bf_replace.drop_duplicates('用户ID').groupby('婚姻状态')['用户ID'].count()
# bf_replace.groupby('婚姻状态')['购买金额'].sum()
# bf_replace.groupby('婚姻状态')['购买金额'].sum()/dt.groupby('婚姻状态')['用户ID'].count()

# 最受喜爱的商品分布和消费情况
Product_top = bf_replace.groupby('商品ID')['用户ID'].count().sort_values(ascending=False).to_frame().reset_index()
# print(Product_top)
consumption_top = bf_replace.groupby('商品ID')['购买金额'].sum().sort_values(ascending=False).to_frame().reset_index()
# print(consumption_top)

# 男女消费者喜爱的商品分布和消费情况
# 男
male_consumption = bf_replace[bf_replace['性别'] == 'M'].groupby('商品ID')['用户ID'].count().sort_values(ascending=False).to_frame().reset_index().head(10)
# print(male_consumption)

# 女
female_consumption = bf_replace[bf_replace['性别'] == 'F'].groupby('商品ID')['用户ID'].count().sort_values(ascending=False).to_frame().reset_index().head(10)
# print(female_consumption)

