import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
pd.set_option('display.width',None)

path = r'C:\Users\Administrator\Desktop\sales.xlsx'
dtypes = {'ORDERDATA' : object , 'ORDERID' : object , 'AMOUNTINFO' : np.float32}
rfm_data = pd.read_excel(path , dtype=dtypes , index_col='USERID')
# rfm_data['ORDERID'] = rfm_data['ORDERID'].apply('str')
# print(rfm_data.info())
# print(rfm_data.describe())
rfm_na = rfm_data.isnull().sum()
# print(rfm_na)

# 查看每一列是否有空值
na_cols = rfm_data.isnull().any(axis=0)
# print('NA_cols:')
# print(na_cols)

# 查看每一行是否有空值
na_lines = rfm_data.isnull().any(axis=1)
# print('NA_LINES:')
# print(na_lines)

# 查看具有缺失行的信息
# print(rfm_data[na_lines])

# 丢弃带有缺失值的行
sales_data = rfm_data.dropna()
# print(sales_data.head())

# 丢弃订单金额小于等于1的记录
sales_data = sales_data[sales_data['AMOUNTINFO']>1]
# print(sales_data)

sales_data['ORDERDATE'] = pd.to_datetime(sales_data['ORDERDATE'] , format='%Y-%m-%d')
# print(sales_data.head())

                                                 # 构建RFM模型
# 1 查看总体数据是否有na值
sales_na = sales_data.isnull().sum()
# print(sales_na)

# 2 计算个ID用户最近一次时间的下单时间，即R值，越小越好
recency_values = sales_data.groupby('USERID')['ORDERDATE'].max()
# print(recency_values)

# 2.1 指定一个时间地点
deadline_date = pd.datetime(2017,1,1)
# 2.2 计算 R 值
r_interval = (deadline_date - recency_values).dt.days
# print(r_interval.head())

# 3 计算各个ID订单数量 , 即 F 值
f_interval = sales_data.groupby('USERID')['ORDERID'].count()
# print(f_interval)

# 4 计算各个ID的订单的总金额 , 即 M 值
m_interval = sales_data.groupby('USERID')['AMOUNTINFO'].sum()
# print(m_interval.head())

# print(sales_data.info())

# 分别计算 r ，f ，m 的值
r_score = pd.cut(r_interval , 5 , labels=[5,4,3,2,1])
# print(r_score.head())
f_score = pd.cut(f_interval , 5 , labels=[1,2,3,4,5])
# print(f_score.head())
m_score = pd.cut(m_interval , 5 , labels=[1,2,3,4,5])
# print(m_score.head())
rfm_list = [r_score , f_score , m_score]
# print(rfm_list)

# 设置R ,F ,M三个维度的列表
rfm_cols = ['r_score' , 'f_score' , 'm_score']
rfm_pd = pd.DataFrame(np.array(rfm_list).transpose() , columns=rfm_cols , index=f_interval.index , dtype=np.int32)
# print(rfm_pd.head())

# RFM组合
rfm_pd_tmp = rfm_pd.copy()
rfm_pd_tmp['r_score'] = rfm_pd_tmp['r_score'].astype('str')
rfm_pd_tmp['f_score'] = rfm_pd_tmp['f_score'].astype('str')
rfm_pd_tmp['m_score'] = rfm_pd_tmp['m_score'].astype('str')
rfm_pd['rfm_comb'] = rfm_pd_tmp['r_score'].str.cat(rfm_pd_tmp['f_score']).str.cat(rfm_pd_tmp['m_score'])
rfmm_data = rfm_pd
# print(rfmm_data.head())
# print(rfmm_data[rfmm_data['rfm_comb'] == '111'].index.values)
rfmm_group = rfmm_data.groupby('rfm_comb')['m_score'].count()
# print(rfmm_group.values)
dict_rfm = {'rfm' : rfmm_group.index , '个数' : rfmm_group.values}
rfm_new = pd.DataFrame(dict_rfm)
# print(rfm_new)
# #
# sns.barplot(x=rfm_new['rfm'] , y=rfm_new['个数'] , data=rfm_new , alpha = 0.8)
# for x ,y in enumerate(rfm_new['个数'].values):
#   plt.text(x , y+0.1,'%s' %y , ha='center' ,va= 'bottom' , fontsize = 12)
# plt.xticks(rotation = 0)
# plt.xlabel('RFM label' , fontsize=12)
# plt.title('The Frequency of RFM labels')
# plt.show()

                                                      #方法二
rfm = sales_data.pivot_table(index=['USERID'] , values=['AMOUNTINFO' , 'ORDERDATE' , 'ORDERID'] ,
                             aggfunc={'ORDERDATE': 'max' , 'AMOUNTINFO' : 'sum' , 'ORDERID':'count'})

rfm['R'] = (rfm['ORDERDATE'].max() - rfm['ORDERDATE']).dt.days
rfm.rename(columns={'AMOUNTINFO': 'M' , 'ORDERID': 'F'} , inplace=True)
def rfm_func(x):
  level = x.apply(lambda x : "1" if x>=1 else "0")
  label = level.R + level.F + level.M
  d = {
    '111': '重要价值客户',
    '011': '重要保持客户',
    '101': '重要发展客户',
    '001': '重要挽留客户',
    '110': '一般价值客户',
    '010': '一般保持客户',
    '100': '一般发展客户',
    '000': '一般挽留客户'
  }
  result = d[label]
  return result

rfm['label'] = rfm[['R' , 'F' , 'M']].apply(lambda x:x-x.mean()).apply(rfm_func , axis=1)
# print(rfm.head())
rfm_label = rfm.loc[rfm['label'] == '一般挽留客户'].reset_index()
print(rfm_label.USERID)
rfm_df = rfm.label.value_counts().reset_index()
plt.figure(figsize=(10,5))
sns.barplot(x=rfm_df['index'] , y=rfm_df['label'] , data=rfm_df ,alpha=0.7)
for x ,y in enumerate(rfm_df['label']):
  plt.text(x , y+0.1,'%s' %y , ha='center' ,va= 'bottom' , fontsize=14)
plt.xlabel('客户类型')
plt.ylabel('人数')
plt.title('RFM客户价值区分图')
plt.show()
print(rfm_df.head())
