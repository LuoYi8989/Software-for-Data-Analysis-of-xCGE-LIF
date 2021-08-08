import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import tkinter.scrolledtext
import tkinter.messagebox
import os
from database import Database
import datetime


class FrameParameter(ttk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.ANALYSIS_OPTIONS = ["GSL", "N glycans", "GAGs"]
        self.var_analysis_option = tk.StringVar()
        # self.var_analysis_option.set(self.ANALYSIS_OPTIONS[0])


        ## 获取一些默认参数
        self.read_default_in_referencewell_from_file()
        self.read_default_normalization_from_file()

        self.version_analysis_choice = None
        self.list_user_choose_referencewell = []
        self.normal_standard = None
        self.combobox_normal_standards = None

        self.creatWidge()

    def read_default_in_referencewell_from_file(self):
        """获取txt文件中默认的glycans in referencewell"""
        cwd = os.getcwd()

        # f_default_in_referencewell = open(cwd+"/default_in_referencewell.txt", mode="r")
        f_default_in_referencewell = open("default_in_referencewell.txt", mode="r")
        self.default_referencewell_glycanname = [i for i in f_default_in_referencewell.read().split(",")]
        f_default_in_referencewell.close()
        print(self.default_referencewell_glycanname)
        print(type(self.default_referencewell_glycanname))

    def read_default_normalization_from_file(self):
        """获取txt文件中默认的glycans for normalization"""
        cwd = os.getcwd()
        # f_default_normalizaton = open(cwd+"/default_normalization.txt", mode="r")
        f_default_normalizaton = open("default_normalization.txt", mode="r")
        self.default_normalizaton = f_default_normalizaton.read()
        f_default_normalizaton.close()
        print(self.default_normalizaton)
        print(type(self.default_normalizaton))

    def get_which_database(self, *args):
        """获得用户选择的数据库类型：GSL N-glycan GAGs, 并获取相应的版本 self.dict_database_version"""
        self.database = Database()
        self.dataframe_database = self.database.create_dataframe_from_csv(self.combobox_analysis_choice.get())

        self.all_version_analysis_choice = self.dataframe_database.sort_values(by="date", ascending=False).loc[:,
                                           "date"].unique().tolist()
        print(self.all_version_analysis_choice)
        self.dict_database_version = {}  # 存储所有version的dict {year1:[date], year2:[date]}
        for each in self.all_version_analysis_choice:  # -->int
            if each.year not in self.dict_database_version.keys():
                self.dict_database_version[each.year] = []
                self.dict_database_version[each.year].append(each)
            else:
                self.dict_database_version[each.year].append(each)
        print(self.dict_database_version)

        self.combobox_version_analysis_choice_year["values"] = list(self.dict_database_version.keys())
        self.combobox_version_analysis_choice_year.set(list(self.dict_database_version.keys())[0])
        self.combobox_version_analysis_choice.set(self.all_version_analysis_choice[0])
        self.button_reference_default.config(state="normal")
        self.combobox_reference_number.config(state="readonly")

        # 删除referencell_canvas原有子组件,以避免发生上次选择的glycan不在本次的数据库中的情况
        for widget in self.canvas_choose_reference.winfo_children():
            widget.destroy()



    def version_year_analysis_choice(self, *args):
        """database version的年份选择后，显示更详细的时间"""
        # self.var_version_analysis_choice_year

        print(self.var_version_analysis_choice_year.get())

        datelist = self.dict_database_version[self.var_version_analysis_choice_year.get()]
        self.combobox_version_analysis_choice["values"] = datelist
        # 默认当前database的最新版本
        self.combobox_version_analysis_choice.set(datelist[0])

        # 删除referencell_canvas原有子组件,以避免发生上次选择的glycan不在本次的数据库中的情况
        for widget in self.canvas_choose_reference.winfo_children():
            widget.destroy()

    def get_version_analysis_choice(self, *args):
        """获取选择的database's version  yyyy-mm-dd"""
        print(self.var_version_analysis_choice.get())
        # datetime.date(*map(int, self.var_version_analysis_choice.get().split('-')))  将str表示成date形式
        self.version_analysis_choice = datetime.date(*map(int, self.var_version_analysis_choice.get().split('-')))

        temp_dataframe_database = self.dataframe_database[
            self.dataframe_database["date"] == self.version_analysis_choice]
        self.all_glycanname_of_version = sorted(temp_dataframe_database["name_of_glycan"].unique().tolist())
        self.combobox_normal_standards["values"] = self.all_glycanname_of_version

        # 删除referencell_canvas原有子组件,以避免发生上次选择的glycan不在本次的数据库中的情况
        for widget in self.canvas_choose_reference.winfo_children():
            widget.destroy()

    def show_referencewell_choose_combobox(self, *args):
        self.get_version_analysis_choice()  # to get self.all_glycanname_of_version
        number = self.var_reference_number.get()

        # 先删除原有子组件
        for widget in self.canvas_choose_reference.winfo_children():
            widget.destroy()

        for i in range(number):
            frame_temp = tk.Frame(self.canvas_choose_reference)
            self.canvas_choose_reference.create_window((10, 20 + i * 30), window=frame_temp, anchor="w")
            label = tk.Label(frame_temp, text="Glycan %d:" % (i + 1))
            label.pack(side="left", padx=5)
            exec('self.v{} = tk.StringVar()'.format(i))
            exec('self.combobox_temp{} = ttk.Combobox(frame_temp, textvariable=self.v{})'.format(i, i))
            exec('self.combobox_temp{}["values"] = self.all_glycanname_of_version'.format(i))
            exec('self.combobox_temp{}.current(0)'.format(i))
            exec('self.combobox_temp{}.config(state="readonly")'.format(i))
            exec('self.combobox_temp{}.pack(side="left", padx=5)'.format(i))

    def default_referencewell_choose_combobox(self):
        number = len(self.default_referencewell_glycanname)
        self.combobox_reference_number.set(number)
        self.get_version_analysis_choice()  # to get self.all_glycanname_of_version

        # 先删除原有子组件
        for widget in self.canvas_choose_reference.winfo_children():
            widget.destroy()

        number = len(self.default_referencewell_glycanname)
        for i in range(number):
            frame_temp = tk.Frame(self.canvas_choose_reference)
            self.canvas_choose_reference.create_window((10, 20 + i * 30), window=frame_temp, anchor="w")
            label = tk.Label(frame_temp, text="Glycan %d:" % (i + 1))
            label.pack(side="left", padx=5)
            exec('self.v{} = tk.StringVar()'.format(i))
            exec('self.combobox_temp{} = ttk.Combobox(frame_temp, textvariable=self.v{})'.format(i, i))
            exec('self.combobox_temp{}["values"] = self.all_glycanname_of_version'.format(i))
            if self.default_referencewell_glycanname[i] in self.all_glycanname_of_version:
                exec('self.combobox_temp{}.set(self.default_referencewell_glycanname[{}])'.format(i, i))
            exec('self.combobox_temp{}.config(state="readonly")'.format(i))
            exec('self.combobox_temp{}.pack(side="left", padx=5)'.format(i))

    def canvas_choose_reference_mousewheel(self, event):
        """让canvas能够使用鼠标滚轮滑动"""
        self.canvas_choose_reference.yview_scroll(-1 * event.delta, "units")
        # self.canvas_choose_sample.yview_scroll(-1 * (event.delta / 120), "units")
        # 在 Windows 上，您绑定到<MouseWheel>并且需要除以event.delta120（或其他一些因素，具体取决于您希望滚动的速度）
        # 在 OSX 上，您绑定到<MouseWheel>并且您需要event.delta不加修改地使用

    def get_referencewell(self):
        self.list_user_choose_referencewell = []
        for i in range(self.var_reference_number.get()):
            exec('self.list_user_choose_referencewell.append(self.v{}.get())'.format(i))
            # 检查glycan的选择是否为空
            if self.list_user_choose_referencewell[-1] == "":
                tkinter.messagebox.showinfo(title="warning", message="Invalid glycan in the referencewell")
                return

        for i in range(self.var_reference_number.get()):
            exec('self.combobox_temp{}.config(state="disabled")'.format(i))
        print(self.list_user_choose_referencewell)  # [] is valid
        self.combobox_relnor.config(state='readonly')
        if self.var_reference_number.get() == 0:
            self.combobox_relnor["values"] = ["Relativization"]
        else:
            self.combobox_relnor["values"] = ["Normalization", "Relativization"]

        self.button_sure_choose_reference.config(state='disabled')

    def choose_normal_standards(self, *args):
        if self.combobox_relnor.get() == "Normalization":
            # self.v_normal_standards = tk.StringVar()
            # self.combobox_normal_standards = ttk.Combobox(self.frame_choose_normalrelat,
            #                                               textvariable=self.v_normal_standards)
            # self.combobox_normal_standards["values"] = self.all_glycanname
            # self.combobox_normal_standards.config(state="readonly")
            # self.combobox_normal_standards.pack(side="left", padx=5)
            # self.combobox_normal_standards.bind("<<ComboboxSelected>>", self.get_normal_standards)

            # self.combobox_relnor.config(state='disabled')
            self.combobox_normal_standards.config(state="readonly")
            if self.default_normalizaton in self.all_glycanname_of_version:
                self.combobox_normal_standards.set(self.default_normalizaton)
            self.get_normal_standards()
            self.combobox_normal_standards_as_referencewell.config(state="readonly")
            if self.var_reference_number.get() == 0:
                self.combobox_normal_standards_as_referencewell["values"] = ["no"]
            else:
                self.combobox_normal_standards_as_referencewell["values"] = ["yes", "no"]

        if self.combobox_relnor.get() == "Relativization":
            # self.combobox_relnor.config(state='disabled')
            self.normal_standard = None
            self.combobox_normal_standards.config(state="disabled")
            self.combobox_normal_standards_as_referencewell.config(state="disabled")



    def get_normal_standards(self, *args):
        print(self.combobox_normal_standards.get())
        self.normal_standard = self.combobox_normal_standards.get()
        # self.get_normal_standards_as_referencewell()  # 当改变standard，自动获取当前选择是否作为reference well

    def get_normal_standards_as_referencewell(self, *args):
        if self.combobox_normal_standards_as_referencewell.get() == "yes":
            self.list_user_choose_referencewell.append(self.normal_standard)
            self.list_user_choose_referencewell = list(set(self.list_user_choose_referencewell))  # 为了防止standard已经出现在referenwell里
        self.combobox_normal_standards.config(state='disabled')
        if self.combobox_normal_standards_as_referencewell.get() == "no":
            if self.normal_standard in self.list_user_choose_referencewell:
                self.list_user_choose_referencewell.remove(self.normal_standard)

        print(self.list_user_choose_referencewell)

    def get_default_normalization(self):  ### 加一个提示
        ### 获取用户输入的default_referencewell_glycanname
        self.default_normalizaton = self.entry_default_normalization.get()
        print(self.default_normalizaton)
        print(type(self.default_normalizaton))

        ### 将新的default_normalization写入文件，在下次打开app时可以读取上次的保存记录
        f_default_normalizaton = open("default_normalization.txt", mode="w")
        f_default_normalizaton.write(self.default_normalizaton)
        f_default_normalizaton.close()

    def get_default_referenwell(self):  ### 加一个提示

        ### 获取用户输入的default_referencewell_glycanname
        self.default_referencewell_glycanname = [i for i in self.entry_default_referenwell.get().split(",")]
        print(self.default_referencewell_glycanname)

        ### 将新的default_referencewell_glycanname写入文件，在下次打开app时可以读取上次的保存记录
        sep = ","
        f_default_in_referencewell = open("default_in_referencewell.txt", mode="w")
        f_default_in_referencewell.write(sep.join(self.default_referencewell_glycanname))
        f_default_in_referencewell.close()

    def creatWidge(self):
        """对应于GUI2中的self.frame_parameter = ttk.Frame(self.tab)"""
        self.frame_main = ttk.Frame(self, height=640, width=1020)
        self.frame_main.pack(fill="both", expand=True)
        self.frame_main.pack_propagate(0)
        # expand=True
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        self.frame_analysis_choice = ttk.Frame(self.frame_main, height=50)
        self.frame_analysis_choice.pack(side="top", fill="x", pady=10)
        self.label_analysis_choice = ttk.Label(self.frame_analysis_choice, text="Analyse for:").pack(side="left",
                                                                                                     padx=5)
        self.combobox_analysis_choice = ttk.Combobox(self.frame_analysis_choice, textvariable=self.var_analysis_option)
        self.combobox_analysis_choice["values"] = self.ANALYSIS_OPTIONS
        # self.combobox_analysis_choice.current(0)  # 设置初始显示值，值为元组['values']的下标
        self.combobox_analysis_choice.config(state='readonly')
        self.combobox_analysis_choice.pack(side="left", padx=5)
        self.combobox_analysis_choice.bind("<<ComboboxSelected>>", self.get_which_database)
        self.label_show_analysis_choice = ttk.Label(self.frame_analysis_choice, textvariable=self.var_analysis_option)
        self.label_show_analysis_choice.pack(side="right", anchor="w", padx=5)

        # self.all_version_analysis_choice = self.dataframe_database.sort_values(by="date", ascending=False).loc[:,
        #                                    "date"].unique().tolist()
        # print(self.all_version_analysis_choice)
        # self.dict_database_version = {}  # 存储所有version的dict {year1:[date], year2:[date]}
        # for each in self.all_version_analysis_choice:  # -->int
        #     if each.year not in self.dict_database_version.keys():
        #         self.dict_database_version[each.year] = []
        #         self.dict_database_version[each.year].append(each)
        #     else:
        #         self.dict_database_version[each.year].append(each)
        # print(self.dict_database_version)

        self.label_version_analysis_choice = ttk.Label(self.frame_analysis_choice,
                                                       text="choose the version of database:")
        self.label_version_analysis_choice.pack(side="left", padx=5, pady=5, anchor="e")

        self.var_version_analysis_choice_year = tk.IntVar()
        self.combobox_version_analysis_choice_year = ttk.Combobox(self.frame_analysis_choice, state="readonly", width=8,
                                                                  textvariable=self.var_version_analysis_choice_year)
        # self.combobox_version_analysis_choice_year["values"] = list(self.dict_database_version.keys())
        # self.get_version_analysis_choice()
        self.combobox_version_analysis_choice_year.pack(side="left", padx=5)
        self.combobox_version_analysis_choice_year.set("")
        self.combobox_version_analysis_choice_year.bind("<<ComboboxSelected>>", self.version_year_analysis_choice)
        # self.combobox_version_analysis_choice_year.set(list(self.dict_database_version.keys())[0])

        self.var_version_analysis_choice = tk.StringVar()
        self.combobox_version_analysis_choice = ttk.Combobox(self.frame_analysis_choice, state="readonly", width=12,
                                                             textvariable=self.var_version_analysis_choice)
        # self.combobox_version_analysis_choice["values"] = self.all_version_analysis_choice
        # self.get_version_analysis_choice()
        self.combobox_version_analysis_choice.pack(side="left", padx=5)
        self.combobox_version_analysis_choice.bind("<<ComboboxSelected>>", self.get_version_analysis_choice)
        # self.combobox_version_analysis_choice.set(self.all_version_analysis_choice[0])

        ttk.Separator(self.frame_main).pack(fill="x", pady=5)
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        self.frame_choose_reference_number = ttk.Frame(self.frame_main)
        self.frame_choose_reference_number.pack(side="top", fill="x", pady=10)

        self.label_reference_number = ttk.Label(self.frame_choose_reference_number,
                                                text="choose glycan number in the referencewell:")
        self.label_reference_number.pack(side="left", padx=5)
        self.var_reference_number = tk.IntVar()
        self.combobox_reference_number = ttk.Combobox(self.frame_choose_reference_number,
                                                      textvariable=self.var_reference_number, state="disabled")
        self.combobox_reference_number["values"] = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.combobox_reference_number.pack(side="left", padx=5)
        self.combobox_reference_number.set("")
        self.combobox_reference_number.bind("<<ComboboxSelected>>", self.show_referencewell_choose_combobox)
        self.button_reference_default = ttk.Button(self.frame_choose_reference_number, text="default",
                                                   command=self.default_referencewell_choose_combobox, state="disabled")
        self.button_reference_default.pack(side="left", padx=5)

        # --------------------------------------------------------------------------------------------------------------
        self.frame_choose_reference = ttk.Frame(self.frame_main)
        self.frame_choose_reference.pack(side="top", fill="x")

        self.canvas_choose_reference = tk.Canvas(self.frame_choose_reference,
                                                 height=180, scrollregion=(0, 0, 320, 320))
        vbar = tk.Scrollbar(self.frame_choose_reference)
        vbar.pack(side="right", fill="y")
        vbar.config(command=self.canvas_choose_reference.yview)
        self.canvas_choose_reference.config(width=300, height=180)
        self.canvas_choose_reference.config(yscrollcommand=vbar.set)
        self.canvas_choose_reference.pack(side="left", expand=True, fill="both", padx=5)
        self.canvas_choose_reference.bind("<MouseWheel>", self.canvas_choose_reference_mousewheel)
        # --------------------------------------------------------------------------------------------------------------
        self.frame_sure_choose_reference = ttk.Frame(self.frame_main)
        self.frame_sure_choose_reference.pack(side="top", fill="x")

        self.button_sure_choose_reference = ttk.Button(self.frame_sure_choose_reference, text="ok",
                                                       command=self.get_referencewell)  # 关联函数 确定用户选择的reference
        self.button_sure_choose_reference.pack(side="left", padx=5, pady=5)

        ttk.Separator(self.frame_main).pack(fill="x", pady=5)
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        self.frame_choose_normalrelat = ttk.Frame(self.frame_main)
        self.frame_choose_normalrelat.pack(side="top", fill="x")

        self.label_analysis_method = ttk.Label(self.frame_choose_normalrelat, text="Method of analysis:"). \
            pack(side="left", padx=5, pady=5)
        self.var_relnor = tk.StringVar()
        self.combobox_relnor = ttk.Combobox(self.frame_choose_normalrelat, textvariable=self.var_relnor)
        # 下拉列表没有command函数（方法)。
        # 下拉列表的虚拟事件是 "<<ComboboxSelected>>"
        self.combobox_relnor["values"] = ["Normalization", "Relativization"]
        # self.combobox_relnor.config(state='readonly')
        self.combobox_relnor.config(state='disabled')
        self.combobox_relnor.pack(side="left", padx=5, pady=5)
        self.combobox_relnor.bind("<<ComboboxSelected>>", self.choose_normal_standards)

        self.v_normal_standards = tk.StringVar()
        self.combobox_normal_standards = ttk.Combobox(self.frame_choose_normalrelat,
                                                      textvariable=self.v_normal_standards)
        # self.combobox_normal_standards["values"] = self.all_glycanname
        self.combobox_normal_standards.config(state="disabled")
        self.combobox_normal_standards.pack(side="left", padx=5)
        self.combobox_normal_standards.bind("<<ComboboxSelected>>", self.get_normal_standards)

        self.label_standards_as_referencewell = ttk.Label(self.frame_choose_normalrelat, text="in referencewell?")
        self.label_standards_as_referencewell.pack(side="left", padx=5)
        self.v_normal_standards_as_referencewell = tk.StringVar()
        self.combobox_normal_standards_as_referencewell = ttk.Combobox(self.frame_choose_normalrelat,
                                                                       textvariable=self.v_normal_standards_as_referencewell)
        # self.combobox_normal_standards["values"] = self.all_glycanname
        self.combobox_normal_standards_as_referencewell.config(state="disabled")
        self.combobox_normal_standards_as_referencewell.pack(side="left", padx=5)
        self.combobox_normal_standards_as_referencewell.bind("<<ComboboxSelected>>",
                                                             self.get_normal_standards_as_referencewell)

        ttk.Separator(self.frame_main).pack(fill="x", pady=5)

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        self.frame_default_normalization = ttk.Frame(self.frame_main)
        self.frame_default_normalization.pack(side="bottom", fill="x", pady=5)

        self.label_default_normalization = ttk.Label(self.frame_default_normalization,
                                                     text="default glycan for normalization:")
        self.label_default_normalization.pack(side="left", anchor="w", padx=5)

        self.var_default_normalization = tk.StringVar()
        self.entry_default_normalization = ttk.Entry(self.frame_default_normalization, width=20,
                                                     textvariable=self.var_default_normalization)
        self.entry_default_normalization.pack(side="left", anchor="w", padx=5)
        ## show default referencewell  # self.default_referencewell_glycanname is a list
        self.var_default_normalization.set(self.default_normalizaton)

        self.button_default_normalization = ttk.Button(self.frame_default_normalization, text="ok",
                                                       command=self.get_default_normalization)
        self.button_default_normalization.pack(side="right", anchor="w", padx=5)

        ttk.Separator(self.frame_main).pack(fill="x", pady=5, side="bottom")
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        self.frame_default_referenwell = ttk.Frame(self.frame_main)
        self.frame_default_referenwell.pack(side="bottom", fill="x", pady=5)

        self.label_default_referenwell = ttk.Label(self.frame_default_referenwell, text="default in referenwell:")
        self.label_default_referenwell.pack(side="left", anchor="w", padx=5)

        self.var_default_referenwell = tk.StringVar()
        self.entry_default_referenwell = ttk.Entry(self.frame_default_referenwell, width=70,
                                                   textvariable=self.var_default_referenwell)
        self.entry_default_referenwell.pack(side="left", anchor="w", padx=5)
        ## show default referencewell  # self.default_referencewell_glycanname is a list
        sep = ","
        self.var_default_referenwell.set(sep.join(self.default_referencewell_glycanname))

        self.button_default_referenwell = ttk.Button(self.frame_default_referenwell, text="ok",
                                                     command=self.get_default_referenwell)
        self.button_default_referenwell.pack(side="right", anchor="w", padx=5)

        ttk.Separator(self.frame_main).pack(fill="x", pady=5, side="bottom")


if __name__ == "__main__":
    root = tk.Tk()  # 创建跟窗口对象
    root.geometry("1200x740+100+100")
    root.title("Frame_Parameter")
    database = FrameParameter(master=root)  # the object of the class Database
    root.mainloop()
