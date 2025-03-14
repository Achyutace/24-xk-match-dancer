import pandas as pd
from match_partner import DataPreprocess,MatchPartner
# 从preprocessed_data/combined_data.csv读入数据
filepath = './data'
data = pd.read_csv('preprocessed_data/frisat.csv')

# 选出所有5、(10月12日（星期六）)一项值为1.0的
sat_first = data[data['5、(10月12日（星期六）)'] == 1.0]

# 选出所有5、(10月12日（星期六）)一项值为2.0的
sat_second = data[data['5、(10月12日（星期六）)'] == 2.0]

# 选出所有5、(10月12日（星期六）)一项值为3.0的
sat_third = data[data['5、(10月12日（星期六）)'] == 3.0]

# 将结果保存到data文件夹下
sat_first.to_csv('data/satfirst.csv', index=False)
sat_second.to_csv('data/satsecond.csv', index=False)
sat_third.to_csv('data/satthird.csv', index=False)



# 把sat_first和sat_second拼起来,存在./data/raw.csv中
combined_data = pd.concat([sat_first, sat_second], ignore_index=True)
combined_data.to_csv('./data/raw.csv', index=False)
sat_process = DataPreprocess('./data/raw.csv','satday')
sat_process.data_cleansing()
sat_process.save_df()
sat_process = DataPreprocess('./data/satsecond.csv','satsec')
sat_process.data_cleansing()
sat_process.save_df()
sat_match =  MatchPartner('./preprocessed_data/combined_data.csv', 'satday','./data/preprocessed_satday_wp_df.csv', './data/preprocessed_satday_mp_df.csv')
sat_match.match_partners_with_preferences()