import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import nan as NA
import seaborn as sns
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
pd.set_option('display.width',None)

path = r'C:\Users\Administrator\Desktop\sales.xlsx'
df = pd.read_excel(path , header=0 , names=['用户ID' , '下单日期' , '订单ID' , '消费金额'])
df['月份'] = df['下单日期'].values.astype('datetime64[M]')
df['订单ID'] = df['订单ID'].apply(str)
# print(df.info())
# print(df.head())
df_new = df.dropna()
# print(df_new.isnull().sum())
# print(df_new.info())

                                                          # 用户消费金额
user_amount_sum = df_new.groupby('用户ID')['消费金额'].sum().reset_index()
# print(user_amount_sum.head())
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.style.use('ggplot')
# user_amount_sum['消费金额'].head().plot(kind='bar')
# plt.grid(True)
# plt.show()

                                                           # 累积消费金额
# DataFrame 进行groupby（'某个列名'）后该列名会变成index ， 返回一个DataFrame
amout_sorted = df_new.groupby('用户ID').sum().sort_values('消费金额' , ascending=False)
# print(df_new.head())
# print(amout_sorted.head())
# del amout_sorted['订单ID']
user_cumsum = amout_sorted.apply(lambda x: x.cumsum()/x.sum())
# # print(amout_sorted.head())
# print(user_cumsum.head())
# user_cumsum.reset_index().消费金额.plot(fontsize=12)
# plt.grid(True)
# plt.show()

                                                             # 月消费人数
month_people = df_new.groupby('月份')['订单ID'].apply(lambda x: len(x.drop_duplicates())).sum()
# print(month_people)

                                                           # 用户平均消费金额
user_per = df_new.groupby(['月份' , '用户ID']).sum().reset_index().groupby('月份')['消费金额'].mean()
# print(user_per)

                                                                # 复购率
pivot_counts = df_new.pivot_table(index='用户ID' , columns='月份' , values='下单日期' , aggfunc='count').fillna(0)
# print(pivot_counts.head())
purchase_r = pivot_counts.applymap(lambda x:1 if x>1 else NA if x==0 else 0)
# print(purchase_r.head())
# df_fougou = purchase_r.sum()/purchase_r.count()
# print(df_fougou.head())
# plt.figure(figsize=(10,5))
# df_fougou.plot()
# plt.title('用户复购率图')
# plt.ylabel('复购率')
# plt.grid(True)
# plt.show()

                                                            #回购率
# pivot_amount = df_new.pivot_table(index='用户ID' , columns='月份' , values='消费金额' , aggfunc='mean').fillna(0)
# pivot_purchase = pivot_amount.applymap(lambda x:1 if x>0 else 0)
# columns_month = df_new['月份'].sort_values().astype('str').unique()
# # print(pivot_purchase.head())
# def purchase_back(data):
#   status = []
#   for i in range(11):
#     if data[i] == 1:
#       if data[i+1] == 1:
#         status.append(1)
#       if data[i+1] == 0:
#         status.append(0)
#     else:
#         status.append(NA)
#   status.append(NA)
#   return pd.Series(status ,pivot_amount.columns)
# purchase_b = pivot_purchase.apply(purchase_back , axis=1)
# df_huigou = purchase_b.sum()/purchase_b.count()
# # print(purchase_b.head())
# print(df_huigou)
# plt.figure(figsize=(12,5))
# df_huigou.plot()
# plt.title('回购率图')
# plt.ylabel('回购率')
# plt.grid(True)
# plt.show()

                                                                 # 用户生命周期
user_life = df_new.groupby('用户ID')['下单日期'].agg(['min' , 'max'])
# print(user_life.head())
user_life_day = user_life['max'] - user_life['min']
# print(user_life_day.head())
# print(user_life_day.describe())
day_percent = (user_life['min'] == user_life['max']).value_counts()
# print(day_percent)
# day_percent.plot(kind='bar', alpha=0.3 , width=0.3)
# plt.show()
u_l = user_life_day.reset_index()
u_l.rename(columns={0 : '天数'} , inplace=True)
# print(u_l.head())
u_d = u_l['天数']/np.timedelta64(1 , 'D')
print(u_d.head())
u_d[u_d>0].hist(bins=40 , color='purple')
plt.title('二次消费以上用户的生命周期直方图')
plt.xlabel('天数' , fontsize=15)
plt.ylabel('人数', fontsize=15)
plt.show()
