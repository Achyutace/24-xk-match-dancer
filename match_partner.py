import numpy as np
import pandas as pd
import csv

'''
以下所有代码中：
wp: with partner
mp: match partner
'''

class DataLoader():
    
    def __init__(self,filepath,filename) -> None:
        '''
        param NUM : 总人数
        param MATCH : 匹配的人数
        '''
        self.NUM = 220
        self.MATCH = 140
        self.wp_df = None
        self.mp_df = None
        self.filepath = filepath
        self.filename = filename
class DataPreprocess(DataLoader):
    '''
    数据预处理，我也不知道我当时为什么要写成继承。。。可能是刚学会练练手
    '''
    def __init__(self, filepath,filename) -> None:
        super().__init__(filepath,filename)

    def data_cleansing(self):
        '''
        数据清洗的第一步！！
        然后初步分成wp_df和mp_df
        '''
        # 读入csv
        df = pd.read_csv(self.filepath)
        # 保留每个id最后一次填写的内容
        df = df.drop_duplicates(subset='3、你的电话号码是？', keep='last')
        # 分成wp_df和mp_df
        self.wp_df = df[df['9、你选择自带舞伴还是匹配舞伴？'] == 1]
        self.mp_df = df[df['9、你选择自带舞伴还是匹配舞伴？'] == 2]
        # 第一次打印日志
        print(f"最后一次填写自带舞伴的学生数: {len(self.wp_df)}")
        print(f"最后一次填写需要匹配舞伴的学生数: {len(self.mp_df)}") 
        # 进行双向匹配
        self.validate_wp_partners()
        # 第二次打印日志
        print(f"自带舞伴的学生数: {len(self.wp_df)}")
        combined_df = pd.concat([self.wp_df, self.mp_df], ignore_index=True)
    
        # 保存合并后的数据到指定路径
        combined_df.to_csv(f'./preprocessed_data/combined{self.filename}_data.csv', index=False)

    def validate_wp_partners(self):
        '''
        筛选出所有进行双向配对的舞伴
        '''
        # 创建一个集合来存储有效的自带舞伴的手机号
        valid_wp_phones = set()        # 遍历自带舞伴的数据
        for index, row in self.wp_df.iterrows():
            partner_phone = int(row['11、你的舞伴的电话号码是？'])
            # your_phone = int(row['3、你的电话号码是？'])
            # print(partner_phone,'and',your_phone,'and',row['序号'])
            # 检查舞伴是否也在问卷中并且选择了自带舞伴
            if partner_phone in self.wp_df['3、你的电话号码是？'].values:
                partner_row = self.wp_df[self.wp_df['3、你的电话号码是？'] == partner_phone]
                if not partner_row.empty and partner_row.iloc[0]['11、你的舞伴的电话号码是？'] == row['3、你的电话号码是？'] :
                    # 双方都填写了问卷并且把对方作为舞伴
                    valid_wp_phones.add(row['3、你的电话号码是？'])
                    valid_wp_phones.add(partner_phone)
        # 过滤出有效的自带舞伴数据
        self.wp_df = self.wp_df[self.wp_df['3、你的电话号码是？'].isin(valid_wp_phones)]
        # 创建一个新的数据框来存储配对后的数据
        paired_df = pd.DataFrame(columns=self.wp_df.columns)
        
        # 遍历有效的舞伴数据，将每一对舞伴的记录添加到新的数据框中
        for phone in valid_wp_phones:
            partner_phone = self.wp_df[self.wp_df['3、你的电话号码是？'] == phone]['11、你的舞伴的电话号码是？'].values[0]
            if phone < partner_phone:  # 确保每一对只添加一次
                pair = self.wp_df[(self.wp_df['3、你的电话号码是？'] == phone) | (self.wp_df['3、你的电话号码是？'] == partner_phone)]
                paired_df = pd.concat([paired_df, pair])
        # 生成一个csv，两列，存储配对情况，第一列是自己手机号，第二列是舞伴手机号
        # 生成配对情况的CSV文件
        pair_list = []
        for phone in valid_wp_phones:
            partner_phone = self.wp_df[self.wp_df['3、你的电话号码是？'] == phone]['11、你的舞伴的电话号码是？'].values[0]
            if phone < partner_phone:  # 确保每一对只添加一次
                pair_list.append([phone, partner_phone])

        pair_df = pd.DataFrame(pair_list, columns=['自己手机号', '舞伴手机号'])
        pair_df.to_csv(f'./data/{self.filename}_paired_list.csv', index=False)
        # 将新的数据框赋值给 self.wp_df
        self.wp_df = paired_df
    
    def save_df(self):
        self.wp_df.to_csv(f"./data/preprocessed_{self.filename}_wp_df.csv", index=False)
        self.mp_df.to_csv(f"./data/preprocessed_{self.filename}_mp_df.csv", index=False)

class MatchPartner(DataLoader):
    '''
    继承自DataLoader，接口只需要输入各种filepath，和filename即可自动完成数据筛选和配对。
    '''
    def __init__(self,filepath,filename,mp_filepath) -> None:
        super().__init__(filepath,filename)
        self.mp_df = pd.read_csv(mp_filepath)
    def calculate_fitness(self, row1, row2):
        # 计算两个人匹配适合度
        fitness = 0
        
        # 是否想遇见同院系搭档
        if row1['17、你希望舞伴的院系是？'] ==1 and row1['7、你的院系是？'] == row2['7、你的院系是？']:
            fitness += 3
        
       # 是否想遇见不同院系搭档
        if row1['17、你希望舞伴的院系是？'] ==2 and row1['7、你的院系是？'] != row2['7、你的院系是？']:
            fitness += 1

        if row1['19、你希望你的舞伴更加外向还是内向？'] == row1['18、你更加外向还是内向？'] :
            fitness += 1


        # 院系无所谓
        if row1['17、你希望舞伴的院系是？'] ==3:
            fitness += 1
        
        # 希望舞伴的舞蹈水平
        if row1['21、你希望你舞伴的跳舞水平？'] == row2['20、你的跳舞水平？']:
            fitness += (2 - abs(row1['21、你希望你舞伴的跳舞水平？']-row2['20、你的跳舞水平？']))
        
        return fitness
    
    def construct_fitness_matrix(self):
        # 构造一个len(matchPartner)*len(matchPartner)的表格
        num_mp = len(self.mp_df)
        fitness_matrix = np.zeros((num_mp, num_mp))
        
        for i in range(num_mp):
            for j in range(num_mp):
                if i != j:
                    fitness_matrix[i, j] = self.calculate_fitness(self.mp_df.iloc[i], self.mp_df.iloc[j])+1
        # print(fitness_matrix)
        return fitness_matrix
    
    def apply_gender_constraints(self, fitness_matrix):
        num_mp = len(self.mp_df)
        for i in range(num_mp):
            for j in range(num_mp):
                if self.mp_df.iloc[i]['2、你的性别是？'] == (3 - self.mp_df.iloc[j]['16、你希望舞伴的性别是？']):
                    fitness_matrix[i, j] = -1
                if i==j:
                    fitness_matrix[i, j] = -2
        return fitness_matrix
        
    def greedy_matching(self, fitness_matrix):
        num_mp = len(self.mp_df)
        matched_pairs = []
        matched_indices = set()
        
        for i in range(num_mp):
            if i not in matched_indices:
                max_fitness = -1
                max_index = -1
                for j in range(num_mp):
                    if j not in matched_indices and fitness_matrix[i, j] > max_fitness and fitness_matrix[j,i]>=0:
                        max_fitness = fitness_matrix[i, j]
                        max_index = j
                if max_index != -1:
                    matched_pairs.append((i, max_index))
                    matched_indices.add(i)
                    matched_indices.add(max_index)
        
        return matched_pairs 
    def match_partners_with_preferences(self):
        # Step 5: 构造一个len(matchPartner)*len(matchPartner)的表格
        fitness_matrix = self.construct_fitness_matrix()
        
        # Step 6: 根据想要匹配舞伴的性别和自己的性别，把某些匹配适合度设置为0
        fitness_matrix = self.apply_gender_constraints(fitness_matrix)
        
        # Step 7: 从第一个数据开始，用贪心算法选匹配到的舞伴
        matched_indices = self.greedy_matching(fitness_matrix)
        print(matched_indices)

        # 将匹配结果转换为DataFrame
        matched_pairs = []
        for pair in matched_indices:
            matched_pairs.append(self.mp_df.iloc[pair[0]])
            matched_pairs.append(self.mp_df.iloc[pair[1]])
        matched_df = pd.DataFrame(matched_pairs)

        
        # 保存匹配结果到CSV文件
        matched_df.to_csv(f'{self.filename}_preferences.csv', index=False)


if __name__ == "__main__":
    '''
    当时测试用的代码，现在已经不适用
    '''
    # preprocess = DataPreprocess('./test.csv')
    preprocess = DataPreprocess('./dancer-data.csv','dancer')
    preprocess.data_cleansing()
    preprocess.save_df()
    match_partner = MatchPartner('./dancer-data.csv', 'matched', './data/preprocessed_dancer_mp_df.csv')
    match_partner.match_partners_with_preferences()