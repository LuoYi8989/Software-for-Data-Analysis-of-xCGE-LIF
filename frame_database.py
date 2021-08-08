# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import tkinter.scrolledtext
import tkinter.messagebox
import pandas as pd
import numpy as np
import time
from database import Database
import datetime


class FrameDatabase(ttk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.ANALYSIS_OPTIONS = ["GSL", "N glycans", "GAGs"]
        self.var_analysis_option = tk.StringVar()

    def get_which_database(self, *args):
        self.database = Database()
        self.dataframe_database = self.database.create_dataframe_from_csv(self.combobox_which_database.get())

    def show_all(self):
        """show_all中的组件"""
        # 先删除原有子组件
        for widget in self.frame_show_database.winfo_children():
            widget.destroy()

        # remainder
        try:
            self.dataframe_database
        except:
            tkinter.messagebox.showinfo(title="warning", message="Please select the type of database")
            return

        self.scrollbar_database_sheet = ttk.Scrollbar(self.frame_show_database, orient='vertical')
        self.treeview_sheet = ttk.Treeview(self.frame_show_database, height=len(self.dataframe_database),
                                           columns=self.dataframe_database.columns, selectmode='extended',
                                           show='headings',
                                           yscrollcomman=self.scrollbar_database_sheet.set)
        # self.treeview_sheet.grid(row=0, column=0)
        self.treeview_sheet.pack(fill="both", side="left", padx=20, pady=3)
        # self.scrollbar_database_sheet.grid(row=0, column=1, sticky='ns')
        self.scrollbar_database_sheet.pack(fill="y", side="right", padx=3, pady=3)
        self.scrollbar_database_sheet.config(command=self.treeview_sheet.yview)

        for i, col in enumerate(self.dataframe_database.columns):
            self.treeview_sheet.heading(column="#" + str(i + 1), text=col)
            self.treeview_sheet.column(i, width=150, anchor='w')

        for index, row in self.dataframe_database.iterrows():
            temp = []
            for i, j in enumerate(self.dataframe_database.columns):
                temp.append(row[j])
            self.treeview_sheet.insert("", "end", values=temp)

    def version(self):
        # 先删除原有子组件
        for widget in self.frame_show_database.winfo_children():
            widget.destroy()

        # remainder
        try:
            self.dataframe_database
        except:
            tkinter.messagebox.showinfo(title="warning", message="Please select the type of database")
            return

        ### 获取所有的version
        self.all_database_version = self.dataframe_database.sort_values(by="date").loc[:, "date"].unique().tolist()
        print(self.all_database_version)
        print(type(self.all_database_version[0]))  # <class 'datetime.date'>
        self.dict_database_version = {}  # 存储所有version的dict {year1:[date], year2:[date]}
        for each in self.all_database_version:  # -->int
            if each.year not in self.dict_database_version.keys():
                self.dict_database_version[each.year] = []
                self.dict_database_version[each.year].append(each)
            else:
                self.dict_database_version[each.year].append(each)
        print(self.dict_database_version)

        ### 让用户选择database的version
        self.frame_choose_database_version = ttk.Frame(self.frame_show_database)
        self.frame_choose_database_version.pack(padx=5, pady=5)

        self.label_choose_database_version = ttk.Label(self.frame_choose_database_version,
                                                       text="choose the version of database:")
        self.label_choose_database_version.pack(side="left", padx=5, pady=5, anchor="e")
        self.var_database_version_year = tk.IntVar()
        self.combobox_choose_database_version_year = ttk.Combobox(self.frame_choose_database_version, state="readonly",
                                                                  textvariable=self.var_database_version_year, width=8)
        self.combobox_choose_database_version_year["values"] = list(self.dict_database_version.keys())
        self.combobox_choose_database_version_year.set(list(self.dict_database_version.keys())[0])
        self.combobox_choose_database_version_year.pack(side="left", padx=5)
        self.combobox_choose_database_version_year.bind("<<ComboboxSelected>>", self.choose_database_version)
        self.var_database_version = tk.StringVar()  # 更精确的时间  eg:datetime.date(2019, 3, 15)
        self.combobox_choose_database_version = ttk.Combobox(self.frame_choose_database_version, state="disabled",
                                                             textvariable=self.var_database_version, width=12)
        # self.combobox_choose_database_version["values"] = self.all_database_version
        self.combobox_choose_database_version.pack(side="left", padx=5)
        self.combobox_choose_database_version.bind("<<ComboboxSelected>>", self.show_database_version)

        ### Layout of 显示数据
        self.frame_show_database_version = ttk.Frame(self.frame_show_database)
        self.frame_show_database_version.pack(padx=5, pady=5, fill="both")
        self.scrollbar_database_version = ttk.Scrollbar(self.frame_show_database_version, orient='vertical')
        self.treeview_sheet_database_version = ttk.Treeview(self.frame_show_database_version,
                                                            columns=self.dataframe_database.columns,
                                                            selectmode='extended',
                                                            show='headings',
                                                            yscrollcomman=self.scrollbar_database_version.set)
        # extend表示可以选中多行
        self.treeview_sheet_database_version.pack(fill="both", side="left", padx=3, pady=5)
        self.scrollbar_database_version.pack(fill="y", side="right", padx=3, pady=5)
        self.scrollbar_database_version.config(command=self.treeview_sheet_database_version.yview)

    def choose_database_version(self, *args):
        """database version的年份选择后，显示更详细的时间"""
        print(self.var_database_version_year.get())

        datelist = self.dict_database_version[self.var_database_version_year.get()]
        self.combobox_choose_database_version.config(state="readonly")
        self.combobox_choose_database_version["values"] = datelist

    def show_database_version(self, *args):
        print(self.var_database_version.get())
        # datetime.date(*map(int, self.var_database_version.get().split('/')))  将str表示成date形式

        ### 根据用户所选的version给所有glycan建立相应的dataframe
        # 建立一个空的dataframe存放结果
        self.dataframe_of_chossen_version_database = pd.DataFrame(columns=self.dataframe_database.columns)
        print(self.dataframe_of_chossen_version_database)

        # 获取所有glycan_name
        all_glycan_name = self.dataframe_database.loc[:, "name_of_glycan"].unique().tolist()

        # 找出所有self.dataframe_database中相应日期的添加到self.dataframe_of_chossen_version_database中
        index = self.dataframe_database[self.dataframe_database["date"] == datetime.date(
            *map(int, self.var_database_version.get().split('-')))].index.tolist()

        for each in index:
            print(self.dataframe_database.iloc[each, :])
            self.dataframe_of_chossen_version_database = self.dataframe_of_chossen_version_database.append(
                self.dataframe_database.iloc[each, :], ignore_index=True)
            all_glycan_name.remove(self.dataframe_database.iloc[each, 0])  # 将添加过的glycan剔除
        print(self.dataframe_of_chossen_version_database)
        print(all_glycan_name)

        # 对于all_glycan_name中其他的glycan添加空值
        for each in all_glycan_name:
            temp = {"name_of_glycan": each, "MTU": None,
                    "date": datetime.date(*map(int, self.var_database_version.get().split('-'))), "flag": None}
            self.dataframe_of_chossen_version_database = self.dataframe_of_chossen_version_database.append(temp,
                                                                                                           ignore_index=True)
        self.dataframe_of_chossen_version_database.sort_values(by=["MTU", "name_of_glycan"], ignore_index=True,
                                                               inplace=True)
        print(self.dataframe_of_chossen_version_database)

        ### 显示结果
        # 首先删除原有表单中的内容
        if self.treeview_sheet_database_version.get_children() != ():
            exit = self.treeview_sheet_database_version.get_children()
            for item in exit:
                self.treeview_sheet_database_version.delete(item)

        # 向表单中添加数据
        for i, col in enumerate(self.dataframe_of_chossen_version_database.columns):
            self.treeview_sheet_database_version.heading(column="#" + str(i + 1), text=col)
            self.treeview_sheet_database_version.column(i, width=150, anchor='w')

        for index, row in self.dataframe_of_chossen_version_database.iterrows():
            temp = []
            for i, j in enumerate(self.dataframe_of_chossen_version_database.columns):
                temp.append(row[j])
            self.treeview_sheet_database_version.insert("", "end", values=temp)

    def search(self):
        """search中的组件"""
        # 先删除原有子组件
        for widget in self.frame_show_database.winfo_children():
            widget.destroy()

        # remainder
        try:
            self.dataframe_database
        except:
            tkinter.messagebox.showinfo(title="warning", message="Please select the type of database")
            return

        self.frame_search_1 = ttk.Frame(self.frame_show_database)
        self.frame_search_1.pack(padx=5, pady=5)

        self.label_search_name = ttk.Label(self.frame_search_1, text="name_of_glycan:", width=15)
        self.label_search_name.pack(side="left", padx=5, pady=5, anchor="e")
        self.var_search_name = tk.StringVar(value="")
        self.entry_search_name = ttk.Entry(self.frame_search_1, textvariable=self.var_search_name, width=15)
        self.entry_search_name.bind("<KeyPress>", self.search_button_state)
        self.entry_search_name.pack(side="left", padx=5, pady=5)

        self.label_search_date = ttk.Label(self.frame_search_1, text="date:", width=15)
        self.label_search_date.pack(side="left", padx=5, pady=5, anchor="e")
        self.var_search_date = tk.StringVar(value="")
        self.entry_search_date = ttk.Entry(self.frame_search_1, textvariable=self.var_search_date, width=15)
        self.entry_search_date.pack(side="left", padx=5, pady=5)

        self.label_search_flag = ttk.Label(self.frame_search_1, text="flag:", width=15)
        self.label_search_flag.pack(side="left", padx=5, pady=5, anchor="e")
        self.var_search_flag = tk.StringVar(value="")
        self.combobox_search_flag = ttk.Combobox(self.frame_search_1, textvariable=self.var_search_flag, width=15)
        self.combobox_search_flag["values"] = ["manu", "auto"]
        self.combobox_search_flag.pack(side="left", padx=5, pady=5)

        self.button_search = ttk.Button(self.frame_show_database, text="search", command=self.fetch)
        self.button_search.pack(padx=5, pady=5)

        self.frame_show_search = ttk.Frame(self.frame_show_database, height=10)
        self.frame_show_search.pack(side="top", padx=5, pady=5)
        # fill="both"

        self.scrollbar_search = ttk.Scrollbar(self.frame_show_search, orient='vertical')
        self.treeview_sheet_search = ttk.Treeview(self.frame_show_search,
                                                  columns=self.dataframe_database.columns, selectmode='extended',
                                                  show='headings',
                                                  yscrollcomman=self.scrollbar_search.set)
        # extend表示可以选中多行
        self.treeview_sheet_search.pack(fill="both", side="left", padx=3, pady=5)
        self.scrollbar_search.pack(fill="y", side="right", padx=3, pady=5)
        self.scrollbar_search.config(command=self.treeview_sheet_search.yview)

    def search_button_state(self, event):
        self.button_search.config(state="normal")

    def fetch(self):
        """search组件中涉及到的方法"""

        # 首先删除原有表单中的内容
        if self.treeview_sheet_search.get_children() != ():
            exit = self.treeview_sheet_search.get_children()
            for item in exit:
                self.treeview_sheet_search.delete(item)

        name = self.var_search_name.get()
        date = self.var_search_date.get()
        flag = self.var_search_flag.get()
        name = name.strip()  # 去掉string前后的空格
        date = date.strip()
        flag = flag.strip()
        # print(1,name, date, flag)

        # --------------------------------------------------------------------------------------------------------
        name_list = list(set(self.dataframe_database.iloc[:, 0].values.tolist()))  # glycan_name列表
        # print(name_list)

        index = []  # index: 搜索结果在self.dataframe_database中的编号
        self.search_result = []  # 根据index编号，将结果放在该列表里
        # eg: [['test1', 8.98, datetime.date(2019, 3, 10), 'manu'], ['test1', 8.99, datetime.date(2019, 3, 15), 'manu']]

        #### 不输入任何值的时候，搜索显示全部
        if name == "" and date == "" and flag == "":
            for i, col in enumerate(self.dataframe_database.columns):
                self.treeview_sheet_search.heading(column="#" + str(i + 1), text=col)
                self.treeview_sheet_search.column(i, width=150, anchor='w')

            for index, row in self.dataframe_database.iterrows():
                temp = []
                for i, j in enumerate(self.dataframe_database.columns):
                    temp.append(row[j])
                self.treeview_sheet_search.insert("", "end", values=temp)

        ### 没有输入glycan_name的情况
        elif name == "" and (date != "" or flag != ""):
            if date != "" and flag == "":
                index = self.dataframe_database[
                    self.dataframe_database["date"] == datetime.date(*map(int, date.split('-')))].index.tolist()
            elif date == "" and flag != "":
                index = self.dataframe_database[self.dataframe_database["flag"] == flag].index.tolist()
            elif date != "" and flag != "":
                index_flag = self.dataframe_database[self.dataframe_database["flag"] == flag].index.tolist()
                index_date = self.dataframe_database[
                    self.dataframe_database["date"] == datetime.date(*map(int, date.split('-')))].index.tolist()
                index = list(set(index_flag).intersection(set(index_date)))
                print("index_flag", index_flag)
                print("index_date", index_date)
            print(index)  # index: 搜索结果在self.dataframe_database中的编号

        ### 输入glycan_name, 但是不存在该名字
        elif name != "" and (name not in name_list):
            tkinter.messagebox.showinfo(title="warning", message="can not find!")

        ### 输入glycan_name, 且存在该名字
        elif name != "" and (name in name_list):
            # 利用sql语句在数据库中找相应的数据

            if date == "" and flag == "":
                index = self.dataframe_database[self.dataframe_database["name_of_glycan"] == name].index.tolist()
            elif date != "" and flag == "":
                index_name = self.dataframe_database[self.dataframe_database["name_of_glycan"] == name].index.tolist()
                index_date = self.dataframe_database[
                    self.dataframe_database["date"] == datetime.date(*map(int, date.split('-')))].index.tolist()
                index = list(set(index_name).intersection(set(index_date)))
            elif date == "" and flag != "":
                index_name = self.dataframe_database[self.dataframe_database["name_of_glycan"] == name].index.tolist()
                index_flag = self.dataframe_database[self.dataframe_database["flag"] == flag].index.tolist()
                index = list(set(index_name).intersection(set(index_flag)))
            elif date != "" and flag != "":
                index_name = self.dataframe_database[self.dataframe_database["name_of_glycan"] == name].index.tolist()
                index_flag = self.dataframe_database[self.dataframe_database["flag"] == flag].index.tolist()
                index_date = self.dataframe_database[
                    self.dataframe_database["date"] == datetime.date(*map(int, date.split('-')))].index.tolist()
                index = list(set(index_name).intersection(set(index_flag)).intersection(set(index_date)))

        # --------------------------------------------------------------------------------------------------------

        # 将结果添加进self.search_result
        if index != []:
            for each_index in index:
                # print(self.dataframe_database.iloc[each])
                temp = []
                for i, col in enumerate(self.dataframe_database.columns):
                    temp.append(self.dataframe_database.iloc[each_index, i])
                self.search_result.append(temp)
        print(self.search_result)

        if self.search_result == []:
            tkinter.messagebox.showinfo(title="warning", message="can not find!")

        if self.search_result != []:
            for i, col in enumerate(self.dataframe_database.columns):
                self.treeview_sheet_search.heading(column="#" + str(i + 1), text=col)
                self.treeview_sheet_search.column(i, width=150, anchor='w')
            for row in self.search_result:
                # print(row)
                self.treeview_sheet_search.insert("", "end", values=row[:])

    def add(self):
        # 先删除原有子组件
        for widget in self.frame_show_database.winfo_children():
            widget.destroy()

        # remainder  先提醒用户选择数据库
        try:
            self.dataframe_database
        except:
            tkinter.messagebox.showinfo(title="warning", message="Please select the type of database")
            return

        self.frame_add_1 = ttk.Frame(self.frame_show_database)
        self.frame_add_1.pack(padx=5, pady=5)

        self.label_add_name = ttk.Label(self.frame_add_1, text="name_of_glycan:")
        self.label_add_name.pack(side="left", padx=5, pady=5, anchor="e")
        self.var_add_name = tk.StringVar(value="")
        self.entry_add_name = ttk.Entry(self.frame_add_1, textvariable=self.var_add_name, width=15)
        self.entry_add_name.bind("<KeyPress>", self.add_button_state)
        self.entry_add_name.pack(side="left", padx=5, pady=5)

        self.label_add_MTU = ttk.Label(self.frame_add_1, text="MTU:")
        self.label_add_MTU.pack(side="left", padx=5, pady=5, anchor="e")
        self.var_add_MTU = tk.DoubleVar(value=0.0)
        self.entry_add_MTU = ttk.Entry(self.frame_add_1, textvariable=self.var_add_MTU, width=15)
        self.entry_add_MTU.pack(side="left", padx=5, pady=5)

        self.label_add_date = ttk.Label(self.frame_add_1, text="date:")
        self.label_add_date.pack(side="left", padx=5, pady=5, anchor="e")
        self.var_add_date = tk.StringVar(value=time.strftime("%Y-%m-%d", time.localtime()))
        self.entry_add_date = ttk.Entry(self.frame_add_1, textvariable=self.var_add_date, width=15)
        self.entry_add_date.pack(side="left", padx=5, pady=5)

        self.label_add_flag = ttk.Label(self.frame_add_1, text="flag:")
        self.label_add_flag.pack(side="left", padx=5, pady=5, anchor="e")
        self.var_add_flag = tk.StringVar(value="manu")
        self.combobox_add_flag = ttk.Combobox(self.frame_add_1, textvariable=self.var_add_flag, width=15)
        self.combobox_add_flag["values"] = ["manu", "auto"]
        self.combobox_add_flag.pack(side="left", padx=5, pady=5)

        self.button_add = ttk.Button(self.frame_show_database, text="add", command=self.add_into_database,
                                     state="disabled")
        self.button_add.pack(side="top", padx=5, pady=5)

    def add_button_state(self, event):
        # 其实也不需要这个 可以删除
        self.button_add.config(state="normal")

    def check_repeat_record_when_add(self, glycan_name, date):
        """每次向数据库增添数据时，根据输入的的glycan_name和date，判断该条数据是否出现过"""

        # 将date由str改成date形式
        date = datetime.date(*map(int, date.split('-')))

        for index, row in self.dataframe_database.iterrows():
            glycan_name_database = row["name_of_glycan"]
            date_database = row["date"]
            if glycan_name_database == glycan_name and date_database == date:
                return False
        return True

    def add_into_database(self):
        name = self.var_add_name.get()
        try:
            MTU = self.var_add_MTU.get()
        except:
            tkinter.messagebox.showinfo(title="warning", message="Invalid MTU")
            return
        date = self.var_add_date.get()
        flag = self.var_add_flag.get()
        name = name.strip()  # 去掉string前后的空格
        date = date.strip()  # string "2021-05-27"
        flag = flag.strip()

        if name == "" or date == "":
            tkinter.messagebox.showinfo(title="warning", message="Invalid Input")
        elif self.check_repeat_record_when_add(name, date) == False:
            tkinter.messagebox.showinfo(title="warning", message="重复数据")
        else:
            record = [name, MTU, date, flag]
            try:
                self.database.write_to_csv(record, self.combobox_which_database.get())
            except:
                tkinter.messagebox.showinfo(title="warning", message="Invalid Input")
            else:
                tkinter.messagebox.showinfo(title="success", message="Have been added!")
                self.dataframe_database = self.database.create_dataframe_from_csv(self.combobox_which_database.get())
                # 更新一下原始的dataframe, which comes from Database

    def delete(self):
        # 先删除原有子组件
        for widget in self.frame_show_database.winfo_children():
            widget.destroy()

        # remainder  先提醒用户选择数据库
        try:
            self.dataframe_database
        except:
            tkinter.messagebox.showinfo(title="warning", message="Please select the type of database")
            return

        self.search()
        self.button_delete = ttk.Button(self.frame_show_database, text="confirm to delete",
                                        command=self.delete_from_database, state="disabled")
        self.button_delete.pack(padx=3, pady=5)

        self.button_delete.config(state="normal")

    def delete_from_database(self):
        print('selection()', self.treeview_sheet_search.selection())
        self.delete_record = []
        for each in self.treeview_sheet_search.selection():
            self.delete_record.append(self.treeview_sheet_search.item(each, "values"))
        print(self.delete_record)
        if self.delete_record == []:
            tkinter.messagebox.showinfo(title="warning", message="没有选择删除记录")
        else:
            drop_index_list = []
            for record in self.delete_record:
                index_name = self.dataframe_database[
                    self.dataframe_database["name_of_glycan"] == record[0]].index.tolist()
                index_MTU = self.dataframe_database[self.dataframe_database["MTU"] == float(record[1])].index.tolist()
                index_flag = self.dataframe_database[self.dataframe_database["flag"] == record[3]].index.tolist()
                index_date = self.dataframe_database[
                    self.dataframe_database["date"] == datetime.date(*map(int, record[2].split('-')))].index.tolist()
                index = list(set(index_name).intersection(set(index_flag)).intersection(set(index_date)).intersection(
                    set(index_MTU)))
                print(index)
                drop_index_list.extend(index)
            print(drop_index_list)
            self.dataframe_database.drop(drop_index_list, inplace=True)
            print("没重新reset index", self.dataframe_database)
            self.dataframe_database.reset_index(drop=True, inplace=True)
            print("reset index", self.dataframe_database)
            # 删除完dataframe中的数据，将dataframe写回csv文件
            self.database.update_csv(self.dataframe_database, self.combobox_which_database.get())
            tkinter.messagebox.showinfo(title="success", message="Have been deleted!")
            self.dataframe_database = self.database.create_dataframe_from_csv(self.var_analysis_option.get())
            # 更新一下原始的dataframe, which comes from Database

    def update(self):
        # 先删除原有子组件   self.frame_show_database
        for widget in self.frame_show_database.winfo_children():
            widget.destroy()

        # remainder  先提醒用户选择数据库
        try:
            self.dataframe_database
        except:
            tkinter.messagebox.showinfo(title="warning", message="Please select the type of database")
            return

        self.frame_update_input = ttk.Frame(self.frame_show_database)
        self.frame_update_input.pack(side="top", fill="x", padx=5)
        self.button_update_input = ttk.Button(self.frame_update_input, text="input", command=self.update_input)
        self.button_update_input.pack(side="left", padx=5, pady=5, anchor="e")
        self.var_update_color = tk.StringVar()
        self.combobox_update_color = ttk.Combobox(self.frame_update_input, textvariable=self.var_update_color)
        self.combobox_update_color.config(state='disabled')
        self.combobox_update_color.pack(side="left", padx=5, pady=5, anchor="e")
        self.combobox_update_color.bind("<<ComboboxSelected>>", self.get_update_colour)

        self.button_update_input_view = ttk.Button(self.frame_update_input, text="view", command=self.update_input_view,
                                                   state="disabled")
        self.button_update_input_view.pack(side="left", padx=5, pady=5, anchor="e")

        self.frame_update_input_show = ttk.Frame(self.frame_show_database)
        self.frame_update_input_show.pack(side="top", fill="x", padx=5, pady=5)
        self.scrollbar_update_input_show = ttk.Scrollbar(self.frame_update_input_show, orient='vertical')
        self.treeview_sheet_update_input_show = ttk.Treeview(self.frame_update_input_show,
                                                             columns=self.dataframe_database.columns,
                                                             selectmode='extended',
                                                             show='headings',
                                                             yscrollcomman=self.scrollbar_update_input_show.set)
        self.treeview_sheet_update_input_show.pack(fill="both", side="left", padx=3)
        self.scrollbar_update_input_show.pack(fill="y", side="right", padx=3, pady=5)
        self.scrollbar_update_input_show.config(command=self.treeview_sheet_update_input_show.yview)

        ttk.Separator(self.frame_show_database).pack(fill="x")
        # --------------------------------------------------------------------------------------------------------------

        self.frame_update_match = ttk.Frame(self.frame_show_database)
        self.frame_update_match.pack(side="top", fill="x", padx=5)
        self.button_update_match = ttk.Button(self.frame_update_match, text="match1", command=self.update_match,
                                              state="disabled")
        self.button_update_match.pack(side="left", padx=5, pady=5, anchor="e")
        self.label_update_match = ttk.Label(self.frame_update_match, text="(samplename = glycanname)")
        self.label_update_match.pack(side="left", pady=5, anchor="e")
        self.button_update_match2 = ttk.Button(self.frame_update_match, text="match2", command=self.update_match2,
                                              state="disabled")
        self.button_update_match2.pack(side="left", padx=5, pady=5, anchor="e")
        self.label_update_match2 = ttk.Label(self.frame_update_match, text="(samplename = XXX_glycanname.fsa)")
        self.label_update_match2.pack(side="left", pady=5, anchor="e")
        self.button_update_match_view = ttk.Button(self.frame_update_match, text="view", command=self.update_match_view,
                                                   state="disabled")
        self.button_update_match_view.pack(side="left", padx=5, pady=5, anchor="e")
        self.button_update_delete = ttk.Button(self.frame_update_match, text="delete", command=self.update_delete,
                                               state="disabled")
        self.button_update_delete.pack(side="right", padx=5, pady=5, anchor="e")

        self.frame_update_match_show = ttk.Frame(self.frame_show_database)
        self.frame_update_match_show.pack(side="top", fill="x", padx=5, pady=5)
        self.scrollbar_update_match_show = ttk.Scrollbar(self.frame_update_match_show, orient='vertical')
        self.treeview_sheet_update_match_show = ttk.Treeview(self.frame_update_match_show,
                                                             columns=self.dataframe_database.columns,
                                                             selectmode='extended',
                                                             show='headings',
                                                             yscrollcomman=self.scrollbar_update_match_show.set)
        self.treeview_sheet_update_match_show.pack(fill="both", side="left", padx=3)
        self.scrollbar_update_match_show.pack(fill="y", side="right", padx=3, pady=5)
        self.scrollbar_update_match_show.config(command=self.treeview_sheet_update_match_show.yview)
        # self.treeview_sheet_update_match_show.bind('<ButtonRelease-1>', self.update_get_delete_record)

        ttk.Separator(self.frame_show_database).pack(fill="x")
        # --------------------------------------------------------------------------------------------------------------

        self.frame_update_update_to_database = ttk.Frame(self.frame_show_database)
        self.frame_update_update_to_database.pack(side="top", fill="x", padx=5)
        self.var_update_date = tk.StringVar(value=time.strftime("%Y-%m-%d", time.localtime()))
        self.entry_update_date = ttk.Entry(self.frame_update_update_to_database, textvariable=self.var_update_date,
                                           width=15, state="disabled")
        self.entry_update_date.pack(side="left", padx=5, pady=5)
        self.var_update_flag = tk.StringVar(value="manu")
        self.combobox_update_flag = ttk.Combobox(self.frame_update_update_to_database,
                                                 textvariable=self.var_update_flag)
        self.combobox_update_flag["values"] = ["manu", "auto"]
        self.combobox_update_flag.config(state='disabled')
        self.combobox_update_flag.pack(side="left", padx=5, pady=5)
        self.button_update_to_database = ttk.Button(self.frame_update_update_to_database, text="update to database",
                                                    command=self.update_to_database, state="disabled")
        self.button_update_to_database.pack(side="right", padx=5, pady=5, anchor="e")

    def update_input(self):

        filename = tkinter.filedialog.askopenfilename()

        try:
            self.update_raw_data = pd.read_csv(filename, sep="\t", engine='python', encoding='utf-8',
                                               error_bad_lines=False)
            self.update_raw_data_extract = self.update_raw_data.loc[:, ["Dye/Sample Peak", "Sample File Name", "Size","Height"]]
            print(self.update_raw_data)
            print(self.update_raw_data_extract)
            # 提取本次添加的数据
        except:
            tkinter.messagebox.showinfo(title="warning", message="Invalid File")
        else:
            ### 先选出有size值的
            self.update_raw_data_extract = self.update_raw_data_extract.loc[
                                           lambda x: np.isnan(x[x.columns[2]]) == False, :]

            self.combobox_update_color.config(state="readonly")
            self.list_update_all_colour = self.update_raw_data_extract.iloc[:, 0].str[0].unique().tolist()
            self.combobox_update_color["values"] = self.list_update_all_colour

    def get_update_colour(self, *args):
        print(self.combobox_update_color.get())

        ### 提取self.update_raw_data_extract中相应颜色的数据
        self.update_raw_data_extract = self.update_raw_data_extract[self.update_raw_data_extract \
            [self.update_raw_data_extract.columns[0]].str.contains(self.combobox_update_color.get())]
        print("self.update_raw_data_extract")
        print(self.update_raw_data_extract)

        self.button_update_input_view.config(state="normal")

    def update_input_view(self):

        ##### 在表单中展示源数据
        # 首先删除原有表单中的内容
        if self.treeview_sheet_update_input_show.get_children() != ():
            exit = self.treeview_sheet_update_input_show.get_children()
            for item in exit:
                self.treeview_sheet_update_input_show.delete(item)

        # 向表单中添加数据
        for i, col in enumerate(self.update_raw_data_extract.columns):
            self.treeview_sheet_update_input_show.heading(column="#" + str(i + 1), text=col)
            self.treeview_sheet_update_input_show.column(i, width=150, anchor='w')

        for index, row in self.update_raw_data_extract.iterrows():
            temp = []
            for i, j in enumerate(self.update_raw_data_extract.columns):
                temp.append(row[j])
            self.treeview_sheet_update_input_show.insert("", "end", values=temp)

        self.button_update_match.config(state="normal")
        self.button_update_match2.config(state="normal")
        self.button_update_input.config(state="disabled")
        self.combobox_update_color.config(state="disabled")

    def update_match(self):
        ##### # 源数据的glycan_name作为键 值为相应的MTU列表
        self.dict_update_match = {}
        for index, row in self.update_raw_data_extract.iterrows():
            # print(row[0], row[1])
            if row[1] not in self.dict_update_match.keys():
                self.dict_update_match[row[1]] = [[row[2], row[3]]]
            else:
                self.dict_update_match[row[1]].append([row[2], row[3]])
        print("self.dict_update_match")
        print(self.dict_update_match)

        ##### 针对于每一个源数据中的glycan_name，在数据库中找其相对应的最新的MTU值
        self.update_match_result = pd.DataFrame(columns=["name of glycan", "new_MTU", "height", "latest_MTU", "new"])
        for each in self.dict_update_match.keys():
            print(each)
            index = self.dataframe_database[self.dataframe_database["name_of_glycan"] == each].index.tolist()
            match_find = pd.DataFrame(columns=["name of glycan", "MTU", "date", "flag"])
            search_result = []
            # eg: [['test1', 8.98, datetime.date(2019, 3, 10), 'manu'], ['test1', 8.99, datetime.date(2019, 3, 15), 'manu']]
            if index != []:
                for each_index in index:
                    # print(self.dataframe_database.iloc[each])
                    temp = []
                    for i, col in enumerate(self.dataframe_database.columns):
                        temp.append(self.dataframe_database.iloc[each_index, i])
                    search_result.append(temp)
            for temp in search_result:
                match_find = match_find.append({"name of glycan": temp[0], "MTU": temp[1], "date": temp[2],
                                                "flag": temp[3]}, ignore_index=True)

            if match_find.empty:  # 数据库中无该glycan记录
                for [new_MTU, height] in self.dict_update_match[each]:
                    self.update_match_result = self.update_match_result.append(
                        {"name of glycan": each, "new_MTU": new_MTU, "height": height,
                         "latest_MTU": "None", "new": "Yes"}, ignore_index=True)
            else:
                print(each)
                # 找出与上次测量最相近的MTU
                latest_MTU = float(match_find.sort_values(by="date").iloc[-1]["MTU"])
                new_MTU = self.dict_update_match[each][0][0]
                height = self.dict_update_match[each][0][1]
                for [i_MTU, i_height] in self.dict_update_match[each]:
                    if abs(latest_MTU - new_MTU) > abs(latest_MTU - i_MTU):
                        new_MTU = i_MTU
                        height = i_height

                self.update_match_result = self.update_match_result.append({"name of glycan": each, "new_MTU": new_MTU,
                                                                            "height": height,
                                                                            "latest_MTU": latest_MTU, "new": "No"},
                                                                           ignore_index=True)
        # print(self.update_match_result)
        self.button_update_match_view.config(state="normal")

    def update_match2(self):
        ##### # 源数据的glycan_name作为键 值为相应的MTU列表
        self.dict_update_match = {}
        for index, row in self.update_raw_data_extract.iterrows():
            # print(row[0], row[1]) # B,18 B01_GM1-dg.fsa
            index1 = row[1].find("_")
            index2 = row[1].find(".")
            name = row[1][index1+1:index2]
            if name not in self.dict_update_match.keys():
                self.dict_update_match[name] = [[row[2], row[3]]]  # row[2]:MTU row[3]:height
            else:
                self.dict_update_match[name].append([row[2], row[3]])
        print("self.dict_update_match")
        print(self.dict_update_match)

        ##### 针对于每一个源数据中的glycan_name，在数据库中找其相对应的最新的MTU值
        self.update_match_result = pd.DataFrame(columns=["name of glycan", "new_MTU", "height", "latest_MTU", "new"])
        for each in self.dict_update_match.keys():
            print(each)
            index = self.dataframe_database[self.dataframe_database["name_of_glycan"] == each].index.tolist()
            match_find = pd.DataFrame(columns=["name of glycan", "MTU", "date", "flag"])
            search_result = []
            # eg: [['test1', 8.98, datetime.date(2019, 3, 10), 'manu'], ['test1', 8.99, datetime.date(2019, 3, 15), 'manu']]
            if index != []:
                for each_index in index:
                    # print(self.dataframe_database.iloc[each])
                    temp = []
                    for i, col in enumerate(self.dataframe_database.columns):
                        temp.append(self.dataframe_database.iloc[each_index, i])
                    search_result.append(temp)
            for temp in search_result:
                match_find = match_find.append({"name of glycan": temp[0], "MTU": temp[1], "date": temp[2],
                                                "flag": temp[3]}, ignore_index=True)

            if match_find.empty:  # 数据库中无该glycan记录
                for [new_MTU, height] in self.dict_update_match[each]:
                    self.update_match_result = self.update_match_result.append(
                        {"name of glycan": each, "new_MTU": new_MTU, "height": height,
                         "latest_MTU": "None", "new": "Yes"}, ignore_index=True)
            else:
                print(each)
                # 找出与上次测量最相近的MTU
                latest_MTU = float(match_find.sort_values(by="date").iloc[-1]["MTU"])
                new_MTU = self.dict_update_match[each][0][0]
                height = self.dict_update_match[each][0][1]
                for [i_MTU, i_height] in self.dict_update_match[each]:
                    if abs(latest_MTU - new_MTU) > abs(latest_MTU - i_MTU):
                        new_MTU = i_MTU
                        height = i_height

                self.update_match_result = self.update_match_result.append({"name of glycan": each, "new_MTU": new_MTU,
                                                                            "height": height,
                                                                            "latest_MTU": latest_MTU, "new": "No"},
                                                                           ignore_index=True)
        # print(self.update_match_result)
        self.button_update_match_view.config(state="normal")

    def update_match_view(self):

        #####将self.update_match_result展示在表单中
        # 首先删除原有表单中的内容
        if self.treeview_sheet_update_match_show.get_children() != ():
            exit = self.treeview_sheet_update_match_show.get_children()
            for item in exit:
                self.treeview_sheet_update_match_show.delete(item)

        # 向表单中添加数据
        for i, col in enumerate(self.update_match_result.columns):
            self.treeview_sheet_update_match_show.heading(column="#" + str(i + 1), text=col)
            self.treeview_sheet_update_match_show.column(i, width=150, anchor='w')

        for index, row in self.update_match_result.iterrows():
            temp = []
            for i, j in enumerate(self.update_match_result.columns):
                temp.append(row[j])
            self.treeview_sheet_update_match_show.insert("", "end", values=temp)

        self.button_update_match.config(state="disabled")
        self.entry_update_date.config(state="normal")
        self.combobox_update_flag.config(state="normal")
        self.button_update_to_database.config(state="normal")
        self.button_update_delete.config(state="normal")

    # def update_get_delete_record(self, event):
    #     self.button_update_delete.config(state="normal")
    #     self.delete_record = self.treeview_sheet_update_match_show.item(
    #         self.treeview_sheet_update_match_show.selection(), "values")
    #     # selection -> Returns the tuple of selected items.
    #     print(self.delete_record)

    def update_delete(self):
        ### 获得用户选择的删除选项
        print(self.treeview_sheet_update_match_show.selection())
        self.delete_record = []
        for record in self.treeview_sheet_update_match_show.selection():
            self.delete_record.append(list(self.treeview_sheet_update_match_show.item(record, "values")))
        print(self.delete_record)

        ### 从self.update_match_result中删除用户所选择的record
        for index, row in self.update_match_result.iterrows():
            temp = []
            for i, j in enumerate(self.update_match_result.columns):
                temp.append(str(row[j]))

            if temp in self.delete_record:
                print("delete")
                self.update_match_result = self.update_match_result.drop([index])
        # print(self.update_match_result)
        self.update_match_view()

    def update_to_database(self):
        # print(self.var_update_flag.get())
        # print(self.var_update_date.get())
        # print(self.update_match_result)
        # check_repeat_record_when_add(self, glycan_name, date)

        ### 检查是否有重复数据
        # 将date由str改成date形式
        # date = datetime.date(*map(int, self.var_update_date.get().split('-')))
        date = self.var_update_date.get()
        for index, row in self.update_match_result.iterrows():
            name = row["name of glycan"]
            if self.check_repeat_record_when_add(name, date) == False:
                tkinter.messagebox.showinfo(title="warning", message="重复数据")
                return

        try:
            for index, row in self.update_match_result.iterrows():
                record = [row["name of glycan"], row["new_MTU"], self.var_update_date.get(), self.var_update_flag.get()]
                self.database.write_to_csv(record, self.combobox_which_database.get())
        except:
            tkinter.messagebox.showinfo(title="warning", message="Invalid Input")
        else:
            tkinter.messagebox.showinfo(title="success", message="Have been updated!")
            self.dataframe_database = self.database.create_dataframe_from_csv(self.combobox_which_database.get())
            # 更新一下原始的dataframe, which comes from Database

        self.entry_update_date.config(state="disabled")
        self.combobox_update_flag.config(state="disabled")

    def creatWidge(self):
        """对应于GUI2中的self.frame_database = ttk.Frame(self.tab)"""
        self.frame_main = ttk.Frame(self, height=640, width=1020)
        self.frame_main.pack(fill="both", expand=True)
        self.frame_main.pack_propagate(0)
        # expand=True

        # self.frame_choose_database = ttk.Frame(self.frame_main, height=5, borderwidth=2, relief="ridge")
        self.frame_choose_database = ttk.Frame(self.frame_main, relief="ridge", height=50)
        self.frame_choose_database.pack(side="top", fill="x")
        self.frame_choose_database.pack_propagate(0)
        # self.frame_choose_database.grid(row=0, column=0, rowspan=1, columnspan=6, padx=3, pady=3, sticky="EW")
        self.label_type_of_database = ttk.Label(self.frame_choose_database, text="type of database:")
        self.label_type_of_database.pack(side="left", padx=3)
        # self.label_type_of_database.grid(row=0, column=0, padx=3, pady=3, sticky="EW")
        self.combobox_which_database = ttk.Combobox(self.frame_choose_database,
                                                    textvariable=self.var_analysis_option)
        self.combobox_which_database["values"] = self.ANALYSIS_OPTIONS
        # self.combobox_which_database.current(0)  # 设置初始显示值，值为元组['values']的下标
        self.combobox_which_database.config(state='readonly')  # 设为只读模式
        self.combobox_which_database.pack(side="left", padx=3)
        self.combobox_which_database.bind("<<ComboboxSelected>>", self.get_which_database)
        self.label_show_which_database = ttk.Label(self.frame_choose_database,
                                                   textvariable=self.var_analysis_option)
        self.label_show_which_database.pack(side="right", padx=3)
        # self.label_show_which_database.grid(row=0, column=6, padx=3, pady=3, sticky="EW")

        self.frame_edit_database = ttk.Frame(self.frame_main, relief="ridge")
        self.frame_edit_database.pack(side="left", fill="y")
        self.button_database_showall = ttk.Button(self.frame_edit_database, text="show all", command=self.show_all)
        self.button_database_showall.pack(pady=10, padx=10)
        self.button_database_version = ttk.Button(self.frame_edit_database, text="version", command=self.version)
        self.button_database_version.pack(pady=10, padx=10)
        self.button_database_search = ttk.Button(self.frame_edit_database, text="search", command=self.search)
        self.button_database_search.pack(pady=10, padx=10)
        self.button_database_add = ttk.Button(self.frame_edit_database, text="add", command=self.add)
        self.button_database_add.pack(pady=10, padx=10)
        self.button_database_delete = ttk.Button(self.frame_edit_database, text="delete", command=self.delete)
        self.button_database_delete.pack(pady=10, padx=10)
        self.button_database_update = ttk.Button(self.frame_edit_database, text="update", command=self.update)
        self.button_database_update.pack(pady=10, padx=10)

        self.frame_show_database = ttk.Frame(self.frame_main, relief="ridge", width=920)
        # self.frame_show_database.grid(row=1, column=1, rowspan=6, columnspan=5, padx=3, pady=3, sticky="EW")
        self.frame_show_database.pack_propagate(0)
        self.frame_show_database.pack(side="right", fill="both")
        self.frame_show_database.grid_propagate(0)
        # 不加grid_propagate(0)的话，在add()函数中，用grid布局的组件会影响frame的大小


if __name__ == "__main__":
    root = tk.Tk()  # 创建跟窗口对象
    root.geometry("1200x740+100+100")
    root.title("Frame_Database")
    database = FrameDatabase(master=root)  # the object of the class Database
    database.creatWidge()
    root.mainloop()
