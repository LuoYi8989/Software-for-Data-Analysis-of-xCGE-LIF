import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import tkinter.scrolledtext
import tkinter.messagebox
import os
import pandas as pd
import numpy as np
import copy


class FrameOverview(ttk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.dataframe_all_raw_data = pd.DataFrame()  # 存储所有文件中的原始数据
        self.dict_selected_data_before_color = {} # 用户选择颜色通道之前
        self.dict_selected_data = {}  # 存放在用户选择后，需要处理的数据 格式 key:sample_name value:该名称中所有的数据

        # 为了给frame_analysed_data传递参数
        self.dataframe_all_raw_data = None
        self.reference_sample = None  # 用户选的reference_sample名: 数据
        self.list_replicates_samples = []
        self.dict_replicates_groups = {}  # {group_name1:[samples], group_name2:[samples]...}
        # self.creatWidge()

    def call_filedialog(self):
        """输入文件，获取所有文件的数据"""
        filename = tkinter.filedialog.askopenfilename()
        filename_output = os.path.basename(filename)
        # for i in range(len(filename)):
        #     if filename[len(filename) - i - 1] != "/":
        #         filename_output += filename[len(filename) - i - 1]
        #     else:
        #         break

        self.text_inputfile.delete(1.0, 'end')  # 删除所有元素

        self.text_inputfile.insert(tk.END, filename_output)
        self.text_inputfile.insert(tk.END, "\n")
        ### 以上是在界面中显示的部分

        ### 接下来建立DataFrame
        try:
            self.dataframe_all_raw_data = pd.read_csv(filename, sep="\t", engine='python', encoding='utf-8')
            # 提取本次添加的数据 这里的分隔符其实是空格
            # sep = "\s+|\t+|\s+\t+|\t+\s+"   将使用任意数量的空格和制表符的任意组合作为分隔符。 |：或
        except:
            tkinter.messagebox.showinfo(title="warning", message="Invalid File")
            # 将本次添加的数据添加到self.dataframe_all_raw_date中
        # print(1000000, raw_data_all)
        print("all", self.dataframe_all_raw_data)

    def sort_list_char(self, alist):
        """给samplename排序"""
        # 所有名字有下划线，按照下划线最后一部分的字符串进行排序
        # 所有名字都没有下划线，按照原名排序
        # 混合，按照原名排序
        list_samplesname_without_ = []
        dict_samplesname_with_ = {}  # {A1_luo01:luo01, A2_luo02:luo02}
        for i, each in enumerate(alist):
            if each.find("_") == -1:  # 没有下划线
                list_samplesname_without_.append(each)
            else:
                dict_samplesname_with_[each] = each.partition("_")[-1]
        list_samplesname_without_.sort()
        if dict_samplesname_with_ != {}:
            list_sort_samplesname_with_ = sorted(dict_samplesname_with_.items(), key=lambda item: item[1])
            list_sort_samplesname_with_ = [each[0] for i, each in enumerate(list_sort_samplesname_with_)]
        else:
            list_sort_samplesname_with_ = []

        return list_samplesname_without_ + list_sort_samplesname_with_


    def ensure_inputfile(self):
        """获取所有samples_name"""

        self.button_inputfile.config(state='disabled')

        ### 读取源数据后进行分组 这里获取所有Sample_name  self.all_samplesname
        self.all_samplesname_unsort = self.dataframe_all_raw_data["Sample File Name"].unique().tolist()
        print(self.all_samplesname_unsort)

        try:
            self.all_samplesname = self.sort_list_char(self.all_samplesname_unsort)
            print(self.all_samplesname)
        except:
            self.all_samplesname = self.all_samplesname_unsort

        self.combobox_choose_reference_sample.config(state='readonly')
        list_show_all_samplesname = copy.deepcopy(self.all_samplesname)  # with None
        list_show_all_samplesname.append("None")
        print(list_show_all_samplesname)
        self.combobox_choose_reference_sample["values"] = list_show_all_samplesname

    def get_choosen_reference_sample(self, *args):
        """获取用户选择的reference_sample，显示用户需选择的samples"""
        ### 获取reference_sample
        if self.combobox_choose_reference_sample.get() == "None":
            self.reference_sample_name = None
        else:
            self.reference_sample_name = self.combobox_choose_reference_sample.get()

        print(self.reference_sample_name)

        ### 让用户选择将要处理的samples
        self.all_samplesname_state = []  # 按钮状态列表  每一个samplename都需要一个变量来记录它是否被选中

        ## 调整self.canvas_choose_sample滚轮长度以适应self.all_samplesname长度
        if len(self.all_samplesname) > 13:
            # long = 450 + ((len(self.all_samplesname) - 13) // 3 + 1) * 100
            long = 450 + ((len(self.all_samplesname) - 13) // 3) * 100
            # 450是不加滑块的长度 对应于13个名字长度
            # 以后每增加100长度，可增加3个名字
            self.canvas_choose_sample.config(scrollregion=(0, 0, long, long))

        for i, each in enumerate(self.all_samplesname):
            frame_temp = tk.Frame(self.canvas_choose_sample)
            self.canvas_choose_sample.create_window((10, 10 + i * 30), window=frame_temp, anchor="nw")
            label_sample = tk.Label(frame_temp, text=each)
            label_sample.pack(side="left")
            exec('self.v{} = tk.IntVar()'.format(i))
            exec('self.v{}.set(1)'.format(i))
            exec('radiobutton_r = tk.Radiobutton(frame_temp, text="Remain", variable=self.v{},value=1)'.format(i))
            exec('radiobutton_c = tk.Radiobutton(frame_temp, text="Cancel", variable=self.v{},value=0)'.format(i))
            exec('radiobutton_r.pack(side="left")')
            exec('radiobutton_c.pack(side="left")')

        self.button_ensure_choose_sample.config(state="normal")

    def canvas_choose_sample_mousewheel(self, event):
        """让canvas能够使用鼠标滚轮滑动"""
        self.canvas_choose_sample.yview_scroll(-1 * event.delta, "units")
        # self.canvas_choose_sample.yview_scroll(-1 * (event.delta / 120), "units")
        # 在 Windows 上，您绑定到<MouseWheel>并且需要除以event.delta120（或其他一些因素，具体取决于您希望滚动的速度）
        # 在 OSX 上，您绑定到<MouseWheel>并且您需要event.delta不加修改地使用

    def get_chosen_samplesname(self):
        """1.获取用户选择的将要处理的samples_name, 2.让用户选择颜色通道"""
        self.button_ensure_choose_sample.config(state="disabled")
        ####### 处理self.dataframe_all_raw_data 构建一个字典，key是sample名称，value是该组中所有的数据
        # 先选出有size值的
        dataframe_raw_data_hassize = self.dataframe_all_raw_data.loc[lambda raw_data_all:
                                                                     np.isnan(raw_data_all[
                                                                                  raw_data_all.columns[2]]) == False, :]
        # print(dataframe_raw_data_hassize)
        # 按名称添加进字典
        for temp_name in self.all_samplesname:
            temp_data = dataframe_raw_data_hassize[
                dataframe_raw_data_hassize[dataframe_raw_data_hassize.columns[1]].isin([temp_name])].reset_index(
                drop=True)
            exec('self.dict_selected_data_before_color["%s" % temp_name] = temp_data')
        # print(self.dict_selected_data)
        print(self.dict_selected_data_before_color.keys())

        #####获取reference_sample的数据

        if self.reference_sample_name != None:
            self.reference_sample_before_color = {}
            self.reference_sample_before_color[self.reference_sample_name] = self.dict_selected_data_before_color[self.reference_sample_name]
        else:
            self.reference_sample_before_color = None

        ###### 获取用户对数据的选择
        for i, each in enumerate(self.all_samplesname):
            loc = locals()
            # https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p23_executing_code_with_local_side_effects.html
            exec('select_result = self.v{}.get()'.format(i))
            select_result = loc['select_result']

            if select_result == 0:
                # 修改self.dict_selected_data中的内容
                self.dict_selected_data_before_color.pop(each)
        # 最终self.dict_selected_data就是用户选择sample_name后的结果


        ####### 获取上述samples的所有颜色
        self.list_all_channel_colour = []
        for i, each in enumerate(self.dict_selected_data_before_color.keys()):
            temp_color = self.dict_selected_data_before_color[each].iloc[:, 0].str[0].unique().tolist()
            self.list_all_channel_colour.extend(temp_color)
        self.list_all_channel_colour = list(set(self.list_all_channel_colour))
        # print(self.list_all_channel_colour)

        self.combobox_choose_colour.config(state='readonly')
        self.combobox_choose_colour["values"] = self.list_all_channel_colour
        # self.combobox_group_number_replicates.config(state='readonly')
        # self.combobox_group_number_replicates_values = [i + 1 for i in range(len(self.dict_selected_data.keys()))]
        # self.combobox_group_number_replicates_values.insert(0, 0)
        # self.combobox_group_number_replicates["values"] = self.combobox_group_number_replicates_values
        self.combobox_choose_reference_sample.config(state='disabled')

    def get_choosen_channel_colour(self, *args):
        """获取用户选择的颜色通道"""
        # self.combobox_choose_colour.get()获取用户选择的通道颜色
        # 从self.dict_selected_data_before_color中提取相应通道颜色的数据
        print(self.combobox_choose_colour.get())
        print(type(self.combobox_choose_colour.get()))
        self.button_ensure_choose_sample.config(state='disabled')
        self.combobox_group_number_replicates.config(state='readonly')
        self.combobox_group_number_replicates_values = [i + 1 for i in range(len(self.dict_selected_data_before_color.keys()))]
        self.combobox_group_number_replicates_values.insert(0, 0)
        self.combobox_group_number_replicates["values"] = self.combobox_group_number_replicates_values

        for i, each in enumerate(self.dict_selected_data_before_color.keys()):
            self.dict_selected_data[each] = self.dict_selected_data_before_color[each][
                self.dict_selected_data_before_color[each][self.dict_selected_data_before_color[each].columns[0]].str.contains(
                    self.combobox_choose_colour.get())]
            self.dict_selected_data[each].reset_index(drop=True, inplace=True)

        ### 处理reference_sample的颜色通道
        if self.reference_sample_name != None:
            self.reference_sample = {}
            self.reference_sample[self.reference_sample_name] = self.reference_sample_before_color[self.reference_sample_name][
                self.reference_sample_before_color[self.reference_sample_name][self.reference_sample_before_color[self.reference_sample_name]
                    .columns[0]].str.contains(
                    self.combobox_choose_colour.get())]
            self.reference_sample[self.reference_sample_name].reset_index(drop=True, inplace=True)
        else:
            self.reference_sample = None

        # self.combobox_choose_colour.config(state='disabled')

        print("self.dict_selected_data_before_color", self.dict_selected_data_before_color)
        print("self.dict_selected_data", self.dict_selected_data)
        print("self.reference_sample", self.reference_sample)

    def get_if_replicates(self, *args):
        """获取replicates_group个数，并按组让用户选择对应的sample"""
        # self.combobox_group_number_replicates   self.canvas_choose_replicates

        self.group_number_replicates = int(self.combobox_group_number_replicates.get())
        print(self.group_number_replicates)

        if self.group_number_replicates == 0:
            return

        self.all_selected_samplesname = list(self.dict_selected_data.keys())

        ### 分组让用户选择
        self.group_num = 1
        self.choose_replicate()
        self.label_group_choose_replicates.config(text="group %d" % self.group_num)
        # self.button_ensure_choose_replicates.config(state='disabled')
        self.button_ensure_input_replicates_name.config(state='disabled')

    def choose_replicate(self):
        """让用户在每个replicates_group中选择相应的samples"""
        # 先删除原有子组件
        for widget in self.canvas_choose_replicates.winfo_children():
            widget.destroy()

        # 设置滑块长度
        if len(self.all_selected_samplesname) > 6:
            long = 200 + ((len(self.all_selected_samplesname) - 6) // 3 + 1) * 100
            # 200是不加滑块的长度 对应于6个名字长度
            # 以后每增加100长度，可增加3个名字
            self.canvas_choose_replicates.config(scrollregion=(0, 0, long, long))

        frame_temp_group = tk.Frame(self.canvas_choose_replicates)
        # self.canvas_choose_replicates.create_window((10, 80), window=frame_temp_group, anchor="w")
        self.canvas_choose_replicates.create_window((10, 5), window=frame_temp_group, anchor="nw")
        for i, each in enumerate(self.all_selected_samplesname):
            frame_temp = tk.Frame(frame_temp_group)
            frame_temp.pack(fill="x", pady=5)
            label_sample = tk.Label(frame_temp, text=each)
            label_sample.pack(side="left")
            exec('self.v{}_replicates_g{} = tk.IntVar()'.format(i, self.group_num))
            exec('self.v{}_replicates_g{}.set(0)'.format(i, self.group_num))
            exec('radiobutton_y = tk.Radiobutton(frame_temp, text="Yes", variable=self.v{}_replicates_g{},value=1)'.format(i, self.group_num))
            exec('radiobutton_n = tk.Radiobutton(frame_temp, text="No", variable=self.v{}_replicates_g{},value=0)'.format(i, self.group_num))
            exec('radiobutton_y.pack(side="left")')
            exec('radiobutton_n.pack(side="left")')

        self.button_ensure_choose_replicates.config(state='normal')

    def canvas_choose_replicates_mousewheel(self, event):
        """让canvas能够使用鼠标滚轮滑动"""
        self.canvas_choose_replicates.yview_scroll(-1 * event.delta, "units")
        # self.canvas_choose_sample.yview_scroll(-1 * (event.delta / 120), "units")
        # 在 Windows 上，您绑定到<MouseWheel>并且需要除以event.delta120（或其他一些因素，具体取决于您希望滚动的速度）
        # 在 OSX 上，您绑定到<MouseWheel>并且您需要event.delta不加修改地使用

    def get_replicates_groups(self):
        self.combobox_choose_colour.config(state='disabled')
        """获取用户的选择，选完后，让用户输入group_name"""
        # self.dict_replicates_groups
        # self.combobox_group_number_replicates.config(state='disabled')

        ### 获取用户的选择
        for num in range(self.group_number_replicates):
            # https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p23_executing_code_with_local_side_effects.html
            loc = locals()
            list_samples_of_this_group = []
            for i, each in enumerate(self.all_selected_samplesname):
                exec('select_result = self.v{}_replicates_g{}.get()'.format(i, self.group_num))
                select_result = loc['select_result']
                print(select_result)
                if select_result == 1:
                    list_samples_of_this_group.append(each)
                    print(each)
            self.dict_replicates_groups[self.group_num] = list_samples_of_this_group.copy()
        print(self.dict_replicates_groups)


        if self.group_num == self.group_number_replicates:
            ### 让用户输入组名
            self.button_ensure_choose_replicates.config(state='disabled')
            self.button_ensure_input_replicates_name.config(state='normal')

            # 先删除原有子组件
            for widget in self.canvas_replicates_name.winfo_children():
                widget.destroy()

            # 设置滑块长度
            if len(self.dict_replicates_groups) > 2:
                height = 200 + (len(self.dict_replicates_groups) - 2 + 1) * 100
            else:
                height = 200
                # 200是不加滑块的长度 对应于2个group
                # 以后每增加100长度，可增加1个名字
                # self.canvas_replicates_name.config(scrollregion=(0, 0, long, long))

            frame_temp_group = tk.Frame(self.canvas_replicates_name)
            self.canvas_replicates_name.create_window((10, 10), window=frame_temp_group, anchor="nw")
            longest_text = 0
            for i, group in enumerate(self.dict_replicates_groups.keys()):
                frame_temp_label = tk.Frame(frame_temp_group)  # for beauty
                frame_temp_label.pack(fill="x", side="top")
                text = str(group) + ":  "
                for each in self.dict_replicates_groups[group]:
                    text += each
                    text += "  "
                if len(text) > longest_text:
                    longest_text = len(text)
                    print(longest_text)
                label = tk.Label(frame_temp_label, text=text, anchor="w")
                label.pack(side="left", padx=5, pady=5)
                frame_temp_entry = tk.Frame(frame_temp_group)  # for beauty
                frame_temp_entry.pack(fill="x", side="top")
                exec('self.entry_replicates_name_g{} = tk.Entry(frame_temp_entry)'.format(group))
                exec('self.entry_replicates_name_g{}.pack(side="left", padx=5, pady=5)'.format(group))

            # 250的长度可以展示25个字符  多余25个字符的 每个字符占10长度
            if longest_text > 25:
                long = 250 + (longest_text-25)*10
                print(long)
            self.canvas_replicates_name.config(scrollregion=(0, 0, long, height))
            # scrollregion 指定 Canvas 可以被滚动的范围   该选项的值是一个 4 元组（x1, y1, x2, y2）表示的矩形

        else:
            ### 对下一组进行选择
            self.group_num += 1
            self.choose_replicate()
            self.label_group_choose_replicates.config(text="group %d" % self.group_num)


    def get_replicates_group_name(self):
        """获取用户输入的group_name"""

        self.dict_replicates_groups_new_name = {}
        for i, group in enumerate(self.dict_replicates_groups.keys()):
            # https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p23_executing_code_with_local_side_effects.html
            loc = locals()
            exec('group_name = self.entry_replicates_name_g{}.get()'.format(group))
            group_name = loc['group_name']
            group_name = group_name.strip()  # 去掉首位空格
            if group_name == '':
                tkinter.messagebox.showinfo(title="warning", message="Invalid group's name")
                return
            if len(group_name) > 20:
                tkinter.messagebox.showinfo(title="warning", message="group's name too long")
                return
            self.dict_replicates_groups_new_name[group_name] = self.dict_replicates_groups[group]

        # del(self.dict_replicates_groups)
        self.dict_replicates_groups = copy.deepcopy(self.dict_replicates_groups_new_name)
        # del(self.dict_replicates_groups_new_name)
        print(self.dict_replicates_groups)
        # {'AB': ['A08_EG09.fsa', 'B08_EG10.fsa'], 'GH': ['G07_EG07.fsa', 'H07_EG08.fsa']}

        self.button_ensure_input_replicates_name.config(state='disabled')
        for i, group in enumerate(self.dict_replicates_groups.keys()):
            exec('self.entry_replicates_name_g{}.config(state="disabled")'.format(i+1))

    def canvas_replicates_name_mousewheel(self, event):
        """让canvas能够使用鼠标滚轮滑动"""
        self.canvas_replicates_name.yview_scroll(-1 * event.delta, "units")
        # self.canvas_choose_sample.yview_scroll(-1 * (event.delta / 120), "units")
        # 在 Windows 上，您绑定到<MouseWheel>并且需要除以event.delta120（或其他一些因素，具体取决于您希望滚动的速度）
        # 在 OSX 上，您绑定到<MouseWheel>并且您需要event.delta不加修改地使用



    def creatWidge(self):
        """对应于GUI2中的 self.frame_overview = ttk.Frame(self.tab)"""
        self.frame_main = ttk.Frame(self, height=640, width=1020)
        self.frame_main.pack(fill="both", expand=True)
        self.frame_main.pack_propagate(0)

        # 设置三窗格布局
        self.panedwindow1 = ttk.PanedWindow(self.frame_main, orient="horizontal")
        self.panedwindow1.pack(fill="both", padx=10, pady=10, expand=1)
        # , expand=1

        self.frame_input = ttk.Frame(self.panedwindow1, width=100, relief="sunken")
        self.panedwindow1.add(self.frame_input)

        self.panedwindow2 = ttk.PanedWindow(self.panedwindow1, orient="horizontal")
        # sashrelief="sunken"
        self.panedwindow1.add(self.panedwindow2)

        self.frame_choose_sample = ttk.Frame(self.panedwindow2, width=200, relief="sunken")
        self.panedwindow2.add(self.frame_choose_sample)

        self.frame_replicates = ttk.Frame(self.panedwindow2, width=200, relief="sunken")
        self.panedwindow2.add(self.frame_replicates)

        # self.frame_input = ttk.Frame(self.frame_main, width=100, relief="sunken")
        # self.frame_input.pack(side="left", fill="y", padx=10, pady=10, expand=1)
        #
        # self.frame_choose_sample = ttk.Frame(self.frame_main, width=200, relief="sunken")
        # self.frame_choose_sample.pack(side="left", fill="y", padx=10, pady=10, expand=1)
        #
        # self.frame_replicates = ttk.Frame(self.frame_main, width=200, relief="sunken")
        # self.frame_replicates.pack(side="right", fill="y", padx=10, pady=10, expand=1)

        # --------------------------------------------------------------------------------------------------------------
        # ---------------- 向frame_input中填充部件

        self.button_inputfile = ttk.Button(self.frame_input, text="input", command=self.call_filedialog)
        self.button_inputfile.pack(side="top", padx=5, pady=5)

        self.label_filename = ttk.Label(self.frame_input, text="filename")
        self.label_filename.pack(side="top", padx=5, pady=5)

        self.text_inputfile = tkinter.scrolledtext.ScrolledText(self.frame_input, width=100)
        self.text_inputfile.pack(side="top", fill="both", padx=5, pady=5)

        self.button_ensure_inputfile = ttk.Button(self.frame_input, text="ok", command=self.ensure_inputfile)
        self.button_ensure_inputfile.pack(side="bottom", padx=5, pady=5)

        # ---------------- 向frame_choose_sample中填充部件

        self.frame_choose_reference_sample = ttk.Frame(self.frame_choose_sample)
        self.frame_choose_reference_sample.pack(side="top", padx=5, pady=5, fill="x")
        self.label_choose_reference_sample = ttk.Label(self.frame_choose_reference_sample,
                                                       text="select reference sample")
        self.label_choose_reference_sample.pack(side="left", padx=5, pady=5, anchor="e")
        self.var_choose_reference_sample = tk.StringVar()
        self.combobox_choose_reference_sample = ttk.Combobox(self.frame_choose_reference_sample,
                                                             textvariable=self.var_choose_reference_sample)
        self.combobox_choose_reference_sample.config(state='disabled')
        self.combobox_choose_reference_sample.pack(side="left", padx=5, pady=5)
        self.combobox_choose_reference_sample.bind("<<ComboboxSelected>>", self.get_choosen_reference_sample)

        self.frame_label_choose_sample = ttk.Frame(self.frame_choose_sample)  # for beauty
        self.frame_label_choose_sample.pack(side="top", padx=5, pady=5, fill="x")
        self.label_choose_sample = ttk.Label(self.frame_label_choose_sample, text="select the samples to be analysed:")
        self.label_choose_sample.pack(side="left", padx=5, pady=5, anchor="e")

        self.frame_choose_sample_temp = ttk.Frame(self.frame_choose_sample)
        self.frame_choose_sample_temp.pack(side="top", padx=5, pady=5, fill="both")
        # expand=True,
        self.canvas_choose_sample = tk.Canvas(self.frame_choose_sample_temp, scrollregion=(0, 0, 450, 450))
        self.vbar_choose_sample_temp = tk.Scrollbar(self.frame_choose_sample_temp)
        self.vbar_choose_sample_temp.pack(side="right", fill="y")
        self.vbar_choose_sample_temp.config(command=self.canvas_choose_sample.yview)
        self.canvas_choose_sample.config(height=400, width=200)
        self.canvas_choose_sample.config(yscrollcommand=self.vbar_choose_sample_temp.set)
        self.canvas_choose_sample.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.canvas_choose_sample.bind("<MouseWheel>", self.canvas_choose_sample_mousewheel)

        self.button_ensure_choose_sample = ttk.Button(self.frame_label_choose_sample, text="ok",
                                        command=self.get_chosen_samplesname,
                                        state="disabled")
        self.button_ensure_choose_sample.pack(side="right", padx=5, pady=5)

        self.frame_choose_colour = ttk.Frame(self.frame_choose_sample)
        self.frame_choose_colour.pack(side="bottom", fill='x', padx=5, pady=5)
        self.label_choose_colour = ttk.Label(self.frame_choose_colour, text="choose channel's colour:")
        self.label_choose_colour.pack(side="left", padx=5, pady=5)

        self.var_channel_colour = tk.StringVar()
        # self.list_all_channel_colour = self.get_channel_colour()
        self.combobox_choose_colour = ttk.Combobox(self.frame_choose_colour, textvariable=self.var_channel_colour)
        # self.combobox_choose_colour["values"] = self.list_all_channel_colour
        self.combobox_choose_colour.config(state='disabled')
        self.combobox_choose_colour.pack(side="left", padx=5, pady=5)
        self.combobox_choose_colour.bind("<<ComboboxSelected>>", self.get_choosen_channel_colour)

        # ---------------- 向frame_replicates中填充部件----------------------------------------------
        self.frame_if_replicates = ttk.Frame(self.frame_replicates)
        self.frame_if_replicates.pack(side="top", fill="x", padx=5, pady=5)

        self.label_if_replicates = ttk.Label(self.frame_if_replicates, text="number of replicate group")
        self.label_if_replicates.pack(side="left", padx=5, pady=5)
        self.var_group_number_replicates = tk.IntVar()
        self.combobox_group_number_replicates = ttk.Combobox(self.frame_if_replicates,
                                                             textvariable=self.var_group_number_replicates)
        # 下拉列表没有command函数（方法)。
        # 下拉列表的虚拟事件是 "<<ComboboxSelected>>"
        self.combobox_group_number_replicates.config(state='disabled')
        self.combobox_group_number_replicates.pack(side="left", padx=5, pady=5)
        self.combobox_group_number_replicates.bind("<<ComboboxSelected>>", self.get_if_replicates)

        self.frame_label_choose_replicates = ttk.Frame(self.frame_replicates)
        self.frame_label_choose_replicates.pack(side="top", fill="x", padx=5, pady=5)
        self.label_choose_replicates = ttk.Label(self.frame_label_choose_replicates,
                                                 text="choose the group of replicates:")
        self.label_choose_replicates.pack(side="left", padx=5, pady=5)

        self.frame_group_choose_replicates = ttk.Frame(self.frame_replicates)
        self.frame_group_choose_replicates.pack(side="top", fill="x", padx=5)
        self.label_group_choose_replicates = ttk.Label(self.frame_group_choose_replicates, text="group")
        self.label_group_choose_replicates.pack(side="left", padx=5)
        self.button_ensure_choose_replicates = ttk.Button(self.frame_group_choose_replicates, text="ok",
                                                          command=self.get_replicates_groups, state="disabled")
        self.button_ensure_choose_replicates.pack(side="right", padx=5)

        self.frame_choose_replicates = ttk.Frame(self.frame_replicates, relief="sunken", height=200)
        self.frame_choose_replicates.pack(expand=True, side="top", fill="x", padx=5, pady=5)
        self.canvas_choose_replicates = tk.Canvas(self.frame_choose_replicates, scrollregion=(0, 0, 250, 250))
        # scrollregion 指定 Canvas 可以被滚动的范围   该选项的值是一个 4 元组（x1, y1, x2, y2）表示的矩形
        self.vbar_choose_replicates = tk.Scrollbar(self.frame_choose_replicates)
        self.vbar_choose_replicates.pack(side="right", fill="y")
        self.vbar_choose_replicates.config(command=self.canvas_choose_replicates.yview)
        self.canvas_choose_replicates.config(width=200, height=200)
        self.canvas_choose_replicates.config(yscrollcommand=self.vbar_choose_replicates.set)
        self.canvas_choose_replicates.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.canvas_choose_replicates.bind("<MouseWheel>", self.canvas_choose_replicates_mousewheel)

        self.frame_input_replicates_name = ttk.Frame(self.frame_replicates)
        self.frame_input_replicates_name.pack(expand=True, side="top", fill="x", padx=5, pady=5)
        self.label_input_replicates_name = ttk.Label(self.frame_input_replicates_name, text="input group's name")
        self.label_input_replicates_name.pack(side="left", padx=5, pady=5)
        self.button_ensure_input_replicates_name = ttk.Button(self.frame_input_replicates_name, text="ok",
                                                              state="disabled", command=self.get_replicates_group_name)
        self.button_ensure_input_replicates_name.pack(side="right", padx=5, pady=5)

        self.frame_replicates_name = ttk.Frame(self.frame_replicates, relief="sunken")
        self.frame_replicates_name.pack(expand=True, side="top", fill="x", padx=5, pady=5)
        self.canvas_replicates_name = tk.Canvas(self.frame_replicates_name, scrollregion=(0, 0, 250, 250))
        self.vbar_replicates_name = tk.Scrollbar(self.frame_replicates_name)
        self.vbar_replicates_name.pack(side="right", fill="y")
        self.vbar_replicates_name.config(command=self.canvas_replicates_name.yview)
        self.vbar_replicates_name_x = tk.Scrollbar(self.frame_replicates_name, orient="horizontal")
        self.vbar_replicates_name_x.pack(side="bottom", fill="x")
        self.vbar_replicates_name_x.config(command=self.canvas_replicates_name.xview)
        # self.canvas_replicates_name.config(width=200, height=300)
        self.canvas_replicates_name.config(width=200, height=200)
        self.canvas_replicates_name.config(yscrollcommand=self.vbar_replicates_name.set,
                                           xscrollcommand=self.vbar_replicates_name_x.set)
        self.canvas_replicates_name.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.canvas_replicates_name.bind("<MouseWheel>", self.canvas_replicates_name_mousewheel)
        for widget in self.canvas_replicates_name.winfo_children():
            widget.bind("<MouseWheel>", self.canvas_replicates_name_mousewheel)


if __name__ == "__main__":
    root = tk.Tk()  # 创建跟窗口对象
    root.geometry("1200x740+100+100")
    root.title("Frame_OverView")
    database = FrameOverview(master=root)  # the object of the class Database
    database.creatWidge()
    root.mainloop()
