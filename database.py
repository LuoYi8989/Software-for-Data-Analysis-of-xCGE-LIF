import pandas as pd
import os
from datetime import datetime
import datetime
import csv


class Database:
    def create_dataframe_from_csv(self, object):
        """将csv文件内容添加到一个dataframe中"""
        cwd = os.getcwd()
        print(cwd)
        if object == "GSL":
            self.dataframe_database = pd.read_csv(cwd+"/GSL_database.csv")
        elif object == "N glycans":
            self.dataframe_database = pd.read_csv(cwd+"/N_glycans_database.csv")
        elif object == "GAGs":
            self.dataframe_database = pd.read_csv(cwd+"/GAGs_database.csv")

        # 将date从string '2021/05/27'转换成datetime形式
        for index, row in self.dataframe_database.iterrows():
            try:
                self.dataframe_database['date'][index] = datetime.date(*map(int, self.dataframe_database['date'][index].split('/')))
            except:
                self.dataframe_database['date'][index] = datetime.date(
                    *map(int, self.dataframe_database['date'][index].split('-')))

        # self.dataframe_database['date'] = pd.to_datetime(self.dataframe_database['date'])
        # self.dataframe_database['date'] = self.dataframe_database['date'].apply(lambda x: datetime.strptime(x, '%Y/%m/%d'))
        self.dataframe_database = self.dataframe_database.sort_values(by=["MTU", "name_of_glycan", "date", "flag"],
                                                                      ignore_index=True)
        return self.dataframe_database

    def write_to_csv(self, record_list, object):
        """向csv文件写一行新数据"""
        # 规范record_list的格式 ["test1", 5.27, "2021/05/27", "manu"]
        record_list[1] = round(record_list[1], 2)  # 保留两位小数
        record_list[2] = record_list[2].replace("-", "/")
        print(record_list)
        # 打开文件，模式是'a'模式，追加内容
        if object == "GSL":
            info = open("GSL_database.csv", 'a', newline='')
        elif object == "N glycans":
            info = open("N_glycans_database.csv", 'a', newline='')
        elif object == "GAGs":
            info = open("GAGs_database.csv", 'a', newline='')

        # 定义一个变量进行写入，将刚才的文件变量传进来，dialect就是定义一下文件的类型，我们定义为excel类型
        csv_write = csv.writer(info, dialect='excel')

        # 进行数据的写入 写入的方法是writerow，通过写入模式对象，调用方法进行写入
        csv_write.writerow(record_list)

    def update_csv(self, dataframe, object):
        """将一个dataframe重新存储到csv文件中"""
        if object == "GSL":
            dataframe.to_csv("GSL_database.csv", index=False)
        elif object == "N glycans":
            dataframe.to_csv("N_glycans_database.csv", index=False)
        elif object == "GAGs":
            dataframe.to_csv("GAGs_database.csv", index=False)


if __name__ == "__main__":
    database = Database()  # the object of the class Database
    temp = database.create_dataframe_from_csv("GSL")
    print(temp)

    record_list = ["test1", 5.27, "2021-05-27", "manu"]
    database.write_to_csv(record_list, "GSL")

    temp2 = database.create_dataframe_from_csv("GSL")
    print(temp2)
