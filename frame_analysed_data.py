"""根据4.22会议更改update database方法  update_method_of_Dong  Sorting2更新"""
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import tkinter.scrolledtext
import tkinter.messagebox
import os
import pandas as pd
import numpy as np
from database import Database
import copy
import datetime
import collections


class FrameAnalysedData(ttk.Frame):

    def __init__(self, master=None, raw_data=None, selected_data=None, analysis_option=None, version_database=None,
                 reference_sample=None, referencewell=None, nor_or_rel=None, normal_standard=None):
        super().__init__(master)
        self.master = master
        self.raw_data = raw_data
        self.selected_data = selected_data
        # 以上两个需要用户在tab_Overview中作出选择后传进来
        self.analysis_option = analysis_option
        self.version_database = version_database  # type:datetime
        self.reference_sample = reference_sample  # dict 名：数据  or None
        self.list_glycans_in_referencewell = referencewell  # or []
        self.nor_or_rel = nor_or_rel
        self.normal_standard = normal_standard
        if self.nor_or_rel == "Relativization":
            if self.normal_standard in self.list_glycans_in_referencewell:
                self.list_glycans_in_referencewell.remove(self.normal_standard)
        self.pack()

        self.database = Database()
        self.dataframe_database = self.database.create_dataframe_from_csv(self.analysis_option)

        # print("目标frame")
        # print(self.raw_data)
        # print(self.raw_data.columns)
        # print(self.analysis_option)
        # print(self.version_database)
        # # print(self.reference_sample.items())
        # print(self.list_glycans_in_referencewell)
        # print(self.nor_or_rel)
        # print(self.normal_standard)
        print("FrameAnalysedData")

        # 为了给frame_figure传参数
        self.annotated_result = None

        self.creatWidge()

    def canvas_process_mousewheel(self, event):
        """让canvas能够使用鼠标滚轮滑动"""
        self.canvas_process.yview_scroll(-1 * event.delta, "units")
        # self.canvas_choose_sample.yview_scroll(-1 * (event.delta / 120), "units")
        # 在 Windows 上，您绑定到<MouseWheel>并且需要除以event.delta120（或其他一些因素，具体取决于您希望滚动的速度）
        # 在 OSX 上，您绑定到<MouseWheel>并且您需要event.delta不加修改地使用

    def bound_to_canvas_process_mousewheel(self, event):
        self.canvas_process.bind_all("<MouseWheel>", self.canvas_process_mousewheel)

    def unbound_to_canvas_process_mousewheel(self, event):
        self.canvas_process.unbind_all("<MouseWheel>")

    def get_raw_data(self):
        try:
            self.raw_data
        except:
            # remainder: you need input a file in tab_Overview
            pass
        else:
            self.button_raw_data_view.config(state="normal")
            self.button_raw_data_download.config(state="normal")

    def show_raw_data(self):
        # 首先删除原有表单中的内容
        # if self.treeview_sheet_show_data.get_children() != ():
        #     exit = self.treeview_sheet_show_data.get_children()
        #     for item in exit:
        #         self.treeview_sheet_show_data.delete(item)

        # 先删除原有子组件
        for widget in self.frame_show_data.winfo_children():
            widget.destroy()

        # fill 以对齐->加滚轮
        # content = tk.Text(self.frame_show_data, width=0, height=600)
        # content.pack(anchor="w", side="left", expand=False)
        # content.configure(background=self.frame_main.cget('background'), highlightbackground=self.frame_main.cget('background'))
        # https://blog.csdn.net/qq_41878777/article/details/105726865?utm_medium=distribute.pc_relevant.none-task-blog-baidujs_title-0&spm=1001.2101.3001.4242

        self.treeview_sheet_show_data = ttk.Treeview(self.frame_show_data, height=600,
                                                     show='headings',
                                                     columns=self.raw_data.columns)
        self.scrollbar_y_show_data = ttk.Scrollbar(self.frame_show_data, orient='vertical')
        self.scrollbar_x_show_data = ttk.Scrollbar(self.frame_show_data, orient='horizontal')
        self.scrollbar_y_show_data.pack(fill="y", side="right")
        self.scrollbar_y_show_data.config(command=self.treeview_sheet_show_data.yview)
        self.scrollbar_x_show_data.pack(fill="x", side="bottom")
        self.scrollbar_x_show_data.config(command=self.treeview_sheet_show_data.xview)
        self.treeview_sheet_show_data.config(xscrollcommand=self.scrollbar_x_show_data.set)
        self.treeview_sheet_show_data.config(yscrollcommand=self.scrollbar_y_show_data.set)
        self.treeview_sheet_show_data.pack(fill="both", side="left", padx=5, pady=5, expand=1)
        # 添加
        for i, col in enumerate(self.raw_data.columns):
            self.treeview_sheet_show_data.heading(column="#" + str(i + 1), text=col)
            self.treeview_sheet_show_data.column(i, width=100, anchor='w')

        for index, row in self.raw_data.iterrows():
            temp = []
            for i, j in enumerate(self.raw_data.columns):
                temp.append(row[j])
            self.treeview_sheet_show_data.insert("", "end", values=temp)

    def download_raw_data(self):
        print("download")
        filename = tkinter.filedialog.asksaveasfilename()
        # filename = tkinter.filedialog.askopenfilename()
        print(filename)
        if not filename.endswith('.xls'):
            self.raw_data.to_excel(filename + '.xls')
        else:
            self.raw_data.to_excel(filename)

    def get_selected_data(self):
        try:
            self.selected_data
        except:
            # remainder: you need input a file in tab_Overview
            pass
        else:
            self.button_selected_data_view.config(state="normal")
            self.button_selected_data_download.config(state="normal")

    def show_selected_data(self):
        # 首先删除原有表单中的内容
        # if self.treeview_sheet_show_data.get_children() != ():
        #     exit = self.treeview_sheet_show_data.get_children()
        #     for item in exit:
        #         self.treeview_sheet_show_data.delete(item)

        # 先删除原有子组件
        for widget in self.frame_show_data.winfo_children():
            widget.destroy()

        self.treeview_sheet_show_data = ttk.Treeview(self.frame_show_data, height=600,
                                                     show='headings',
                                                     columns=list(self.selected_data.items())[0][1].columns)
        self.scrollbar_y_show_data = ttk.Scrollbar(self.frame_show_data, orient='vertical')
        self.scrollbar_x_show_data = ttk.Scrollbar(self.frame_show_data, orient='horizontal')
        self.scrollbar_y_show_data.pack(fill="y", side="right")
        self.scrollbar_y_show_data.config(command=self.treeview_sheet_show_data.yview)
        self.scrollbar_x_show_data.pack(fill="x", side="bottom")
        self.scrollbar_x_show_data.config(command=self.treeview_sheet_show_data.xview)
        self.treeview_sheet_show_data.config(xscrollcommand=self.scrollbar_x_show_data.set)
        self.treeview_sheet_show_data.config(yscrollcommand=self.scrollbar_y_show_data.set)
        self.treeview_sheet_show_data.pack(fill="both", side="left", padx=5, pady=5, expand=1)

        # 添加
        for i, col in enumerate(list(self.selected_data.items())[0][1].columns):
            self.treeview_sheet_show_data.heading(column="#" + str(i + 1), text=col)
            self.treeview_sheet_show_data.column(i, width=100, anchor='w')

        for num, each in enumerate(self.selected_data.items()):

            self.treeview_sheet_show_data.insert("", "end", values=list(self.selected_data.items())[num][0])

            for index, row in list(self.selected_data.items())[num][1].iterrows():
                temp = []
                for i, j in enumerate(list(self.selected_data.items())[num][1].columns):
                    temp.append(row[j])
                self.treeview_sheet_show_data.insert("", "end", values=temp)

    def download_selected_data(self):
        ### 先将dict数据转换成df格式
        df_selected_data = pd.DataFrame(columns=list(self.selected_data.items())[0][1].columns)
        for num, each in enumerate(self.selected_data.items()):
            df = list(self.selected_data.items())[num][1]
            df_selected_data = pd.concat([df_selected_data, df], axis=0)

        ### 存储成csv格式
        filename = tkinter.filedialog.asksaveasfilename()
        # filename = tkinter.filedialog.askopenfilename()
        print(filename)
        if not filename.endswith('.xls'):
            df_selected_data.to_excel(filename + '.xls')
        else:
            df_selected_data.to_excel(filename)

    def update_database_method_top(self, x_database, a_database, a_now, b_database, b_now):
        # 在相应version的database中 MTU glycan < a < b
        # x_database:待更新的glycan在相应version的database中 MTU
        # a_database referencewell中个glycan a的MTU，a_now本次试验测得的a的MTU
        # b_database referencewell中个glycan b的MTU，b_now本次试验测得的a的MTU

        update_value = b_now - (b_database - x_database) / (b_database - a_database) * (b_now - a_now)
        return update_value

    def update_database_method_end(self, x_database, a_database, a_now, b_database, b_now):
        # 在相应version的database中 MTU a < b < glycan
        # x_database:待更新的glycan在相应version的database中 MTU
        # a_database referencewell中个glycan a的MTU，a_now本次试验测得的a的MTU
        # b_database referencewell中个glycan b的MTU，b_now本次试验测得的a的MTU

        update_value = a_now + (x_database - a_database) / (b_database - a_database) * (b_now - a_now)
        return update_value

    def update_database_method_middle(self, x_database, a_database, a_now, b_database, b_now):
        # 在相应version的database中 MTU a < glycan < b
        # x_database:待更新的glycan在相应version的database中 MTU
        # a_database referencewell中个glycan a的MTU，a_now本次试验测得的a的MTU
        # b_database referencewell中个glycan b的MTU，b_now本次试验测得的a的MTU

        update_value = a_now + (x_database - a_database) / (b_database - a_database) * (b_now - a_now)
        return update_value

    def update_database(self):
        # self.reference_sample  # dict 名：数据
        # self.list_glycans_in_referencewell   # eg:['Lc4', 'Gn4', 'Lea penta']

        ### 获取database相应version中所有glycan的测量数据
        # 建立一个空的dataframe存放结果
        self.dataframe_of_chossen_version_database = pd.DataFrame(columns=self.dataframe_database.columns)
        # 获取所有glycan_name
        all_glycan_name = self.dataframe_database.loc[:, "name_of_glycan"].unique().tolist()
        # 找出所有self.dataframe_database中相应日期的添加到self.dataframe_of_chossen_version_database中
        index = self.dataframe_database[self.dataframe_database["date"] == self.version_database].index.tolist()
        for each in index:
            # print(self.dataframe_database.iloc[each, :])
            self.dataframe_of_chossen_version_database = self.dataframe_of_chossen_version_database.append(
                self.dataframe_database.iloc[each, :], ignore_index=True)
            all_glycan_name.remove(self.dataframe_database.iloc[each, 0])  # 将添加过的glycan剔除
        # 对于all_glycan_name中其他的glycan添加空值
        for each in all_glycan_name:
            temp = {"name_of_glycan": each, "MTU": None, "date": self.version_database, "flag": None}
            self.dataframe_of_chossen_version_database = self.dataframe_of_chossen_version_database.append(temp,
                                                                                                           ignore_index=True)
        self.dataframe_of_chossen_version_database.sort_values(by=["MTU", "name_of_glycan"], ignore_index=True,
                                                               inplace=True)
        self.dataframe_of_chossen_version_database["MTU"] = self.dataframe_of_chossen_version_database["MTU"].astype(
            float)  # 将MTU由str转换成float
        # 将dataframe转换成dict形式
        df = collections.OrderedDict(zip(self.dataframe_of_chossen_version_database.loc[:, "name_of_glycan"],
                                         self.dataframe_of_chossen_version_database.loc[:, "MTU"]))
        self.dict_all_glycans_in_database_version = dict(df)
        print("---------------------------------------------------")
        print(self.dict_all_glycans_in_database_version)

        # --------------------------------------------------------------------------------------------------------------
        if self.reference_sample == None:
            self.dict_glycans_in_referencewell_database = {}
            self.dict_glycans_in_referencewell_now = {}
            self.dict_all_glycans_in_database_update = self.dict_all_glycans_in_database_version
            self.button_update_database_view.config(state="normal")
            self.button_update_database_download.config(state="normal")
            return
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        ### 找到referencewell每个对应的version的MTU
        self.dict_glycans_in_referencewell_database = {}  # glycan:version_MTU
        for each in self.list_glycans_in_referencewell:
            self.dict_glycans_in_referencewell_database[each] = self.dict_all_glycans_in_database_version[each]
        print(self.dict_glycans_in_referencewell_database)

        # --------------------------------------------------------------------------------------------------------------
        ### 在self.reference_sample的数据中，根据self.dict_glycans_in_referencewell的值找到本次实验对应glycan的MTU
        self.dict_glycans_in_referencewell_now = {}  # glycan:this_time_MTU 本次实验中测得的MTU
        for each in self.dict_glycans_in_referencewell_database.items():
            print('each[0], each[1]')
            print(each[0], each[1])
            diff = float('inf')
            temp_MTU = None
            for index, record in list(self.reference_sample.items())[0][1].iterrows():
                if abs(each[1] - float(record[2])) < diff:
                    diff = abs(each[1] - float(record[2]))
                    temp_MTU = float(record[2])
            # print("temp_MTU", temp_MTU)
            self.dict_glycans_in_referencewell_now[each[0]] = temp_MTU
            # print(self.dict_glycans_in_referencewell_now[each[0]])
        print("referencewell_now")
        print(self.dict_glycans_in_referencewell_now)

        # --------------------------------------------------------------------------------------------------------------
        ### 更新database中所有glycan的MTU数据
        """先计算待更新的glycan和referencewell中所有glycan的距离，再判断用哪一种更新方法"""
        self.dict_all_glycans_in_database_update = {}  # database中所有glycan的更新数据
        if self.list_glycans_in_referencewell == []:
            self.dict_all_glycans_in_database_update = self.dict_all_glycans_in_database_version
            self.button_update_database_view.config(state="normal")
            self.button_update_database_download.config(state="normal")
            return

        # self.dict_all_glycans_in_database_update = self.dict_all_glycans_in_database_version
        for each in self.dict_all_glycans_in_database_version.items():  # 对于每个glycan进行更新

            if each[0] in self.dict_glycans_in_referencewell_now:  # each是referencewell，直接更新
                self.dict_all_glycans_in_database_update[each[0]] = self.dict_glycans_in_referencewell_now[each[0]]
                continue

            # if each[1] == None:
            if np.isnan(each[1]):
                print("None")
                self.dict_all_glycans_in_database_update[each[0]] = None
                continue

            ## each不是referencewell 且有value值

            # 计算每个glycan和所有referencewell中glycans的距离
            distance_dict = {}
            for temp in self.dict_glycans_in_referencewell_database.items():
                distance_dict[temp[0]] = abs(temp[1] - each[1])
            distance_sort = sorted(distance_dict.items(), key=lambda item: item[1])  # [(),()] 从小到大排序
            # 找出离待更新glycan最近的两个referencewell_glycan
            a_name = distance_sort[0][0]
            a_database = self.dict_all_glycans_in_database_version[a_name]
            a_now = self.dict_glycans_in_referencewell_now[a_name]
            b_name = distance_sort[1][0]
            b_database = self.dict_all_glycans_in_database_version[b_name]
            b_now = self.dict_glycans_in_referencewell_now[b_name]

            # 判断用哪种方法更新each
            if each[1] < a_database:
                update_value = self.update_database_method_top(each[1], a_database, a_now, b_database, b_now)
            elif each[1] > b_database:
                update_value = self.update_database_method_end(each[1], a_database, a_now, b_database, b_now)
            else:
                update_value = self.update_database_method_middle(each[1], a_database, a_now, b_database, b_now)

            self.dict_all_glycans_in_database_update[each[0]] = round(update_value, 2)

        print("self.dict_all_glycans_in_database_update")
        print(self.dict_all_glycans_in_database_update)

        self.button_update_database_view.config(state="normal")
        self.button_update_database_download.config(state="normal")

    def show_update_database(self):
        # if self.treeview_sheet_show_data.get_children() != ():
        #     exit = self.treeview_sheet_show_data.get_children()
        #     for item in exit:
        #         self.treeview_sheet_show_data.delete(item)

        # 先删除原有子组件
        for widget in self.frame_show_data.winfo_children():
            widget.destroy()

        self.treeview_sheet_show_data = ttk.Treeview(self.frame_show_data, height=600,
                                                     show='headings',
                                                     columns=["a", "b"])
        self.scrollbar_y_show_data = ttk.Scrollbar(self.frame_show_data, orient='vertical')
        self.scrollbar_x_show_data = ttk.Scrollbar(self.frame_show_data, orient='horizontal')
        self.scrollbar_y_show_data.pack(fill="y", side="right")
        self.scrollbar_y_show_data.config(command=self.treeview_sheet_show_data.yview)
        self.scrollbar_x_show_data.pack(fill="x", side="bottom")
        self.scrollbar_x_show_data.config(command=self.treeview_sheet_show_data.xview)
        self.treeview_sheet_show_data.config(xscrollcommand=self.scrollbar_x_show_data.set)
        self.treeview_sheet_show_data.config(yscrollcommand=self.scrollbar_y_show_data.set)
        self.treeview_sheet_show_data.pack(fill="both", side="left", padx=5, pady=5, expand=1)

        # 添加
        col = ["name_of_glycan", "MTU"]
        for i, j in enumerate(["a", "b"]):
            self.treeview_sheet_show_data.heading(column="#" + str(i + 1), text=col[i])
            self.treeview_sheet_show_data.column(i, width=450, anchor='w')

        # 1. glycan_latest_MTU in referencewell    self.dict_glycans_in_referencewell_database
        self.treeview_sheet_show_data.insert("", "end", values=["the MTU of the glycans in referencewell at version %s"
                                                                % str(self.version_database), ''])
        for num, each in enumerate(self.dict_glycans_in_referencewell_database.items()):
            temp = [each[0], each[1]]
            self.treeview_sheet_show_data.insert("", "end", values=temp)
        self.treeview_sheet_show_data.insert("", "end", values=['', ''])

        # 2.glycan_this_time_MTU in referencewell    self.dict_glycans_in_referencewell_now
        self.treeview_sheet_show_data.insert("", "end",
                                             values=["the MTU of the glycans in referencewell at this time", ''])
        for num, each in enumerate(self.dict_glycans_in_referencewell_now.items()):
            temp = [each[0], each[1]]
            self.treeview_sheet_show_data.insert("", "end", values=temp)
        self.treeview_sheet_show_data.insert("", "end", values=['', ''])

        # 3.self.dict_all_glycans_in_database_version
        self.treeview_sheet_show_data.insert("", "end", values=["the MTU of all glycans in database of version %s" %
                                                                str(self.version_database), ''])
        for num, each in enumerate(self.dict_all_glycans_in_database_version.items()):
            temp = [each[0], each[1]]
            self.treeview_sheet_show_data.insert("", "end", values=temp)
        self.treeview_sheet_show_data.insert("", "end", values=['', ''])

        # 4.self.dict_all_glycans_in_database_update
        self.treeview_sheet_show_data.insert("", "end", values=["the updated MTU of all glycans in database", ''])
        for num, each in enumerate(self.dict_all_glycans_in_database_update.items()):
            temp = [each[0], each[1]]
            self.treeview_sheet_show_data.insert("", "end", values=temp)
        self.treeview_sheet_show_data.insert("", "end", values=['', ''])

    def download_update_database(self):
        ### 先将dict数据转换成df格式    self.dict_all_glycans_in_database_update  self.dict_all_glycans_in_database_version
        # 行号为glycan_name, 两列: MTU_in_database, MTU_update
        df_update_database = pd.DataFrame(columns=["MTU_in_database", "MTU_update"],
                                          index=list(self.dict_all_glycans_in_database_update.keys()))
        for num, each in enumerate(self.dict_all_glycans_in_database_update.items()):
            df_update_database.loc[each[0], "MTU_in_database"] = self.dict_all_glycans_in_database_version[each[0]]
            df_update_database.loc[each[0], "MTU_update"] = self.dict_all_glycans_in_database_update[each[0]]
        print(df_update_database)

        ### 存储成csv格式
        filename = tkinter.filedialog.asksaveasfilename()
        # filename = tkinter.filedialog.askopenfilename()
        print(filename)
        if not filename.endswith('.xls'):
            df_update_database.to_excel(filename + '.xls')
        else:
            df_update_database.to_excel(filename)

    def analysis_of_nor_or_rel(self):
        # self.selected_data   self.normal_standard
        self.dict_nor_or_rel = copy.deepcopy(self.selected_data)  # 存放最终结果

        if self.nor_or_rel == "Normalization":
            index = []  # index: 搜索结果在self.dataframe_database中的编号
            temp = []  # 根据index编号，将结果放在该列表里

            ### 先找到数据库中self.normal_standard最新测量的MTU
            index = self.dataframe_database[
                self.dataframe_database["name_of_glycan"] == self.normal_standard].sort_values('date',
                                                                                               ascending=False).index.tolist()

            if index != []:
                temp = []
                for i, col in enumerate(self.dataframe_database.columns):
                    temp.append(self.dataframe_database.iloc[index[0], i])
            self.latest_MTU_normal_standard = float(temp[1])
            print(temp)
            print("self.latest_MTU_normal_standard", self.latest_MTU_normal_standard)

            ### Normalization
            for temp in self.dict_nor_or_rel.items():
                standard_MTU = None
                standard_Intensity = None
                diff_min = float("inf")
                for index, value in temp[1].iterrows():
                    diff = abs((value["Size"] - self.latest_MTU_normal_standard))
                    if diff < diff_min:
                        diff_min = diff
                        standard_Intensity = value["Height"]
                        standard_MTU = value["Size"]
                temp[1]["Height"] = round(temp[1]["Height"].div(standard_Intensity), 2)

        if self.nor_or_rel == "Relativization":
            sum_of_absolute_signal_intensities = {}
            for temp in self.dict_nor_or_rel.items():  # each Sample
                temp_sum = temp[1]["Height"].sum()
                sum_of_absolute_signal_intensities[temp[0]] = temp_sum
                temp[1]["Height"] = round(temp[1]["Height"].div(temp_sum) * 100, 2)  # 以百分比呈现

        print(self.dict_nor_or_rel)
        self.button_nor_or_rel_view.config(state="normal")
        self.button_nor_or_rel_download.config(state="normal")

    def show_nor_or_rel(self):
        # 首先删除原有表单中的内容
        # if self.treeview_sheet_show_data.get_children() != ():
        #     exit = self.treeview_sheet_show_data.get_children()
        #     for item in exit:
        #         self.treeview_sheet_show_data.delete(item)

        # 先删除原有子组件
        for widget in self.frame_show_data.winfo_children():
            widget.destroy()

        self.treeview_sheet_show_data = ttk.Treeview(self.frame_show_data, height=600,
                                                     show='headings',
                                                     columns=list(self.dict_nor_or_rel.items())[0][1].columns)
        self.scrollbar_y_show_data = ttk.Scrollbar(self.frame_show_data, orient='vertical')
        self.scrollbar_x_show_data = ttk.Scrollbar(self.frame_show_data, orient='horizontal')
        self.scrollbar_y_show_data.pack(fill="y", side="right")
        self.scrollbar_y_show_data.config(command=self.treeview_sheet_show_data.yview)
        self.scrollbar_x_show_data.pack(fill="x", side="bottom")
        self.scrollbar_x_show_data.config(command=self.treeview_sheet_show_data.xview)
        self.treeview_sheet_show_data.config(xscrollcommand=self.scrollbar_x_show_data.set)
        self.treeview_sheet_show_data.config(yscrollcommand=self.scrollbar_y_show_data.set)
        self.treeview_sheet_show_data.pack(fill="both", side="left", padx=5, pady=5, expand=1)

        # 添加
        for i, col in enumerate(list(self.dict_nor_or_rel.items())[0][1].columns):
            self.treeview_sheet_show_data.heading(column="#" + str(i + 1), text=col)
            self.treeview_sheet_show_data.column(i, width=100, anchor='w')

        for num, each in enumerate(self.dict_nor_or_rel.items()):

            self.treeview_sheet_show_data.insert("", "end", values=list(self.dict_nor_or_rel.items())[num][0])

            for index, row in list(self.dict_nor_or_rel.items())[num][1].iterrows():
                temp = []
                for i, j in enumerate(list(self.dict_nor_or_rel.items())[num][1].columns):
                    temp.append(row[j])
                self.treeview_sheet_show_data.insert("", "end", values=temp)

    def download_nor_or_rel(self):
        # self.dict_nor_or_rel
        ### 先将dict数据转换成df格式
        df_nor_or_rel = pd.DataFrame(columns=list(self.dict_nor_or_rel.items())[0][1].columns)
        for num, each in enumerate(self.dict_nor_or_rel.items()):
            df = list(self.dict_nor_or_rel.items())[num][1]
            df_nor_or_rel = pd.concat([df_nor_or_rel, df], axis=0)

        ### 存储成csv格式
        filename = tkinter.filedialog.asksaveasfilename()
        # filename = tkinter.filedialog.askopenfilename()
        print(filename)
        if not filename.endswith('.xls'):
            df_nor_or_rel.to_excel(filename + '.xls')
        else:
            df_nor_or_rel.to_excel(filename)


    def sort_data_by_MTU(self):
        # self.sort_ranging  self.dict_nor_or_rel
        sample_name = list(self.dict_nor_or_rel.keys())

        sort_data_columns_name = []
        for temp in sample_name:
            sort_data_columns_name.append(temp + "_Size")
            sort_data_columns_name.append(temp + "_Height")

        self.sort_data_by_MTU = pd.DataFrame(columns=sort_data_columns_name)  # 最终返回结果

        all_dataframes = copy.deepcopy(self.dict_nor_or_rel)
        min_in_sorted = float("inf")
        unsorted_sample = {temp[0]: [temp[1]["Size"].iloc[0], temp[1]["Height"].iloc[0]] for temp in
                           all_dataframes.items()}
        while all_dataframes != {}:
            min_in_sorted = float("inf")
            each_line_sorted = {each_sample: [None, 0] for each_sample in sample_name}  # 大表中排好序的每一行的sample_name
            # ----------------- 本次循环结束 代表大表中每一行排序结束-----------------------
            for each in range(len(sample_name)):
                min_sample = min(unsorted_sample.items(),
                                 key=lambda a: a[1])  # ('dfD07_DS4.fsa': [0.13, 1.4615384615384615]) 找到本轮未排序的最小值
                if min_in_sorted == float("inf"):  # 判断之前是否排序过
                    min_in_sorted = min_sample[1][0]
                    each_line_sorted[min_sample[0]] = min_sample[1]
                    #     print(all_dataframes[min_sample[0]])
                    # ---------把各个DataFrame中添加到each_line_sorted里的行删掉--------
                    all_dataframes[min_sample[0]].drop(index=0, inplace=True)
                    all_dataframes[min_sample[0]] = all_dataframes[min_sample[0]].reset_index(drop=True)
                    # ---------更新未排序的相应的值--------
                    unsorted_sample[min_sample[0]] = [float("inf"), float("inf")]

                else:  # 判断排过序的最小值和未排序的最小值是否相差1以内
                    if min_sample[1][0] - min_in_sorted <= self.var_sort_ranging.get():
                        # min_in_sorted = min_sample[1][0]
                        each_line_sorted[min_sample[0]] = min_sample[1]
                        # ---------把各个DataFrame中添加到each_line_sorted里的行删掉--------
                        all_dataframes[min_sample[0]].drop(0, inplace=True)
                        all_dataframes[min_sample[0]] = all_dataframes[min_sample[0]].reset_index(drop=True)
                        # ---------更新未排序的相应的值--------
                        unsorted_sample[min_sample[0]] = [float("inf"), float("inf")]
                    else:  # 跳出该行排序
                        break

            # ------------ 大表中每一行排序结束  将each_line_sorted更新到大表中  更新unsorted_sample----------
            temp_dict = {}
            for each in each_line_sorted.items():
                temp_dict[each[0] + "_Size"] = each[1][0]
                temp_dict[each[0] + "_Height"] = each[1][1]
            self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)

            delete = []
            for each in unsorted_sample.items():
                if each[1] == [float("inf"), float("inf")]:
                    #             print(len(all_dataframes[each[0]]))
                    #             print(each[0])
                    if len(all_dataframes[each[0]]) == 0:
                        all_dataframes.pop(each[0])
                        delete.append(each[0])
                    else:
                        unsorted_sample[each[0]] = [all_dataframes[each[0]]["Size"].iloc[0],
                                                    all_dataframes[each[0]]["Height"].iloc[0]]
            for each in delete:  # all_dataframes中删除掉的samplename, unsorted_sample中也要删除
                unsorted_sample.pop(each)

        ###  add mean MTU column
        self.sort_data_by_MTU["mean_MTU"] = round(self.sort_data_by_MTU[
                                                      [i for i in self.sort_data_by_MTU.columns.tolist() if
                                                       i.find("Size") != -1]].mean(axis=1), 2)

        print(self.sort_data_by_MTU)
        self.button_sort_data_by_MTU_view.config(state="normal")
        self.button_sort_data_by_MTU_download.config(state="normal")


    def help_std(self, info):
        # info = {"a":[1,2],"b":[2,3],"c":[9,8]} #求1，2，9方差
        # 不管为空的
        value = []
        for i, j in enumerate(info.items()):  # j = ('a', [1, 2])
            if j[1][0] != None:
                value.append(j[1][0])
        if value == []:
            std = 0
        else:
            std = np.std(np.array(value))
        return std

    # def help_std2(self, info):
    #     # 为空的设置为0参与std  效果不好
    #     value = []
    #     for i, j in enumerate(info.items()):  # j = ('a', [1, 2])
    #         if j[1][0] != None:
    #             value.append(j[1][0])
    #         else:
    #             value.append(0)
    #     print(value)
    #     return np.std(np.array(value))


    def sort_data_by_MTU2(self):
        # 两次std比较中，第一次只比较当前行，第二次比较(std当前行+std上一行)
        # self.sort_ranging  self.dict_nor_or_rel
        sample_name = list(self.dict_nor_or_rel.keys())

        sort_data_columns_name = []
        for temp in sample_name:
            sort_data_columns_name.append(temp + "_Size")
            sort_data_columns_name.append(temp + "_Height")

        self.sort_data_by_MTU = pd.DataFrame(columns=sort_data_columns_name)  # 最终返回结果

        current_index = [0 for i in range(len(sample_name))]  # 每个sample当前排序到的位置
        current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
        current_sort_line_replace = {each_sample: [None, 0] for each_sample in sample_name}  # current_sort_line_before

        while True:
            current_info = {}
            for i, j in enumerate(sample_name):
                if current_index[i] == None:
                    current_info[j] = [None, 0]
                else:
                    current_info[j] = [self.dict_nor_or_rel[j].iloc[current_index[i], 2], self.dict_nor_or_rel[j].iloc[current_index[i], 3]]
            # current_info = {j: [self.dict_nor_or_rel[j].iloc[current_index[i], 2], self.dict_nor_or_rel[j].iloc[current_index[i], 3]] for i, j in enumerate(sample_name)}
            # info = {"a":[1,2],"b":[2,3],"c":[9,8]}
            # 每个sample当前排序到的位置的信息

            # 判断是否完成全部排序，跳出循环
            if current_index == [None for i in range(len(sample_name))]:
                break

            ### 普通排序
            # 每一轮排序的最小值
            current_sort_min = list(current_info.items())[0]  # ('a', [1, 2])/('a', [None, 0])
            for i, j in enumerate(current_info.items()):
                # print(j[1][0])
                if current_sort_min[1] == [None, 0] and j[1] != [None, 0]:
                    current_sort_min = j
                if current_sort_min[1] != [None, 0] and j[1] != [None, 0]:
                    if j[1][0] < current_sort_min[1][0]:
                        current_sort_min = j
            current_sort_line[current_sort_min[0]] = current_sort_min[1]  # 将最小值放到正在填充的那行中
            # 开始比较
            for i, j in enumerate(current_info.items()):
                if j[1] != [None, 0]:
                    if j[1][0] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                        current_sort_line[j[0]] = j[1]
                        current_index[i] += 1  # 序号向下走一位
                        if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                            current_index[i] = None

            ### 判断current_sort_line中不为空的后面一个是否在阈值内 更新current_sort_line_replace  current_sort_line
            for i, j in enumerate(current_sort_line.items()):  # j = ('a', [1, 2])
                if j[1] != [None, 0] and current_index[i] != None:
                    # 他的后一个
                    print(current_sort_line)
                    print(current_index)
                    print(self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2])
                    next_info = {j[0]: [self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2], self.dict_nor_or_rel[j[0]].iloc[current_index[i], 3]]}
                    # next_info = {"c":[9,8]}
                    ## 判断下一个是否在范围内
                    if next_info[j[0]][0] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                        current_sort_line_next = copy.deepcopy(current_sort_line)
                        current_sort_line_next[j[0]] = next_info[j[0]]
                        ## 比较current_sort_line_next和current_sort_line的方差
                        if self.help_std(current_sort_line_next) < self.help_std(current_sort_line):
                            # std小，在current_sort_line_replace中换原值，在current_sort_line中替换next,
                            current_sort_line_replace[j[0]] = current_sort_line[j[0]]
                            current_sort_line[j[0]] = next_info[j[0]]
                            current_index[i] += 1  # 序号向下走一位
                            if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                current_index[i] = None

            ### 下一个的数都不在阈值内的，直接更新current_sort_line到self.sort_data_by_MTU
            if current_sort_line_replace == {each_sample: [None, 0] for each_sample in sample_name}:
                temp_dict = {}
                for each in current_sort_line.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
                # 添加完成后将current_sort_line至空，开始新的一行排序
            else:  ### current_sort_line_replace不为空
                # 找到当前current_sort_line的最小值
                current_sort_min = list(current_sort_line.items())[0]  # 有可能是（"a"，[None, 0])
                for i, j in enumerate(current_sort_line.items()):
                    if current_sort_min[1] == [None, 0] and j[1] != [None, 0]:
                        current_sort_min = j
                    if current_sort_min[1] != [None, 0] and j[1] != [None, 0]:
                        if current_sort_min[1][0] > j[1][0]:
                            current_sort_min = j
                # 看之前是空的的后一位在不在新范围内
                for i, j in enumerate(current_sort_line.items()):  # j =（"a"，[None, 0])
                    if j[1] == [None, 0]:
                        if current_index[i] != None:
                            if self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                                current_sort_line[j[0]] = [self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2], self.dict_nor_or_rel[j[0]].iloc[current_index[i], 3]]
                                current_index[i] += 1  # 序号向下走一位
                                if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                    current_index[i] = None
                # 以上将所有能放在current_sort_line 和current_sort_line_replace中的都取出
                # 接下来看看current_sort_line还有哪些可以放到current_sort_line_replace
                for i, j in enumerate(current_sort_line.items()):
                    if j[1] != [None, 0] and current_sort_line_replace[j[0]] == [None, 0]:  # 看看底下的能不能放上面
                        temp_current_sort_line = copy.deepcopy(current_sort_line)
                        temp_current_sort_line_replace = copy.deepcopy(current_sort_line_replace)
                        temp_current_sort_line_replace[j[0]] = temp_current_sort_line[j[0]]
                        temp_current_sort_line[j[0]] = [None, 0]
                        if (self.help_std(temp_current_sort_line) + self.help_std(temp_current_sort_line_replace)) < (self.help_std(current_sort_line) + self.help_std(current_sort_line_replace)):  # 换
                            current_sort_line_replace[j[0]] = current_sort_line[j[0]]
                            current_sort_line[j[0]] = [None, 0]

                # 将current_sort_line和current_sort_line_replace都更新到self.sort_data_by_MTU
                temp_dict = {}
                for each in current_sort_line_replace.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                temp_dict = {}
                for each in current_sort_line.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                # 添加完成后将current_sort_line和current_sort_line_replace至空，开始新的一行排序
                current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
                current_sort_line_replace = {each_sample: [None, 0] for each_sample in sample_name}


        ###  add mean MTU column
        self.sort_data_by_MTU["mean_MTU"] = round(self.sort_data_by_MTU[
                                                      [i for i in self.sort_data_by_MTU.columns.tolist() if
                                                       i.find("Size") != -1]].mean(axis=1), 2)

        print(self.sort_data_by_MTU)
        self.button_sort_data_by_MTU_view.config(state="normal")
        self.button_sort_data_by_MTU_download.config(state="normal")

    def help_min(self, current_info):
        # 每一轮排序的最小值 info = {"a":[1,2],"b":[2,3],"c":[9,8]}
        current_sort_min = list(current_info.items())[0]  # ('a', [1, 2])/('a', [None, 0])
        for i, j in enumerate(current_info.items()):
            # print(j[1][0])
            if current_sort_min[1] == [None, 0] and j[1] != [None, 0]:
                current_sort_min = j
            if current_sort_min[1] != [None, 0] and j[1] != [None, 0]:
                if j[1][0] < current_sort_min[1][0]:
                    current_sort_min = j
        return current_sort_min

    def sort_data_by_MTU3(self):
        # 两次std比较中，二次都比较(std当前行+std上一行)
        # self.sort_ranging  self.dict_nor_or_rel
        sample_name = list(self.dict_nor_or_rel.keys())

        sort_data_columns_name = []
        for temp in sample_name:
            sort_data_columns_name.append(temp + "_Size")
            sort_data_columns_name.append(temp + "_Height")

        self.sort_data_by_MTU = pd.DataFrame(columns=sort_data_columns_name)  # 最终返回结果

        current_index = [0 for i in range(len(sample_name))]  # 每个sample当前排序到的位置
        current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
        current_sort_line_replace = {each_sample: [None, 0] for each_sample in sample_name}  # current_sort_line_before

        while True:
            current_info = {}
            for i, j in enumerate(sample_name):
                if current_index[i] == None:
                    current_info[j] = [None, 0]
                else:
                    current_info[j] = [self.dict_nor_or_rel[j].iloc[current_index[i], 2], self.dict_nor_or_rel[j].iloc[current_index[i], 3]]
            # current_info = {j: [self.dict_nor_or_rel[j].iloc[current_index[i], 2], self.dict_nor_or_rel[j].iloc[current_index[i], 3]] for i, j in enumerate(sample_name)}
            # info = {"a":[1,2],"b":[2,3],"c":[9,8]}
            # 每个sample当前排序到的位置的信息

            # 判断是否完成全部排序，跳出循环
            if current_index == [None for i in range(len(sample_name))]:
                break

            ### 普通排序
            # 每一轮排序的最小值
            current_sort_min = self.help_min(current_info)
            current_sort_line[current_sort_min[0]] = current_sort_min[1]  # 将最小值放到正在填充的那行中
            # 开始比较
            for i, j in enumerate(current_info.items()):
                if j[1] != [None, 0]:
                    if j[1][0] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                        current_sort_line[j[0]] = j[1]
                        current_index[i] += 1  # 序号向下走一位
                        if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                            current_index[i] = None

            ### 判断current_sort_line中不为空的后面一个是否在阈值内 更新current_sort_line_replace  current_sort_line
            for i, j in enumerate(current_sort_line.items()):  # j = ('a', [1, 2])
                if j[1] != [None, 0] and current_index[i] != None:
                    # 他的后一个
                    # print(current_sort_line)
                    # print(current_index)
                    # print(self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2])
                    next_info = {j[0]: [self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2], self.dict_nor_or_rel[j[0]].iloc[current_index[i], 3]]}
                    # next_info = {"c":[9,8]}
                    ## 判断下一个是否在范围内
                    if next_info[j[0]][0] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                        current_sort_line_next = copy.deepcopy(current_sort_line)
                        current_sort_line_next[j[0]] = next_info[j[0]]
                        # print("next_info", next_info)
                        # print(current_sort_line)
                        # print(current_sort_line_next)
                        current_sort_line_replace_next = copy.deepcopy(current_sort_line_replace)
                        current_sort_line_replace_next[j[0]] = current_sort_line[j[0]]
                        # print(current_sort_line_replace)
                        # print(current_sort_line_replace_next)
                        # print("next",self.help_std(current_sort_line_next)+self.help_std(current_sort_line_replace_next))
                        # print(self.help_std(current_sort_line)+self.help_std(current_sort_line_replace))
                        ## 比较current_sort_line_next和current_sort_line的方差
                        if (self.help_std(current_sort_line_next)+self.help_std(current_sort_line_replace_next)) < (self.help_std(current_sort_line)+self.help_std(current_sort_line_replace)):
                            # std小，在current_sort_line_replace中换原值，在current_sort_line中替换next,
                            current_sort_line_replace[j[0]] = current_sort_line[j[0]]
                            current_sort_line[j[0]] = next_info[j[0]]
                            current_index[i] += 1  # 序号向下走一位
                            if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                current_index[i] = None

            ### 下一个的数都不在阈值内的，直接更新current_sort_line到self.sort_data_by_MTU
            if current_sort_line_replace == {each_sample: [None, 0] for each_sample in sample_name}:
                temp_dict = {}
                for each in current_sort_line.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
                # 添加完成后将current_sort_line至空，开始新的一行排序
            else:  ### current_sort_line_replace不为空
                # 找到当前current_sort_line的最小值
                current_sort_min = self.help_min(current_sort_line)
                # 看之前是空的的后一位在不在新范围内
                for i, j in enumerate(current_sort_line.items()):  # j =（"a"，[None, 0])
                    if j[1] == [None, 0]:
                        if current_index[i] != None:
                            if self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                                current_sort_line[j[0]] = [self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2], self.dict_nor_or_rel[j[0]].iloc[current_index[i], 3]]
                                current_index[i] += 1  # 序号向下走一位
                                flag_replace = 1  # 替换
                                if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                    current_index[i] = None
                # 以上将所有能放在current_sort_line 和current_sort_line_replace中的都取出
                # 接下来看看current_sort_line还有哪些可以放到current_sort_line_replace
                for i, j in enumerate(current_sort_line.items()):  # j =（"a"，[None, 0])
                    if j[1] != [None, 0] and current_sort_line_replace[j[0]] == [None, 0]:  # 看看底下的能不能放上面
                        temp_current_sort_line = copy.deepcopy(current_sort_line)
                        temp_current_sort_line_replace = copy.deepcopy(current_sort_line_replace)
                        temp_current_sort_line_replace[j[0]] = temp_current_sort_line[j[0]]
                        temp_current_sort_line[j[0]] = [None, 0]
                        # print(j)
                        # print(current_sort_line_replace)
                        # print(temp_current_sort_line_replace)
                        # print(current_sort_line)
                        # print(temp_current_sort_line)
                        # print("temp",self.help_std(temp_current_sort_line) + self.help_std(temp_current_sort_line_replace))
                        # print(self.help_std(current_sort_line) + self.help_std(current_sort_line_replace))
                        if (self.help_std(temp_current_sort_line) + self.help_std(temp_current_sort_line_replace)) < (self.help_std(current_sort_line) + self.help_std(current_sort_line_replace)):  # 换
                            current_sort_line_replace[j[0]] = current_sort_line[j[0]]
                            current_sort_line[j[0]] = [None, 0]

                # 将current_sort_line和current_sort_line_replace都更新到self.sort_data_by_MTU
                temp_dict = {}
                for each in current_sort_line_replace.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                temp_dict = {}
                for each in current_sort_line.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                # 添加完成后将current_sort_line和current_sort_line_replace至空，开始新的一行排序
                current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
                current_sort_line_replace = {each_sample: [None, 0] for each_sample in sample_name}


        ###  add mean MTU column
        self.sort_data_by_MTU["mean_MTU"] = round(self.sort_data_by_MTU[
                                                      [i for i in self.sort_data_by_MTU.columns.tolist() if
                                                       i.find("Size") != -1]].mean(axis=1), 2)

        # print(self.sort_data_by_MTU)
        self.button_sort_data_by_MTU_view.config(state="normal")
        self.button_sort_data_by_MTU_download.config(state="normal")

    def sort_data_by_MTU4(self):
        # 两次std比较中，两次都次只比较当前行 不合理
        # self.sort_ranging  self.dict_nor_or_rel
        sample_name = list(self.dict_nor_or_rel.keys())

        sort_data_columns_name = []
        for temp in sample_name:
            sort_data_columns_name.append(temp + "_Size")
            sort_data_columns_name.append(temp + "_Height")

        self.sort_data_by_MTU = pd.DataFrame(columns=sort_data_columns_name)  # 最终返回结果

        current_index = [0 for i in range(len(sample_name))]  # 每个sample当前排序到的位置
        current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
        current_sort_line_replace = {each_sample: [None, 0] for each_sample in sample_name}  # current_sort_line_before

        while True:
            current_info = {}
            for i, j in enumerate(sample_name):
                if current_index[i] == None:
                    current_info[j] = [None, 0]
                else:
                    current_info[j] = [self.dict_nor_or_rel[j].iloc[current_index[i], 2], self.dict_nor_or_rel[j].iloc[current_index[i], 3]]
            # current_info = {j: [self.dict_nor_or_rel[j].iloc[current_index[i], 2], self.dict_nor_or_rel[j].iloc[current_index[i], 3]] for i, j in enumerate(sample_name)}
            # info = {"a":[1,2],"b":[2,3],"c":[9,8]}
            # 每个sample当前排序到的位置的信息

            # 判断是否完成全部排序，跳出循环
            if current_index == [None for i in range(len(sample_name))]:
                break

            ### 普通排序
            # 每一轮排序的最小值
            current_sort_min = list(current_info.items())[0]  # ('a', [1, 2])/('a', [None, 0])
            for i, j in enumerate(current_info.items()):
                # print(j[1][0])
                if current_sort_min[1] == [None, 0] and j[1] != [None, 0]:
                    current_sort_min = j
                if current_sort_min[1] != [None, 0] and j[1] != [None, 0]:
                    if j[1][0] < current_sort_min[1][0]:
                        current_sort_min = j
            current_sort_line[current_sort_min[0]] = current_sort_min[1]  # 将最小值放到正在填充的那行中
            # 开始比较
            for i, j in enumerate(current_info.items()):
                if j[1] != [None, 0]:
                    if j[1][0] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                        current_sort_line[j[0]] = j[1]
                        current_index[i] += 1  # 序号向下走一位
                        if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                            current_index[i] = None

            ### 判断current_sort_line中不为空的后面一个是否在阈值内 更新current_sort_line_replace  current_sort_line
            for i, j in enumerate(current_sort_line.items()):  # j = ('a', [1, 2])
                if j[1] != [None, 0] and current_index[i] != None:
                    # 他的后一个
                    print(current_sort_line)
                    print(current_index)
                    print(self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2])
                    next_info = {j[0]: [self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2], self.dict_nor_or_rel[j[0]].iloc[current_index[i], 3]]}
                    # next_info = {"c":[9,8]}
                    ## 判断下一个是否在范围内
                    if next_info[j[0]][0] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                        current_sort_line_next = copy.deepcopy(current_sort_line)
                        current_sort_line_next[j[0]] = next_info[j[0]]
                        ## 比较current_sort_line_next和current_sort_line的方差
                        if self.help_std(current_sort_line_next) < self.help_std(current_sort_line):
                            # std小，在current_sort_line_replace中换原值，在current_sort_line中替换next,
                            current_sort_line_replace[j[0]] = current_sort_line[j[0]]
                            current_sort_line[j[0]] = next_info[j[0]]
                            current_index[i] += 1  # 序号向下走一位
                            if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                current_index[i] = None

            ### 下一个的数都不在阈值内的，直接更新current_sort_line到self.sort_data_by_MTU
            if current_sort_line_replace == {each_sample: [None, 0] for each_sample in sample_name}:
                temp_dict = {}
                for each in current_sort_line.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
                # 添加完成后将current_sort_line至空，开始新的一行排序
            else:  ### current_sort_line_replace不为空
                # 找到当前current_sort_line的最小值
                current_sort_min = list(current_sort_line.items())[0]  # 有可能是（"a"，[None, 0])
                for i, j in enumerate(current_sort_line.items()):
                    if current_sort_min[1] == [None, 0] and j[1] != [None, 0]:
                        current_sort_min = j
                    if current_sort_min[1] != [None, 0] and j[1] != [None, 0]:
                        if current_sort_min[1][0] > j[1][0]:
                            current_sort_min = j
                # 看之前是空的的后一位在不在新范围内
                for i, j in enumerate(current_sort_line.items()):  # j =（"a"，[None, 0])
                    if j[1] == [None, 0]:
                        if current_index[i] != None:
                            if self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                                current_sort_line[j[0]] = [self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2], self.dict_nor_or_rel[j[0]].iloc[current_index[i], 3]]
                                current_index[i] += 1  # 序号向下走一位
                                if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                    current_index[i] = None
                # 以上将所有能放在current_sort_line 和current_sort_line_replace中的都取出
                # 接下来看看current_sort_line还有哪些可以放到current_sort_line_replace
                for i, j in enumerate(current_sort_line.items()):
                    if j[1] != [None, 0] and current_sort_line_replace[j[0]] == [None, 0]:  # 看看底下的能不能放上面
                        temp_current_sort_line = copy.deepcopy(current_sort_line)
                        temp_current_sort_line_replace = copy.deepcopy(current_sort_line_replace)
                        temp_current_sort_line_replace[j[0]] = temp_current_sort_line[j[0]]
                        temp_current_sort_line[j[0]] = [None, 0]
                        if self.help_std(temp_current_sort_line) < self.help_std(current_sort_line):  # 换
                            current_sort_line_replace[j[0]] = current_sort_line[j[0]]
                            current_sort_line[j[0]] = [None, 0]

                # 将current_sort_line和current_sort_line_replace都更新到self.sort_data_by_MTU
                temp_dict = {}
                for each in current_sort_line_replace.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                temp_dict = {}
                for each in current_sort_line.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                # 添加完成后将current_sort_line和current_sort_line_replace至空，开始新的一行排序
                current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
                current_sort_line_replace = {each_sample: [None, 0] for each_sample in sample_name}


        ###  add mean MTU column
        self.sort_data_by_MTU["mean_MTU"] = round(self.sort_data_by_MTU[
                                                      [i for i in self.sort_data_by_MTU.columns.tolist() if
                                                       i.find("Size") != -1]].mean(axis=1), 2)

        print(self.sort_data_by_MTU)
        self.button_sort_data_by_MTU_view.config(state="normal")
        self.button_sort_data_by_MTU_download.config(state="normal")

    def sort_data_by_MTU5(self):
        # 两次std比较中，二次都比较(std当前行+std上一行) 加上循环，判断当前行是否有改变
        # self.sort_ranging  self.dict_nor_or_rel
        sample_name = list(self.dict_nor_or_rel.keys())

        sort_data_columns_name = []
        for temp in sample_name:
            sort_data_columns_name.append(temp + "_Size")
            sort_data_columns_name.append(temp + "_Height")

        self.sort_data_by_MTU = pd.DataFrame(columns=sort_data_columns_name)  # 最终返回结果

        current_index = [0 for i in range(len(sample_name))]  # 每个sample当前排序到的位置
        current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
        current_sort_line_replace = {each_sample: [None, 0] for each_sample in sample_name}  # current_sort_line_before

        while True:
            current_info = {}
            for i, j in enumerate(sample_name):
                if current_index[i] == None:
                    current_info[j] = [None, 0]
                else:
                    current_info[j] = [self.dict_nor_or_rel[j].iloc[current_index[i], 2], self.dict_nor_or_rel[j].iloc[current_index[i], 3]]
            # current_info = {j: [self.dict_nor_or_rel[j].iloc[current_index[i], 2], self.dict_nor_or_rel[j].iloc[current_index[i], 3]] for i, j in enumerate(sample_name)}
            # info = {"a":[1,2],"b":[2,3],"c":[9,8]}
            # 每个sample当前排序到的位置的信息

            # 判断是否完成全部排序，跳出循环
            if current_index == [None for i in range(len(sample_name))]:
                break

            ### 普通排序
            # 每一轮排序的最小值
            current_sort_min = self.help_min(current_info)
            current_sort_line[current_sort_min[0]] = current_sort_min[1]  # 将最小值放到正在填充的那行中
            # 开始比较
            for i, j in enumerate(current_info.items()):
                if j[1] != [None, 0]:
                    if j[1][0] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                        current_sort_line[j[0]] = j[1]
                        current_index[i] += 1  # 序号向下走一位
                        if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                            current_index[i] = None

            ### 判断current_sort_line中不为空的后面一个是否在阈值内 更新current_sort_line_replace  current_sort_line
            flag_next_replace = 1  # 有发生下一个把前一个替换的情况
            while flag_next_replace == 1:
                flag_next_replace = 0
                for i, j in enumerate(current_sort_line.items()):  # j = ('a', [1, 2])
                    if j[1] != [None, 0] and current_index[i] != None:
                        # 他的后一个
                        # print(current_sort_line)
                        # print(current_index)
                        # print(self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2])
                        next_info = {j[0]: [self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2], self.dict_nor_or_rel[j[0]].iloc[current_index[i], 3]]}
                        # next_info = {"c":[9,8]}
                        ## 判断下一个是否在范围内
                        if next_info[j[0]][0] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                            current_sort_line_next = copy.deepcopy(current_sort_line)
                            current_sort_line_next[j[0]] = next_info[j[0]]
                            # print("next_info", next_info)
                            # print(current_sort_line)
                            # print(current_sort_line_next)
                            current_sort_line_replace_next = copy.deepcopy(current_sort_line_replace)
                            current_sort_line_replace_next[j[0]] = current_sort_line[j[0]]
                            # print(current_sort_line_replace)
                            # print(current_sort_line_replace_next)
                            # print("next",self.help_std(current_sort_line_next)+self.help_std(current_sort_line_replace_next))
                            # print(self.help_std(current_sort_line)+self.help_std(current_sort_line_replace))
                            ## 比较current_sort_line_next和current_sort_line的方差
                            if (self.help_std(current_sort_line_next)+self.help_std(current_sort_line_replace_next)) < (self.help_std(current_sort_line)+self.help_std(current_sort_line_replace)):
                                # std小，在current_sort_line_replace中换原值，在current_sort_line中替换next,
                                current_sort_line_replace[j[0]] = current_sort_line[j[0]]
                                current_sort_line[j[0]] = next_info[j[0]]
                                current_index[i] += 1  # 序号向下走一位
                                flag_next_replace = 1  # 有发生下一个把前一个替换的情况
                                current_sort_min = self.help_min(current_sort_line)  # 更新当前行的最小值
                                if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                    current_index[i] = None

            ### 下一个的数都不在阈值内的，直接更新current_sort_line到self.sort_data_by_MTU
            if current_sort_line_replace == {each_sample: [None, 0] for each_sample in sample_name}:
                temp_dict = {}
                for each in current_sort_line.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
                # 添加完成后将current_sort_line至空，开始新的一行排序
            else:  ### current_sort_line_replace不为空
                flag_down_go_up = 1
                while flag_down_go_up == 1:
                    flag_down_go_up = 0
                    #  找到当前current_sort_line的最小值
                    current_sort_min = self.help_min(current_sort_line)
                    # 看之前是空的的后一位在不在新范围内
                    for i, j in enumerate(current_sort_line.items()):  # j =（"a"，[None, 0])
                        if j[1] == [None, 0]:
                            if current_index[i] != None:
                                if self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                                    current_sort_line[j[0]] = [self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2], self.dict_nor_or_rel[j[0]].iloc[current_index[i], 3]]
                                    current_index[i] += 1  # 序号向下走一位
                                    flag_replace = 1  # 替换
                                    if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                        current_index[i] = None
                    # 以上将所有能放在current_sort_line 和current_sort_line_replace中的都取出
                    # 接下来看看current_sort_line还有哪些可以放到current_sort_line_replace
                    for i, j in enumerate(current_sort_line.items()):  # j =（"a"，[None, 0])
                        if j[1] != [None, 0] and current_sort_line_replace[j[0]] == [None, 0]:  # 看看底下的能不能放上面
                            temp_current_sort_line = copy.deepcopy(current_sort_line)
                            temp_current_sort_line_replace = copy.deepcopy(current_sort_line_replace)
                            temp_current_sort_line_replace[j[0]] = temp_current_sort_line[j[0]]
                            temp_current_sort_line[j[0]] = [None, 0]
                            # print(j)
                            # print(current_sort_line_replace)
                            # print(temp_current_sort_line_replace)
                            # print(current_sort_line)
                            # print(temp_current_sort_line)
                            # print("temp",self.help_std(temp_current_sort_line) + self.help_std(temp_current_sort_line_replace))
                            # print(self.help_std(current_sort_line) + self.help_std(current_sort_line_replace))
                            if (self.help_std(temp_current_sort_line) + self.help_std(temp_current_sort_line_replace)) < (self.help_std(current_sort_line) + self.help_std(current_sort_line_replace)):  # 换
                                current_sort_line_replace[j[0]] = current_sort_line[j[0]]
                                current_sort_line[j[0]] = [None, 0]
                                flag_down_go_up = 1

                # 将current_sort_line和current_sort_line_replace都更新到self.sort_data_by_MTU
                temp_dict = {}
                for each in current_sort_line_replace.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                temp_dict = {}
                for each in current_sort_line.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                # 添加完成后将current_sort_line和current_sort_line_replace至空，开始新的一行排序
                current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
                current_sort_line_replace = {each_sample: [None, 0] for each_sample in sample_name}


        ###  add mean MTU column
        self.sort_data_by_MTU["mean_MTU"] = round(self.sort_data_by_MTU[
                                                      [i for i in self.sort_data_by_MTU.columns.tolist() if
                                                       i.find("Size") != -1]].mean(axis=1), 2)

        # print(self.sort_data_by_MTU)
        self.button_sort_data_by_MTU_view.config(state="normal")
        self.button_sort_data_by_MTU_download.config(state="normal")

    def sort_data_by_MTU6(self):
        # 两次std比较中，二次都比较(std当前行+std上一行)  加一个大循环
        # self.sort_ranging  self.dict_nor_or_rel
        sample_name = list(self.dict_nor_or_rel.keys())

        sort_data_columns_name = []
        for temp in sample_name:
            sort_data_columns_name.append(temp + "_Size")
            sort_data_columns_name.append(temp + "_Height")

        self.sort_data_by_MTU = pd.DataFrame(columns=sort_data_columns_name)  # 最终返回结果

        current_index = [0 for i in range(len(sample_name))]  # 每个sample当前排序到的位置
        current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
        current_sort_line_replace = {each_sample: [None, 0] for each_sample in sample_name}  # current_sort_line_before

        while True:
            current_info = {}
            for i, j in enumerate(sample_name):
                if current_index[i] == None:
                    current_info[j] = [None, 0]
                else:
                    current_info[j] = [self.dict_nor_or_rel[j].iloc[current_index[i], 2], self.dict_nor_or_rel[j].iloc[current_index[i], 3]]
            # current_info = {j: [self.dict_nor_or_rel[j].iloc[current_index[i], 2], self.dict_nor_or_rel[j].iloc[current_index[i], 3]] for i, j in enumerate(sample_name)}
            # info = {"a":[1,2],"b":[2,3],"c":[9,8]}
            # 每个sample当前排序到的位置的信息

            # 判断是否完成全部排序，跳出循环
            if current_index == [None for i in range(len(sample_name))]:
                break

            ### 普通排序
            # 每一轮排序的最小值
            current_sort_min = self.help_min(current_info)
            current_sort_line[current_sort_min[0]] = current_sort_min[1]  # 将最小值放到正在填充的那行中
            # 开始比较
            for i, j in enumerate(current_info.items()):
                if j[1] != [None, 0]:
                    if j[1][0] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                        current_sort_line[j[0]] = j[1]
                        current_index[i] += 1  # 序号向下走一位
                        flag_replace = 1  # 替换
                        if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                            current_index[i] = None

            flag_replace = 1  # 有发生下一个把前一个替换的情况
            while flag_replace == 1:
                flag_replace = 0
                ### 判断current_sort_line中不为空的后面一个是否在阈值内 更新current_sort_line_replace  current_sort_line
                for i, j in enumerate(current_sort_line.items()):  # j = ('a', [1, 2])
                    if j[1] != [None, 0] and current_index[i] != None:
                        # 他的后一个
                        # print(current_sort_line)
                        # print(current_index)
                        # print(self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2])
                        next_info = {j[0]: [self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2], self.dict_nor_or_rel[j[0]].iloc[current_index[i], 3]]}
                        # next_info = {"c":[9,8]}
                        ## 判断下一个是否在范围内
                        if next_info[j[0]][0] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                            current_sort_line_next = copy.deepcopy(current_sort_line)
                            current_sort_line_next[j[0]] = next_info[j[0]]
                            # print("next_info", next_info)
                            # print(current_sort_line)
                            # print(current_sort_line_next)
                            current_sort_line_replace_next = copy.deepcopy(current_sort_line_replace)
                            current_sort_line_replace_next[j[0]] = current_sort_line[j[0]]
                            # print(current_sort_line_replace)
                            # print(current_sort_line_replace_next)
                            # print("next",self.help_std(current_sort_line_next)+self.help_std(current_sort_line_replace_next))
                            # print(self.help_std(current_sort_line)+self.help_std(current_sort_line_replace))
                            ## 比较current_sort_line_next和current_sort_line的方差
                            if (self.help_std(current_sort_line_next)+self.help_std(current_sort_line_replace_next)) < (self.help_std(current_sort_line)+self.help_std(current_sort_line_replace)):
                                # std小，在current_sort_line_replace中换原值，在current_sort_line中替换next,
                                current_sort_line_replace[j[0]] = current_sort_line[j[0]]
                                current_sort_line[j[0]] = next_info[j[0]]
                                current_index[i] += 1  # 序号向下走一位
                                flag_replace = 1  # 替换
                                if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                    current_index[i] = None

                ### 下一个的数都不在阈值内的，直接更新current_sort_line到self.sort_data_by_MTU
                if current_sort_line_replace == {each_sample: [None, 0] for each_sample in sample_name}:
                    break

                else:  ### current_sort_line_replace不为空
                    # 找到当前current_sort_line的最小值
                    current_sort_min = self.help_min(current_sort_line)
                    # 看之前是空的的后一位在不在新范围内
                    for i, j in enumerate(current_sort_line.items()):  # j =（"a"，[None, 0])
                        if j[1] == [None, 0]:
                            if current_index[i] != None:
                                if self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                                    current_sort_line[j[0]] = [self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2], self.dict_nor_or_rel[j[0]].iloc[current_index[i], 3]]
                                    current_index[i] += 1  # 序号向下走一位
                                    flag_replace = 1  # 替换
                                    if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                        current_index[i] = None
                    # 以上将所有能放在current_sort_line 和current_sort_line_replace中的都取出
                    # 接下来看看current_sort_line还有哪些可以放到current_sort_line_replace
                    for i, j in enumerate(current_sort_line.items()):  # j =（"a"，[None, 0])
                        if j[1] != [None, 0] and current_sort_line_replace[j[0]] == [None, 0]:  # 看看底下的能不能放上面
                            temp_current_sort_line = copy.deepcopy(current_sort_line)
                            temp_current_sort_line_replace = copy.deepcopy(current_sort_line_replace)
                            temp_current_sort_line_replace[j[0]] = temp_current_sort_line[j[0]]
                            temp_current_sort_line[j[0]] = [None, 0]
                            # print(j)
                            # print(current_sort_line_replace)
                            # print(temp_current_sort_line_replace)
                            # print(current_sort_line)
                            # print(temp_current_sort_line)
                            # print("temp",self.help_std(temp_current_sort_line) + self.help_std(temp_current_sort_line_replace))
                            # print(self.help_std(current_sort_line) + self.help_std(current_sort_line_replace))
                            if (self.help_std(temp_current_sort_line) + self.help_std(temp_current_sort_line_replace)) < (self.help_std(current_sort_line) + self.help_std(current_sort_line_replace)):  # 换
                                current_sort_line_replace[j[0]] = current_sort_line[j[0]]
                                current_sort_line[j[0]] = [None, 0]
                                flag_replace = 1  # 替换

            ##### 以上current_sort_line和current_sort_line_replace都确定好，下来更新到self.sort_data_by_MTU
            ### 下一个的数都不在阈值内的，直接更新current_sort_line到self.sort_data_by_MTU
            if current_sort_line_replace == {each_sample: [None, 0] for each_sample in sample_name}:
                temp_dict = {}
                for each in current_sort_line.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
            else:
                # 将current_sort_line和current_sort_line_replace都更新到self.sort_data_by_MTU
                temp_dict = {}
                for each in current_sort_line_replace.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                temp_dict = {}
                for each in current_sort_line.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                # 添加完成后将current_sort_line和current_sort_line_replace至空，开始新的一行排序
                current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
                current_sort_line_replace = {each_sample: [None, 0] for each_sample in sample_name}


        ###  add mean MTU column
        self.sort_data_by_MTU["mean_MTU"] = round(self.sort_data_by_MTU[
                                                      [i for i in self.sort_data_by_MTU.columns.tolist() if
                                                       i.find("Size") != -1]].mean(axis=1), 2)

        # print(self.sort_data_by_MTU)
        self.button_sort_data_by_MTU_view.config(state="normal")
        self.button_sort_data_by_MTU_download.config(state="normal")

    def sort_data_by_MTU7(self):
        # 普通比较，只看整数位
        # self.sort_ranging  self.dict_nor_or_rel
        sample_name = list(self.dict_nor_or_rel.keys())

        sort_data_columns_name = []
        for temp in sample_name:
            sort_data_columns_name.append(temp + "_Size")
            sort_data_columns_name.append(temp + "_Height")

        self.sort_data_by_MTU = pd.DataFrame(columns=sort_data_columns_name)  # 最终返回结果

        all_dataframes = copy.deepcopy(self.dict_nor_or_rel)
        min_in_sorted = float("inf")
        unsorted_sample = {temp[0]: [temp[1]["Size"].iloc[0], temp[1]["Height"].iloc[0]] for temp in
                           all_dataframes.items()}
        while all_dataframes != {}:
            min_in_sorted = float("inf")
            each_line_sorted = {each_sample: [None, 0] for each_sample in sample_name}  # 大表中排好序的每一行的sample_name
            # ----------------- 本次循环结束 代表大表中每一行排序结束-----------------------
            for each in range(len(sample_name)):
                min_sample = min(unsorted_sample.items(),
                                 key=lambda a: a[1])  # ('dfD07_DS4.fsa': [0.13, 1.4615384615384615]) 找到本轮未排序的最小值
                if min_in_sorted == float("inf"):  # 判断之前是否排序过
                    min_in_sorted = min_sample[1][0]
                    each_line_sorted[min_sample[0]] = min_sample[1]
                    #     print(all_dataframes[min_sample[0]])
                    # ---------把各个DataFrame中添加到each_line_sorted里的行删掉--------
                    all_dataframes[min_sample[0]].drop(index=0, inplace=True)
                    all_dataframes[min_sample[0]] = all_dataframes[min_sample[0]].reset_index(drop=True)
                    # ---------更新未排序的相应的值--------
                    unsorted_sample[min_sample[0]] = [float("inf"), float("inf")]

                else:
                    if self.var_sort_ranging.get() <= 1:
                        # 判断排过序的最小值和未排序的最小值是否相差1以内 threshold<1时，当数据个位不同，重启一行
                        if (min_sample[1][0] - min_in_sorted <= self.var_sort_ranging.get()) and (min_sample[1][0]%10//1 == min_in_sorted%10//1):
                            # min_in_sorted = min_sample[1][0]
                            each_line_sorted[min_sample[0]] = min_sample[1]
                            # ---------把各个DataFrame中添加到each_line_sorted里的行删掉--------
                            all_dataframes[min_sample[0]].drop(0, inplace=True)
                            all_dataframes[min_sample[0]] = all_dataframes[min_sample[0]].reset_index(drop=True)
                            # ---------更新未排序的相应的值--------
                            unsorted_sample[min_sample[0]] = [float("inf"), float("inf")]
                        else:  # 跳出该行排序
                            break
                    else:
                        if min_sample[1][0] - min_in_sorted <= self.var_sort_ranging.get():
                            # min_in_sorted = min_sample[1][0]
                            each_line_sorted[min_sample[0]] = min_sample[1]
                            # ---------把各个DataFrame中添加到each_line_sorted里的行删掉--------
                            all_dataframes[min_sample[0]].drop(0, inplace=True)
                            all_dataframes[min_sample[0]] = all_dataframes[min_sample[0]].reset_index(drop=True)
                            # ---------更新未排序的相应的值--------
                            unsorted_sample[min_sample[0]] = [float("inf"), float("inf")]
                        else:  # 跳出该行排序
                            break

            # ------------ 大表中每一行排序结束  将each_line_sorted更新到大表中  更新unsorted_sample----------
            temp_dict = {}
            for each in each_line_sorted.items():
                temp_dict[each[0] + "_Size"] = each[1][0]
                temp_dict[each[0] + "_Height"] = each[1][1]
            self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)

            delete = []
            for each in unsorted_sample.items():
                if each[1] == [float("inf"), float("inf")]:
                    #             print(len(all_dataframes[each[0]]))
                    #             print(each[0])
                    if len(all_dataframes[each[0]]) == 0:
                        all_dataframes.pop(each[0])
                        delete.append(each[0])
                    else:
                        unsorted_sample[each[0]] = [all_dataframes[each[0]]["Size"].iloc[0],
                                                    all_dataframes[each[0]]["Height"].iloc[0]]
            for each in delete:  # all_dataframes中删除掉的samplename, unsorted_sample中也要删除
                unsorted_sample.pop(each)

        ###  add mean MTU column
        self.sort_data_by_MTU["mean_MTU"] = round(self.sort_data_by_MTU[
                                                      [i for i in self.sort_data_by_MTU.columns.tolist() if
                                                       i.find("Size") != -1]].mean(axis=1), 2)

        self.button_sort_data_by_MTU_view.config(state="normal")
        self.button_sort_data_by_MTU_download.config(state="normal")

    def sort_data_by_MTU8(self):
        # 普通比较用整数位  第一次用std比较 第二次比较和最小值的差 加一个大循环
        # self.sort_ranging  self.dict_nor_or_rel
        sample_name = list(self.dict_nor_or_rel.keys())

        sort_data_columns_name = []
        for temp in sample_name:
            sort_data_columns_name.append(temp + "_Size")
            sort_data_columns_name.append(temp + "_Height")

        self.sort_data_by_MTU = pd.DataFrame(columns=sort_data_columns_name)  # 最终返回结果

        current_index = [0 for i in range(len(sample_name))]  # 每个sample当前排序到的位置
        current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
        current_sort_line_replace = {each_sample: [None, 0] for each_sample in sample_name}  # current_sort_line_before

        while True:
            current_info = {}
            for i, j in enumerate(sample_name):
                if current_index[i] == None:
                    current_info[j] = [None, 0]
                else:
                    current_info[j] = [self.dict_nor_or_rel[j].iloc[current_index[i], 2], self.dict_nor_or_rel[j].iloc[current_index[i], 3]]
            # current_info = {j: [self.dict_nor_or_rel[j].iloc[current_index[i], 2], self.dict_nor_or_rel[j].iloc[current_index[i], 3]] for i, j in enumerate(sample_name)}
            # info = {"a":[1,2],"b":[2,3],"c":[9,8]}
            # 每个sample当前排序到的位置的信息

            # 判断是否完成全部排序，跳出循环
            if current_index == [None for i in range(len(sample_name))]:
                break

            ### 普通排序
            # 每一轮排序的最小值
            current_sort_min = self.help_min(current_info)
            current_sort_line[current_sort_min[0]] = current_sort_min[1]  # 将最小值放到正在填充的那行中
            # 开始比较
            if self.var_sort_ranging.get() <= 1:  # 只看整数位
                for i, j in enumerate(current_info.items()):
                    if j[1] != [None, 0]:
                        if (j[1][0] - current_sort_min[1][0] <= self.var_sort_ranging.get()) and (j[1][0] % 10 // 1 == current_sort_min[1][0]% 10 // 1):
                            current_sort_line[j[0]] = j[1]
                            current_index[i] += 1  # 序号向下走一位
                            if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                current_index[i] = None
            else:
                for i, j in enumerate(current_info.items()):
                    if j[1] != [None, 0]:
                        if j[1][0] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                            current_sort_line[j[0]] = j[1]
                            current_index[i] += 1  # 序号向下走一位
                            if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                current_index[i] = None


            flag_replace = 1  # 有发生下一个把前一个替换的情况
            while flag_replace == 1:
                flag_replace = 0
                ### 判断current_sort_line中不为空的后面一个是否在阈值内 更新current_sort_line_replace  current_sort_line
                for i, j in enumerate(current_sort_line.items()):  # j = ('a', [1, 2])
                    if j[1] != [None, 0] and current_index[i] != None:
                        # 他的后一个
                        next_info = {j[0]: [self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2], self.dict_nor_or_rel[j[0]].iloc[current_index[i], 3]]}
                        # next_info = {"c":[9,8]}
                        ## 判断下一个是否在范围内
                        if next_info[j[0]][0] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                            current_sort_line_next = copy.deepcopy(current_sort_line)
                            current_sort_line_next[j[0]] = next_info[j[0]]
                            current_sort_line_replace_next = copy.deepcopy(current_sort_line_replace)
                            current_sort_line_replace_next[j[0]] = current_sort_line[j[0]]
                            ## 比较current_sort_line_next和current_sort_line的方差
                            if (self.help_std(current_sort_line_next)+self.help_std(current_sort_line_replace_next)) < (self.help_std(current_sort_line)+self.help_std(current_sort_line_replace)):
                                # std小，在current_sort_line_replace中换原值，在current_sort_line中替换next,
                                current_sort_line_replace[j[0]] = current_sort_line[j[0]]
                                current_sort_line[j[0]] = next_info[j[0]]
                                current_index[i] += 1  # 序号向下走一位
                                flag_replace = 1  # 替换
                                if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                    current_index[i] = None

                ### 下一个的数都不在阈值内的，直接更新current_sort_line到self.sort_data_by_MTU
                if current_sort_line_replace == {each_sample: [None, 0] for each_sample in sample_name}:
                    break

                else:  ### current_sort_line_replace不为空
                    # 找到当前current_sort_line的最小值
                    current_sort_min = self.help_min(current_sort_line)
                    # 看之前是空的的后一位在不在新范围内
                    for i, j in enumerate(current_sort_line.items()):  # j =（"a"，[None, 0])
                        if j[1] == [None, 0]:
                            if current_index[i] != None:
                                if self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                                    current_sort_line[j[0]] = [self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2], self.dict_nor_or_rel[j[0]].iloc[current_index[i], 3]]
                                    current_index[i] += 1  # 序号向下走一位
                                    flag_replace = 1  # 替换
                                    if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                        current_index[i] = None
                    # 以上将所有能放在current_sort_line 和current_sort_line_replace中的都取出
                    # 接下来看看current_sort_line还有哪些可以放到current_sort_line_replace    比较时用距离两行都存在的值中的最小值确定
                    # 先找到两行都存在值的最小值
                    double_exist_replace_min = float("inf")
                    double_exist_min = float("inf")
                    for i, j in enumerate(current_sort_line.items()):  # j =（"a"，[None, 0])
                            if j[1] != [None, 0] and current_sort_line_replace[j[0]] != [None, 0]:  # 看看底下的能不能放上面
                                double_exist_replace_min = min(double_exist_replace_min, current_sort_line_replace[j[0]][0])
                                double_exist_min = min(double_exist_min,j[1][0])
                    # print(double_exist_replace_min)
                    # print(double_exist_min)
                    # 再看底下的能不能放上去
                    for i, j in enumerate(current_sort_line.items()):  # j =（"a"，[None, 0])
                        if j[1] != [None, 0] and current_sort_line_replace[j[0]] == [None, 0]:  # 看看底下的能不能放上面
                            if (abs(j[1][0] - double_exist_min)) > (abs(j[1][0] - double_exist_replace_min)):
                                current_sort_line_replace[j[0]] = current_sort_line[j[0]]
                                current_sort_line[j[0]] = [None, 0]
                                flag_replace = 1  # 替换

            ##### 以上current_sort_line和current_sort_line_replace都确定好，下来更新到self.sort_data_by_MTU
            ### 下一个的数都不在阈值内的，直接更新current_sort_line到self.sort_data_by_MTU
            if current_sort_line_replace == {each_sample: [None, 0] for each_sample in sample_name}:
                temp_dict = {}
                for each in current_sort_line.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
            else:
                # 将current_sort_line和current_sort_line_replace都更新到self.sort_data_by_MTU
                temp_dict = {}
                for each in current_sort_line_replace.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                temp_dict = {}
                for each in current_sort_line.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                # 添加完成后将current_sort_line和current_sort_line_replace至空，开始新的一行排序
                current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
                current_sort_line_replace = {each_sample: [None, 0] for each_sample in sample_name}


        ###  add mean MTU column
        self.sort_data_by_MTU["mean_MTU"] = round(self.sort_data_by_MTU[
                                                      [i for i in self.sort_data_by_MTU.columns.tolist() if
                                                       i.find("Size") != -1]].mean(axis=1), 2)

        # print(self.sort_data_by_MTU)
        self.button_sort_data_by_MTU_view.config(state="normal")
        self.button_sort_data_by_MTU_download.config(state="normal")

    def sort_data_by_MTU9(self):
        # 普通比较  第一次用std比较 第二次比较和最小值的差 加一个大循环
        # self.sort_ranging  self.dict_nor_or_rel
        sample_name = list(self.dict_nor_or_rel.keys())

        sort_data_columns_name = []
        for temp in sample_name:
            sort_data_columns_name.append(temp + "_Size")
            sort_data_columns_name.append(temp + "_Height")

        self.sort_data_by_MTU = pd.DataFrame(columns=sort_data_columns_name)  # 最终返回结果

        current_index = [0 for i in range(len(sample_name))]  # 每个sample当前排序到的位置
        current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
        current_sort_line_replace = {each_sample: [None, 0] for each_sample in sample_name}  # current_sort_line_before

        while True:
            current_info = {}
            for i, j in enumerate(sample_name):
                if current_index[i] == None:
                    current_info[j] = [None, 0]
                else:
                    current_info[j] = [self.dict_nor_or_rel[j].iloc[current_index[i], 2], self.dict_nor_or_rel[j].iloc[current_index[i], 3]]
            # current_info = {j: [self.dict_nor_or_rel[j].iloc[current_index[i], 2], self.dict_nor_or_rel[j].iloc[current_index[i], 3]] for i, j in enumerate(sample_name)}
            # info = {"a":[1,2],"b":[2,3],"c":[9,8]}
            # 每个sample当前排序到的位置的信息

            # 判断是否完成全部排序，跳出循环
            if current_index == [None for i in range(len(sample_name))]:
                break

            ### 普通排序
            # 每一轮排序的最小值
            current_sort_min = self.help_min(current_info)
            current_sort_line[current_sort_min[0]] = current_sort_min[1]  # 将最小值放到正在填充的那行中
            print("current_info", current_info)
            print("current_index", current_index)
            # 开始比较
            for i, j in enumerate(current_info.items()):
                if j[1] != [None, 0]:
                    if j[1][0] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                        current_sort_line[j[0]] = j[1]
                        current_index[i] += 1  # 序号向下走一位
                        if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                            current_index[i] = None
            print("current_sort_min", current_sort_min)
            print("current_sort_line", current_sort_line)
            print("current_index", current_index)


            flag_replace = 1  # 有发生下一个把前一个替换的情况
            while flag_replace == 1:
                flag_replace = 0
                ### 判断current_sort_line中不为空的后面一个是否在阈值内 更新current_sort_line_replace  current_sort_line
                print("new")
                print("current_sort_line", current_sort_line)
                for i, j in enumerate(current_sort_line.items()):  # j = ('a', [1, 2])
                    if j[1] != [None, 0] and current_index[i] != None:
                        # 他的后一个
                        next_info = {j[0]: [self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2], self.dict_nor_or_rel[j[0]].iloc[current_index[i], 3]]}
                        # next_info = {"c":[9,8]}
                        ## 判断下一个是否在范围内
                        if next_info[j[0]][0] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                            current_sort_line_next = copy.deepcopy(current_sort_line)
                            current_sort_line_next[j[0]] = next_info[j[0]]
                            current_sort_line_replace_next = copy.deepcopy(current_sort_line_replace)
                            current_sort_line_replace_next[j[0]] = current_sort_line[j[0]]
                            ## 比较current_sort_line_next和current_sort_line的方差
                            if (self.help_std(current_sort_line_next)+self.help_std(current_sort_line_replace_next)) < (self.help_std(current_sort_line)+self.help_std(current_sort_line_replace)):
                                # std小，在current_sort_line_replace中换原值，在current_sort_line中替换next,
                                current_sort_line_replace[j[0]] = current_sort_line[j[0]]
                                current_sort_line[j[0]] = next_info[j[0]]
                                current_index[i] += 1  # 序号向下走一位
                                flag_replace = 1  # 替换
                                if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                    current_index[i] = None
                print("current_sort_line", current_sort_line)
                print("current_sort_line_replace", current_sort_line_replace)
                print("current_index", current_index)

                ### 下一个的数都不在阈值内的，直接更新current_sort_line到self.sort_data_by_MTU
                if current_sort_line_replace == {each_sample: [None, 0] for each_sample in sample_name}:
                    break

                else:  ### current_sort_line_replace不为空
                    # 找到当前current_sort_line的最小值
                    current_sort_min = self.help_min(current_sort_line)
                    # 看之前是空的的后一位在不在新范围内
                    for i, j in enumerate(current_sort_line.items()):  # j =（"a"，[None, 0])
                        if j[1] == [None, 0]:
                            if current_index[i] != None:
                                if self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2] - current_sort_min[1][0] <= self.var_sort_ranging.get():
                                    current_sort_line[j[0]] = [self.dict_nor_or_rel[j[0]].iloc[current_index[i], 2], self.dict_nor_or_rel[j[0]].iloc[current_index[i], 3]]
                                    current_index[i] += 1  # 序号向下走一位
                                    flag_replace = 1  # 替换
                                    if current_index[i] > self.dict_nor_or_rel[j[0]].shape[0] - 1:
                                        current_index[i] = None
                    # 以上将所有能放在current_sort_line 和current_sort_line_replace中的都取出
                    # 接下来看看current_sort_line还有哪些可以放到current_sort_line_replace    比较时用距离两行都存在的值中的最小值确定
                    # 先找到两行都存在值的最小值
                    double_exist_replace_min = float("inf")
                    double_exist_min = float("inf")
                    for i, j in enumerate(current_sort_line.items()):  # j =（"a"，[None, 0])
                            if j[1] != [None, 0] and current_sort_line_replace[j[0]] != [None, 0]:  # 看看底下的能不能放上面
                                double_exist_replace_min = min(double_exist_replace_min, current_sort_line_replace[j[0]][0])
                                double_exist_min = min(double_exist_min,j[1][0])
                    # print(double_exist_replace_min)
                    # print(double_exist_min)
                    # 再看底下的能不能放上去
                    for i, j in enumerate(current_sort_line.items()):  # j =（"a"，[None, 0])
                        if j[1] != [None, 0] and current_sort_line_replace[j[0]] == [None, 0]:  # 看看底下的能不能放上面
                            if (abs(j[1][0] - double_exist_min)) > (abs(j[1][0] - double_exist_replace_min)):
                                current_sort_line_replace[j[0]] = current_sort_line[j[0]]
                                current_sort_line[j[0]] = [None, 0]
                                flag_replace = 1  # 替换
                print("current_sort_line", current_sort_line)
                print("current_sort_line_replace", current_sort_line_replace)
                print("current_index", current_index)

            ##### 以上current_sort_line和current_sort_line_replace都确定好，下来更新到self.sort_data_by_MTU
            ### 下一个的数都不在阈值内的，直接更新current_sort_line到self.sort_data_by_MTU
            if current_sort_line_replace == {each_sample: [None, 0] for each_sample in sample_name}:
                temp_dict = {}
                for each in current_sort_line.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
            else:
                # 将current_sort_line和current_sort_line_replace都更新到self.sort_data_by_MTU
                temp_dict = {}
                for each in current_sort_line_replace.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                temp_dict = {}
                for each in current_sort_line.items():
                    temp_dict[each[0] + "_Size"] = each[1][0]
                    temp_dict[each[0] + "_Height"] = each[1][1]
                self.sort_data_by_MTU = self.sort_data_by_MTU.append(temp_dict, ignore_index=True)
                # 添加完成后将current_sort_line和current_sort_line_replace至空，开始新的一行排序
                current_sort_line = {each_sample: [None, 0] for each_sample in sample_name}
                current_sort_line_replace = {each_sample: [None, 0] for each_sample in sample_name}


        ###  add mean MTU column
        self.sort_data_by_MTU["mean_MTU"] = round(self.sort_data_by_MTU[
                                                      [i for i in self.sort_data_by_MTU.columns.tolist() if
                                                       i.find("Size") != -1]].mean(axis=1), 2)

        # print(self.sort_data_by_MTU)
        self.button_sort_data_by_MTU_view.config(state="normal")
        self.button_sort_data_by_MTU_download.config(state="normal")



    def show_sort_data_by_MTU(self):
        # 首先删除原有表单中的内容
        # if self.treeview_sheet_show_data.get_children() != ():
        #     exit = self.treeview_sheet_show_data.get_children()
        #     for item in exit:
        #         self.treeview_sheet_show_data.delete(item)

        # 先删除原有子组件
        for widget in self.frame_show_data.winfo_children():
            widget.destroy()

        self.treeview_sheet_show_data = ttk.Treeview(self.frame_show_data, height=600,
                                                     show='headings',
                                                     columns=self.sort_data_by_MTU.columns)
        self.scrollbar_y_show_data = ttk.Scrollbar(self.frame_show_data, orient='vertical')
        self.scrollbar_x_show_data = ttk.Scrollbar(self.frame_show_data, orient='horizontal')
        self.scrollbar_y_show_data.pack(fill="y", side="right")
        self.scrollbar_y_show_data.config(command=self.treeview_sheet_show_data.yview)
        self.scrollbar_x_show_data.pack(fill="x", side="bottom")
        self.scrollbar_x_show_data.config(command=self.treeview_sheet_show_data.xview)
        self.treeview_sheet_show_data.config(xscrollcommand=self.scrollbar_x_show_data.set)
        self.treeview_sheet_show_data.config(yscrollcommand=self.scrollbar_y_show_data.set)
        self.treeview_sheet_show_data.pack(fill="both", side="left", padx=5, pady=5, expand=1)

        # 添加
        for i, col in enumerate(self.sort_data_by_MTU.columns):
            self.treeview_sheet_show_data.heading(column="#" + str(i + 1), text=col)
            self.treeview_sheet_show_data.column(i, width=100, anchor='w')

        for index, row in self.sort_data_by_MTU.iterrows():
            temp = []
            for i, j in enumerate(self.sort_data_by_MTU.columns):
                temp.append(row[j])
            self.treeview_sheet_show_data.insert("", "end", values=temp)

    def download_sort_data_by_MTU(self):
        # self.sort_data_by_MTU  dataframe
        filename = tkinter.filedialog.asksaveasfilename()

        if not filename.endswith('.xls'):
            self.sort_data_by_MTU.to_excel(filename + '.xls')
        else:
            self.sort_data_by_MTU.to_excel(filename)

    def drop_height_less_than_1(self):
        # self.sort_data_by_MTU
        drop_flag = [1 for i in range(len(self.sort_data_by_MTU.index))]
        for i in self.sort_data_by_MTU.index.tolist():  # every row
            for j in self.sort_data_by_MTU.columns.tolist():  # every column
                if j.find("Height") != -1 and self.sort_data_by_MTU.loc[i, j] >= self.var_drop_threshold.get():
                    drop_flag[i] = 0
                    break

        drop_index = [i for i in range(len(drop_flag)) if drop_flag[i] == 1]
        self.sort_data_by_MTU_dropt = self.sort_data_by_MTU.drop(drop_index)

        # 删除size列
        drop_columns = [i for i in self.sort_data_by_MTU.columns.tolist() if i.find("Size") != -1]
        self.sort_data_by_MTU_dropt.drop(columns=drop_columns, inplace=True)
        self.sort_data_by_MTU_dropt.reset_index(inplace=True, drop=True)
        print(self.sort_data_by_MTU_dropt)

        self.button_drop_height_less_than_1_view.config(state="normal")
        self.button_drop_height_less_than_1_download.config(state="normal")

    def show_drop_height_less_than_1(self):
        # 首先删除原有表单中的内容
        # if self.treeview_sheet_show_data.get_children() != ():
        #     exit = self.treeview_sheet_show_data.get_children()
        #     for item in exit:
        #         self.treeview_sheet_show_data.delete(item)

        # 先删除原有子组件
        for widget in self.frame_show_data.winfo_children():
            widget.destroy()

        self.treeview_sheet_show_data = ttk.Treeview(self.frame_show_data, height=600,
                                                     show='headings',
                                                     columns=self.sort_data_by_MTU_dropt.columns)
        self.scrollbar_y_show_data = ttk.Scrollbar(self.frame_show_data, orient='vertical')
        self.scrollbar_x_show_data = ttk.Scrollbar(self.frame_show_data, orient='horizontal')
        self.scrollbar_y_show_data.pack(fill="y", side="right")
        self.scrollbar_y_show_data.config(command=self.treeview_sheet_show_data.yview)
        self.scrollbar_x_show_data.pack(fill="x", side="bottom")
        self.scrollbar_x_show_data.config(command=self.treeview_sheet_show_data.xview)
        self.treeview_sheet_show_data.config(xscrollcommand=self.scrollbar_x_show_data.set)
        self.treeview_sheet_show_data.config(yscrollcommand=self.scrollbar_y_show_data.set)
        self.treeview_sheet_show_data.pack(fill="both", side="left", padx=5, pady=5, expand=1)

        # 添加
        for i, col in enumerate(self.sort_data_by_MTU_dropt.columns):
            self.treeview_sheet_show_data.heading(column="#" + str(i + 1), text=col)
            self.treeview_sheet_show_data.column(i, width=100, anchor='w')

        for index, row in self.sort_data_by_MTU_dropt.iterrows():
            temp = []
            for i, j in enumerate(self.sort_data_by_MTU_dropt.columns):
                temp.append(row[j])
            self.treeview_sheet_show_data.insert("", "end", values=temp)

    def download_drop_height_less_than_1(self):
        # self.sort_data_by_MTU_dropt  dataframe
        filename = tkinter.filedialog.asksaveasfilename()

        if not filename.endswith('.xls'):
            self.sort_data_by_MTU_dropt.to_excel(filename + '.xls')
        else:
            self.sort_data_by_MTU_dropt.to_excel(filename)

    def annotate(self):
        # self.dict_all_glycans_in_database_update  self.var_diff_annotate.get()  self.sort_data_by_MTU_dropt:dataframe

        ### 删除 self.dict_all_glycans_in_database_update中值为np.nan的数据
        print(self.dict_all_glycans_in_database_update)
        self.dict_all_glycans_in_database_update_temp = {}
        for each in self.dict_all_glycans_in_database_update.items():
            if each[1] is not None:
                self.dict_all_glycans_in_database_update_temp[each[0]] = each[1]
        print(self.dict_all_glycans_in_database_update_temp)

        ### 将self.dict_all_glycans_in_database_update 按照MTU大小排序
        self.all_glycans_in_database_update = sorted(self.dict_all_glycans_in_database_update_temp.items(),
                                                     key=lambda x: x[1])
        # print(self.all_glycans_in_database_update)  [('test3', 1.34), ('test1', 8.98)...]

        ### annotate
        # 创建最后保存结果的dataframe
        self.annotated_result = copy.deepcopy(self.sort_data_by_MTU_dropt)
        self.annotated_result['annotate'] = ''

        print('-----------------------------------------------------')

        ### 已self.all_glycans_in_database_update为基准  会出现一个MTU标注了几个glycan_name的情况
        for i, j in enumerate(self.all_glycans_in_database_update):
            diff = float('inf')
            temp_glycan = None
            temp_index = None
            for index, row in self.annotated_result.iterrows():
                print('index', index)
                print(row['mean_MTU'])
                if abs(j[1] - row['mean_MTU']) <= self.var_diff_annotate.get():
                    if diff > abs(j[1] - row['mean_MTU']):
                        diff = abs(j[1] - row['mean_MTU'])
                        temp_glycan = j[0]
                        temp_index = index
                        print(temp_glycan)
                if abs(j[1] - row['mean_MTU']) > self.var_diff_annotate.get() and j[1] < row['mean_MTU']:
                    # 数据库后面的只会和当前mean_MTU相差越来越大  直接跳出数据库循环比较下一个mean_MTU即可
                    break

            # if temp_glycan != None:  # 会出现一个MTU标注了几个glycan_name的情况
            #     print("change", temp_glycan)
            #     # row['annotate'] = temp_glycan
            #     print(self.annotated_result.iloc[temp_index, -1])
            #     # self.annotated_result.iloc[temp_index, -1] = temp_glycan
            #     if self.annotated_result.iloc[temp_index, -1] != "":
            #         self.annotated_result.iloc[temp_index, -1] = self.annotated_result.iloc[temp_index, -1] + '|' + temp_glycan
            #     else:
            #         self.annotated_result.iloc[temp_index, -1] = temp_glycan
            #     print(self.annotated_result.iloc[temp_index])

            if temp_glycan != None:  # 不会出现一个MTU标注了几个glycan_name的情况
                print("change", temp_glycan)
                # row['annotate'] = temp_glycan
                print(self.annotated_result.iloc[temp_index, -1])
                # self.annotated_result.iloc[temp_index, -1] = temp_glycan
                if self.annotated_result.iloc[temp_index, -1] != "":  # 比较一下之前一个的标注和本次标注距mean_MTU之差，留下较小的标注
                    last_annotation = self.annotated_result.iloc[temp_index, -1]  # str
                    update_MTU_of_last_annotation = self.dict_all_glycans_in_database_update[last_annotation]
                    update_MTU_of_this_annotation = self.dict_all_glycans_in_database_update[temp_glycan]
                    if abs(update_MTU_of_this_annotation - self.annotated_result.iloc[temp_index, -2]) < abs(
                            update_MTU_of_last_annotation - self.annotated_result.iloc[temp_index, -2]):
                        self.annotated_result.iloc[temp_index, -1] = temp_glycan
                else:
                    self.annotated_result.iloc[temp_index, -1] = temp_glycan
                print(self.annotated_result.iloc[temp_index])
        """

        ### 已self.annotated_result为基准，每个和self.all_glycans_in_database_update中的比较  会出现几个MTU标注同一个glycan_name的情况
        for index, row in self.annotated_result.iterrows():
            print(row)
            diff = float('inf')
            temp_glycan = None
            temp_index = None
            for i, j in enumerate(self.all_glycans_in_database_update):
                # print('index', index)
                # print(row['mean_MTU'])
                if abs(j[1] - row['mean_MTU']) <= self.var_diff_annotate.get():
                    if diff > abs(j[1] - row['mean_MTU']):
                        diff = abs(j[1] - row['mean_MTU'])
                        temp_glycan = j[0]
                        temp_index = index
                        # print(temp_glycan)
                if abs(j[1] - row['mean_MTU']) > self.var_diff_annotate.get() and j[1] > row['mean_MTU']:
                    # 数据库后面的只会和当前mean_MTU相差越来越大  直接跳出数据库循环比较下一个mean_MTU即可
                    break
            if temp_glycan != None:
                print("change", temp_glycan)
                # row['annotate'] = temp_glycan
                print(self.annotated_result.iloc[temp_index, -1])
                self.annotated_result.iloc[temp_index, -1] = temp_glycan
                # self.annotated_result.iloc[temp_index, -1] = self.annotated_result.iloc[
                #                                                  temp_index, -1] + ' ' + temp_glycan
                # print(self.annotated_result.iloc[temp_index])
        """

        print(self.annotated_result)
        self.button_annotate_download.config(state="normal")
        self.button_annotate_view.config(state="normal")

    def show_annotate(self):
        # 首先删除原有表单中的内容
        # if self.treeview_sheet_show_data.get_children() != ():
        #     exit = self.treeview_sheet_show_data.get_children()
        #     for item in exit:
        #         self.treeview_sheet_show_data.delete(item)

        # 先删除原有子组件
        for widget in self.frame_show_data.winfo_children():
            widget.destroy()

        self.treeview_sheet_show_data = ttk.Treeview(self.frame_show_data, height=600,
                                                     show='headings',
                                                     columns=self.annotated_result.columns)
        self.scrollbar_y_show_data = ttk.Scrollbar(self.frame_show_data, orient='vertical')
        self.scrollbar_x_show_data = ttk.Scrollbar(self.frame_show_data, orient='horizontal')
        self.scrollbar_y_show_data.pack(fill="y", side="right")
        self.scrollbar_y_show_data.config(command=self.treeview_sheet_show_data.yview)
        self.scrollbar_x_show_data.pack(fill="x", side="bottom")
        self.scrollbar_x_show_data.config(command=self.treeview_sheet_show_data.xview)
        self.treeview_sheet_show_data.config(xscrollcommand=self.scrollbar_x_show_data.set)
        self.treeview_sheet_show_data.config(yscrollcommand=self.scrollbar_y_show_data.set)
        self.treeview_sheet_show_data.pack(fill="both", side="left", padx=5, pady=5, expand=1)
        # 用户更改annotation
        self.treeview_sheet_show_data.bind('<Double-Button-1>', self.edit_annotation)  # 双击左键进入编辑

        # 添加
        for i, col in enumerate(self.annotated_result.columns):
            self.treeview_sheet_show_data.heading(column="#" + str(i + 1), text=col)
            self.treeview_sheet_show_data.column(i, width=100, anchor='w')

        for index, row in self.annotated_result.iterrows():
            temp = []
            for i, j in enumerate(self.annotated_result.columns):
                temp.append(row[j])
            self.treeview_sheet_show_data.insert("", "end", values=temp)

    def edit_annotation(self, event):
        self.button_annotate_edit_save.config(state="normal")

        for item in self.treeview_sheet_show_data.selection():
            # item = I001
            item_text = self.treeview_sheet_show_data.item(item, "values")
            print(item_text[-1])  # 输出所选行的值
        # self.edit_annotation_column = self.treeview_sheet_show_data.identify_column(event.x)  # 列
        self.edit_annotation_row = self.treeview_sheet_show_data.identify_row(event.y)  # 行
        print(self.edit_annotation_row)

    def annotate_edit_save(self):
        # 获取更新的annotation
        new_annotation = self.entry_annotate_edit.get()
        print(new_annotation)

        # 在dataframe中更改
        # row = int(self.edit_annotation_row[1:]) - 1
        row = int(self.edit_annotation_row[1:], 16) - 1  # I00F
        print(row)
        self.annotated_result.iloc[row, -1] = new_annotation
        print(self.annotated_result)

        # 重新show annotation
        self.show_annotate()

    def download_annotate(self):
        filename = tkinter.filedialog.asksaveasfilename()

        if not filename.endswith('.xls'):
            self.annotated_result.to_excel(filename + '.xls')
        else:
            self.annotated_result.to_excel(filename)

    def creatWidge(self):
        """对应于GUI2中的self.frame_analysed_data = ttk.Frame(self.tab)"""
        self.frame_main = ttk.Frame(self, height=640, width=1020)
        self.frame_main.pack(fill="both", expand=True)
        self.frame_main.pack_propagate(0)

        self.frame_process = ttk.Frame(self.frame_main, width=200)  # 主界面左
        # , relief="ridge"
        # self.frame_process.pack_propagate(0)
        self.frame_process.pack(side="left", fill="y")
        self.canvas_process = tk.Canvas(self.frame_process, width=200, height=640, scrollregion=(0, 0, 1050, 1050))
        self.scrollbar_process = tk.Scrollbar(self.frame_process)
        self.scrollbar_process.pack(side="right", fill="y", pady=5, padx=5)
        self.scrollbar_process.config(command=self.canvas_process.yview)
        self.canvas_process.config(width=200, height=640)
        self.canvas_process.config(yscrollcommand=self.scrollbar_process.set)
        self.canvas_process.pack(side="left", expand=True, fill="both")
        # self.canvas_process.bind("<MouseWheel>", self.canvas_process_mousewheel)

        self.frame_show_data = tk.Frame(self.frame_main, relief="ridge", width=800)  # 主界面右
        self.frame_show_data.pack_propagate(0)
        self.frame_show_data.pack(side="right", fill="both")

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        self.frame_canvas_process = ttk.Frame(self.canvas_process, relief="ridge")  # relief="ridge"
        self.canvas_process.create_window((10, 10), window=self.frame_canvas_process, anchor="nw")
        self.frame_canvas_process.bind("<Enter>", self.bound_to_canvas_process_mousewheel)
        self.frame_canvas_process.bind("<Leave>", self.unbound_to_canvas_process_mousewheel)

        # --------------------------------------------------------------------------------------------------------------

        self.button_raw_data_get = ttk.Button(self.frame_canvas_process, text="get raw data", command=self.get_raw_data)
        self.button_raw_data_get.pack(padx=3, pady=5, anchor="w")
        self.button_raw_data_view = ttk.Button(self.frame_canvas_process, text="view", state="disabled",
                                               command=self.show_raw_data)
        self.button_raw_data_view.pack(padx=3, pady=5, anchor="w")
        self.button_raw_data_download = ttk.Button(self.frame_canvas_process, text="download", state="disabled",
                                                   command=self.download_raw_data)
        self.button_raw_data_download.pack(padx=3, pady=5, anchor="w")

        ttk.Separator(self.frame_canvas_process).pack(fill="x", pady=5)

        # --------------------------------------------------------------------------------------------------------------

        self.button_selected_data_get = ttk.Button(self.frame_canvas_process, text="get selected data",
                                                   command=self.get_selected_data)
        self.button_selected_data_get.pack(padx=3, pady=5, anchor="w")
        self.button_selected_data_view = ttk.Button(self.frame_canvas_process, text="view", state="disabled",
                                                    command=self.show_selected_data)
        self.button_selected_data_view.pack(padx=3, pady=5, anchor="w")
        self.button_selected_data_download = ttk.Button(self.frame_canvas_process, text="download", state="disabled",
                                                        command=self.download_selected_data)
        self.button_selected_data_download.pack(padx=3, pady=5, anchor="w")

        ttk.Separator(self.frame_canvas_process).pack(fill="x", pady=5)

        # --------------------------------------------------------------------------------------------------------------

        self.button_update_database = ttk.Button(self.frame_canvas_process, text="update database",
                                                 command=self.update_database)
        self.button_update_database.pack(padx=3, pady=5, anchor="w")
        self.button_update_database_view = ttk.Button(self.frame_canvas_process, text="view",
                                                      command=self.show_update_database, state="disabled")
        self.button_update_database_view.pack(padx=3, pady=5, anchor="w")
        self.button_update_database_download = ttk.Button(self.frame_canvas_process, text="download", state="disabled",
                                                          command=self.download_update_database)
        self.button_update_database_download.pack(padx=3, pady=5, anchor="w")

        ttk.Separator(self.frame_canvas_process).pack(fill="x", pady=5)

        # --------------------------------------------------------------------------------------------------------------

        self.button_nor_or_rel = ttk.Button(self.frame_canvas_process, text="Normal or Rel",
                                            command=self.analysis_of_nor_or_rel)
        self.button_nor_or_rel.pack(padx=3, pady=5, anchor="w")
        self.button_nor_or_rel_view = ttk.Button(self.frame_canvas_process, text="view", state="disabled",
                                                 command=self.show_nor_or_rel)
        self.button_nor_or_rel_view.pack(padx=3, pady=5, anchor="w")
        self.button_nor_or_rel_download = ttk.Button(self.frame_canvas_process, text="download", state="disabled",
                                                     command=self.download_nor_or_rel)
        self.button_nor_or_rel_download.pack(padx=3, pady=5, anchor="w")

        ttk.Separator(self.frame_canvas_process).pack(fill="x", pady=5)

        # --------------------------------------------------------------------------------------------------------------
        self.frame_choose_sort_ranging = ttk.Frame(self.frame_canvas_process)
        self.frame_choose_sort_ranging.pack(fill="x", padx=5)
        self.var_sort_ranging = tk.DoubleVar()
        self.var_sort_ranging.set(1.00)
        self.scale_sort_ranging = ttk.Scale(self.frame_choose_sort_ranging, from_=0, to=5,
                                            variable=self.var_sort_ranging,
                                            command=lambda v: self.var_sort_ranging.set(round(float(v), 1)))
        self.scale_sort_ranging.pack(side="left")
        self.label_show_sort_ranging = ttk.Label(self.frame_choose_sort_ranging, state="readonly",
                                                 textvariable=self.var_sort_ranging)
        self.label_show_sort_ranging.pack(side="left", padx=5)

        self.button_sort_data_by_MTU = ttk.Button(self.frame_canvas_process, text="sort data by MTU",
                                                  command=self.sort_data_by_MTU9)
        self.button_sort_data_by_MTU.pack(padx=3, pady=5, anchor="w")
        self.button_sort_data_by_MTU_view = ttk.Button(self.frame_canvas_process, text="view", state="disabled",
                                                       command=self.show_sort_data_by_MTU)
        self.button_sort_data_by_MTU_view.pack(padx=3, pady=5, anchor="w")
        self.button_sort_data_by_MTU_download = ttk.Button(self.frame_canvas_process, text="download",
                                                           state="disabled", command=self.download_sort_data_by_MTU)
        self.button_sort_data_by_MTU_download.pack(padx=3, pady=5, anchor="w")

        ttk.Separator(self.frame_canvas_process).pack(fill="x", pady=5)

        # --------------------------------------------------------------------------------------------------------------

        self.frame_choose_drop_threshold = ttk.Frame(self.frame_canvas_process)
        self.frame_choose_drop_threshold.pack(fill="x", padx=5)
        self.var_drop_threshold = tk.DoubleVar()
        self.var_drop_threshold.set(1.00)
        self.scale_drop_threshold = ttk.Scale(self.frame_choose_drop_threshold, from_=0, to=5,
                                              variable=self.var_drop_threshold,
                                              command=lambda v: self.var_drop_threshold.set(round(float(v), 1)))
        self.scale_drop_threshold.pack(side="left")
        self.label_show_drop_threshold = ttk.Label(self.frame_choose_drop_threshold, state="readonly",
                                                   textvariable=self.var_drop_threshold)
        self.label_show_drop_threshold.pack(side="left", padx=5)

        self.button_drop_height_less_than_1 = ttk.Button(self.frame_canvas_process, text="drop small height",
                                                         command=self.drop_height_less_than_1)
        self.button_drop_height_less_than_1.pack(padx=3, pady=5, anchor="w")
        self.button_drop_height_less_than_1_view = ttk.Button(self.frame_canvas_process, text="view",
                                                              state="disabled",
                                                              command=self.show_drop_height_less_than_1)
        self.button_drop_height_less_than_1_view.pack(padx=3, pady=5, anchor="w")
        self.button_drop_height_less_than_1_download = ttk.Button(self.frame_canvas_process, text="download",
                                                                  state="disabled",
                                                                  command=self.download_drop_height_less_than_1)
        self.button_drop_height_less_than_1_download.pack(padx=3, pady=5, anchor="w")

        ttk.Separator(self.frame_canvas_process).pack(fill="x", pady=5)

        # --------------------------------------------------------------------------------------------------------------

        self.frame_choose_diff_annotate = ttk.Frame(self.frame_canvas_process)
        self.frame_choose_diff_annotate.pack(fill="x", padx=5)
        self.var_diff_annotate = tk.DoubleVar()
        self.var_diff_annotate.set(1.00)
        self.scale_diff_annotate = ttk.Scale(self.frame_choose_diff_annotate, from_=0, to=5,
                                             variable=self.var_diff_annotate,
                                             command=lambda v: self.var_diff_annotate.set(round(float(v), 1)))
        self.scale_diff_annotate.pack(side="left")
        self.label_show_diff_annotate = ttk.Label(self.frame_choose_diff_annotate, state="readonly",
                                                  textvariable=self.var_diff_annotate)
        self.label_show_diff_annotate.pack(side="left", padx=5)

        self.button_annotate = ttk.Button(self.frame_canvas_process, text="annotate",
                                          command=self.annotate)
        self.button_annotate.pack(padx=3, pady=5, anchor="w")

        self.button_annotate_view = ttk.Button(self.frame_canvas_process, text="view",
                                               state="disabled",
                                               command=self.show_annotate)
        self.button_annotate_view.pack(padx=3, pady=5, anchor="w")

        self.label_annotate_edit = ttk.Label(self.frame_canvas_process, text="Double click", font=5)
        self.label_annotate_edit.pack(padx=3, pady=5, anchor="w")

        self.var_entry_annotate_edit = tk.StringVar()
        self.entry_annotate_edit = ttk.Entry(self.frame_canvas_process, textvariable=self.var_entry_annotate_edit,
                                             width=10)
        self.entry_annotate_edit.pack(padx=3, pady=5, anchor="w")

        self.button_annotate_edit_save = ttk.Button(self.frame_canvas_process, text="save", state="disabled",
                                                    command=self.annotate_edit_save)
        self.button_annotate_edit_save.pack(padx=3, pady=5, anchor="w")

        self.button_annotate_download = ttk.Button(self.frame_canvas_process, text="download",
                                                   state="disabled", command=self.download_annotate)
        self.button_annotate_download.pack(padx=3, pady=5, anchor="w")


if __name__ == "__main__":
    root = tk.Tk()  # 创建跟窗口对象
    root.geometry("1200x740+100+100")
    root.title("Frame_AnalysedData")
    database = FrameAnalysedData(master=root)  # the object of the class Database
    root.mainloop()
