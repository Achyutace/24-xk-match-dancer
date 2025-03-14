import pandas as pd
from match_partner import DataPreprocess,MatchPartner
# 从preprocessed_data/combined_data.csv读入数据
filepath = './data'
data = pd.read_csv('preprocessed_data/lstfri.csv')

# 选出所有5、(10月11日（星期五）)一项值为1.0的
fri_first = data[data['5、(10月11日（星期五）)'] == 1.0]

# 选出所有5、(10月11日（星期五）)一项值为2.0的
fri_second = data[data['5、(10月11日（星期五）)'] == 2.0]

# 选出所有5、(10月11日（星期五）)一项值为3.0的
fri_third = data[data['5、(10月11日（星期五）)'] == 3.0]

# 将结果保存到data文件夹下
fri_first.to_csv('data/frifirst.csv', index=False)
fri_second.to_csv('data/frisecond.csv', index=False)
fri_third.to_csv('data/frithird.csv', index=False)



# 把fri_first和fri_second拼起来,存在./data/raw.csv中
combined_data = pd.concat([fri_first, fri_second], ignore_index=True)
combined_data.to_csv('./data/raw.csv', index=False)
fri_process = DataPreprocess('./data/raw.csv','friday')
fri_process.data_cleansing()
fri_process.save_df()
fri_process = DataPreprocess('./data/frisecond.csv','frisec')
fri_process.data_cleansing()
fri_process.save_df()
fri_process = DataPreprocess('./data/frifirst.csv','frifir')
fri_process.data_cleansing()
fri_process.save_df()
fri_match =  MatchPartner('./preprocessed_data/combined_data.csv', 'friday','./data/preprocessed_friday_wp_df.csv', './data/preprocessed_friday_mp_df.csv')
fri_match.match_partners_with_preferences()