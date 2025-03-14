import pandas as pd
class RmAlready():
    '''
    对于文件md和sd，我们选出md/(md交sd)并存储在output_path中
    应用场景：我们选出了220个参加周日舞会的同学，数据存在selected_data中, 现在把这220行数据从main_data(所有数据)中删掉
    '''
    def __init__(self,md,sd,o_path):
        self.main_data = pd.read_csv(md)
        self.selected_data = pd.read_csv(sd)
        self.o_path = o_path
    def rm(self):

        # 找到两个数据框中相同的行
        common_rows = pd.merge(self.main_data, self.selected_data, how='inner')

        # 从 main_data 中删除相同的行
        filtered_data = self.main_data[~self.main_data.isin(common_rows.to_dict('list')).all(axis=1)]

        # 计算删除了多少行
        num_removed_rows = len(self.main_data) - len(filtered_data)

        # 保存结果到新的CSV文件
        filtered_data.to_csv('', index=False)

        # 打印删除了多少行，对于本例如果没有报错，应该是删除了220行
        print(f"删除了 {num_removed_rows} 行")

if __name__ == "__main__":
    '''
    应用实例
    '''
    m_filepath = pd.read_csv('./preprocessed_data/lstfri.csv')
    s_filepath = pd.read_csv('./friday_preferences.csv')
    tem = RmAlready(m_filepath,s_filepath,'./preprocessed_data/unlucky.csv')
    tem.rm()
