"""go back 成功"""

import tkinter as tk
from tkinter import ttk
from frame_database import FrameDatabase
from frame_overview import FrameOverview
from frame_parameter import FrameParameter
from frame_analysed_data import FrameAnalysedData
from frame_figure import FrameFigure


class Application(tk.Frame):
    """一个经典的GUI程序类的写法"""

    def __init__(self, master=None):
        # 父类构造器如果不主动调用的话，他不会被自动调用，所以需要调用Frame初始化的方法
        super().__init__(master)  # master使Frame初始化时需传入的参数
        self.master = master  # 将app的master和root进行绑定
        self.pack()  # self本身就是一个组件，需要调用布局管理器

        self.HEIGHT, self.WIDTH = self.winfo_height(), self.winfo_width()
        print(self.HEIGHT, self.WIDTH)

        self.ANALYSIS_OPTIONS = ["GSL", "N glycans", "GAGs"]
        self.var_analysis_option = tk.StringVar()
        self.var_analysis_option.set(self.ANALYSIS_OPTIONS[0])

        self.flag_first_ananlysed_data = 1
        self.flag_first_figure = 1

        self.creatWidge()

    def show_frame_analysed_data(self):
        # 先删除原来的部件
        # for widget in self.frame_analysed_data.winfo_children():
        #     widget.destroy()
        # self.frame_analysed_data.destroy()

        if self.flag_first_ananlysed_data == 0: # 已经出现过frame_ananlysed_data
            try:
                self.tab.forget(4)
                self.tab.forget(6)
            except:
                pass

        self.frame_analysed_data = FrameAnalysedData(self.tab, raw_data=self.frame_overview.dataframe_all_raw_data,
                                                     selected_data=self.frame_overview.dict_selected_data,
                                                     analysis_option=self.frame_parameter.var_analysis_option.get(),
                                                     version_database=self.frame_parameter.version_analysis_choice,
                                                     reference_sample=self.frame_overview.reference_sample,
                                                     referencewell=self.frame_parameter.list_user_choose_referencewell,
                                                     nor_or_rel=self.frame_parameter.combobox_relnor.get(),
                                                     normal_standard=self.frame_parameter.combobox_normal_standards.get(), )

        self.flag_first_ananlysed_data = 0
        self.tab.insert(4, self.frame_analysed_data, text="Analysed Data")
        self.tab.select(self.frame_analysed_data)


    def show_frame_figure(self):
        if self.flag_first_figure == 0:  # 已经出现过frame_figure
            try:
                self.tab.forget(6)
            except:
                pass

        self.frame_figure = FrameFigure(self.tab, annotated_result=self.frame_analysed_data.annotated_result,
                                        nor_or_rel=self.frame_parameter.combobox_relnor.get(),
                                        dict_replicates_groups=self.frame_overview.dict_replicates_groups)
        self.tab.add(self.frame_figure, text="Figure")
        self.tab.select(self.frame_figure)
        self.flag_first_figure = 0

    def creatWidge(self):
        # 设置Notebook布局
        self.tab = ttk.Notebook(self, height=640, width=1020)
        # height=self.HEIGHT, width=self.WIDTH

        self.frame_database = FrameDatabase(self.tab)  # tab for database
        self.frame_database.creatWidge()
        self.tab.add(self.frame_database, text="Database")

        self.frame_overview = FrameOverview(self.tab)  # tab for overview
        self.frame_overview.creatWidge()
        self.tab.add(self.frame_overview, text="Overview")

        self.frame_parameter = FrameParameter(self.tab)  # tab for parameter
        self.tab.add(self.frame_parameter, text="Parameter")

        # self.frame_figure = ttk.Frame(self.tab)  # tab for figure t5
        # self.tab.add(self.frame_figure, text="Figure")

        self.frame_go_analysed_data = ttk.Frame(self.tab)
        self.tab.add(self.frame_go_analysed_data, text="go to Analysed Data")

        self.frame_go_figure = ttk.Frame(self.tab)
        self.tab.add(self.frame_go_figure, text="go to Figure")

        self.tab.pack(fill="both", expand=True)

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------------------------------------
        # Overview  t1表示是在self.frame_overview中的部件

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # Database  t2表示是在self.frame_database中的部件

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # Parameter  t3表示是在self.frame_parameter中的部件

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # FrameAnalysedData
        self.button_start_analysed_data = ttk.Button(self.frame_go_analysed_data, text="START",
                                                     command=self.show_frame_analysed_data)
        self.button_start_analysed_data.pack()

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # FrameFigure
        self.button_start_figure = ttk.Button(self.frame_go_figure, text="START",
                                              command=self.show_frame_figure)
        self.button_start_figure.pack()


if __name__ == '__main__':
    root = tk.Tk()  # 创建跟窗口对象
    root.geometry("1200x740+100+100")
    root.title("GUI")
    app = Application(master=root)
    root.mainloop()
