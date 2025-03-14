import pandas as pd
from match_partner import DataPreprocess,MatchPartner
# 从preprocessed_data/combined_data.csv读入数据
filepath = './data'
data = pd.read_csv('preprocessed_data/combineddancer_data.csv')

# 选出所有5、(10月13日（星期日）)一项值为1.0的
sun_first = data[data['5、(10月13日（星期日）)'] == 1.0]

# 选出所有5、(10月13日（星期日）)一项值为2.0的
sun_second = data[data['5、(10月13日（星期日）)'] == 2.0]

# 选出所有5、(10月13日（星期日）)一项值为3.0的
sun_third = data[data['5、(10月13日（星期日）)'] == 3.0]

# 将结果保存到data文件夹下
sun_first.to_csv('data/sunfirst.csv', index=False)
sun_second.to_csv('data/sunsecond.csv', index=False)
sun_third.to_csv('data/sunthird.csv', index=False)



# 把sun_first和sun_second拼起来,存在./data/raw.csv中
combined_data = pd.concat([sun_first, sun_second], ignore_index=True)
combined_data.to_csv('./data/raw.csv', index=False)
sun_process = DataPreprocess('./data/sunfirst.csv','sunfir')
sun_process.data_cleansing()
sun_process.save_df()
sun_match =  MatchPartner('./preprocessed_data/combined_data.csv', 'sunday','./data/preprocessed_sunfir_mp_df.csv')
sun_match.match_partners_with_preferences()