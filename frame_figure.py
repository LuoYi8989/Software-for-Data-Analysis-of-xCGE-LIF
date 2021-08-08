"""补全electropherogram scollregion长度已调, 调整图像长度 添加真实的electropherogram"""

import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter.messagebox
import numpy as np
import tkinter.colorchooser
import pandas as pd
import tkinter.filedialog


class FrameFigure(ttk.Frame):

    def __init__(self, master=None, annotated_result=None, nor_or_rel=None, dict_replicates_groups=None):
        super().__init__(master)

        # 从frame_analysed_data传过来的
        self.annotated_result = annotated_result
        # self.annotated_result.set_index(["mean_MTU"], inplace=True)
        print(self.annotated_result, "self.annotated_result")
        self.nor_or_rel = nor_or_rel
        self.dict_replicates_groups = dict_replicates_groups
        # 格式{'GH': ['G07_EG07.fsa', 'H07_EG08.fsa'], 'AB': ['A08_EG09.fsa', 'B08_EG10.fsa']} 或{}
        print("self.nor_or_rel:", self.nor_or_rel)
        print(self.dict_replicates_groups)

        self.min_diff_of_mean_MTU = self.culculate_min_diff_of_mean_MTU()
        # self.min_diff_of_mean_MTU = self.min_diff_of_mean_MTU//2
        print("self.min_diff_of_mean_MTU", self.min_diff_of_mean_MTU)
        # 用于electropherogram

        self.len_samples = len(self.annotated_result.columns.values.tolist()) - 2
        # 用于调节canvas scollregion的长度

        self.creatWidge()

    def canvas_choose_figure_mousewheel(self, event):
        """让canvas能够使用鼠标滚轮滑动"""
        self.canvas_choose_figure.yview_scroll(-1 * event.delta, "units")
        # self.canvas_choose_sample.yview_scroll(-1 * (event.delta / 120), "units")
        # 在 Windows 上，您绑定到<MouseWheel>并且需要除以event.delta120（或其他一些因素，具体取决于您希望滚动的速度）
        # 在 OSX 上，您绑定到<MouseWheel>并且您需要event.delta不加修改地使用

    def bound_to_canvas_choose_figure_mousewheel(self, event):
        self.canvas_choose_figure.bind_all("<MouseWheel>", self.canvas_choose_figure_mousewheel)

    def unbound_to_canvas_choose_figure_mousewheel(self, event):
        self.canvas_choose_figure.unbind_all("<MouseWheel>")

    def culculate_min_diff_of_mean_MTU(self):
        MTU = self.annotated_result["mean_MTU"].tolist()
        print(MTU)
        min_value = float('inf')
        for i in range(len(MTU) - 1):
            diff = abs(MTU[i + 1] - MTU[i])
            if diff < min_value:
                print("diff", diff)
                print("min_value", min_value)
                print("MTU[i + 1]", MTU[i + 1])
                print("MTU[i]", MTU[i])
                min_value = diff
        print(min_value)
        return min_value

    def get_annotation_bar_graph(self, *args):
        self.flag_annotation_bar_graph = self.combobox_annotation_bar_graph.get()
        if self.flag_annotation_bar_graph == "No":
            self.combobox_annotation_rotation_bar_graph.config(state="disabled")
        else:
            self.combobox_annotation_rotation_bar_graph.config(state="readonly")

    def get_legend_bar_graph(self, *args):
        self.legend_position_bar_graph = self.combobox_legend_bar_graph.get()

    def get_annotation_rotation_bar_graph(self, *args):
        self.annotation_rotation_bar_graph = self.combobox_annotation_rotation_bar_graph.get()

    def get_yticks_bar_graph(self):
        try:
            self.yticks_bar_graph = [int(i) for i in self.entry_yticks_bar_graph.get().split(",")]
        except:
            tkinter.messagebox.showinfo(title="warning", message="Invalid ticks of y axis")


    def get_x_length_bar_graph(self, *args):
        if self.combobox_x_length_bar_graph.get() != "normal":
            self.x_length_bar_graph = int(self.combobox_x_length_bar_graph.get())
        else:
            self.x_length_bar_graph = self.combobox_x_length_bar_graph.get()

    def choose_samples_bar_graph(self):
        # self.frame_choose_samples_bar_graph  self.canvas_choose_samples_bar_graph  self.annotated_result
        self.all_samples_name_bar_graph = self.annotated_result.columns.values.tolist()
        self.all_samples_name_bar_graph.pop(), self.all_samples_name_bar_graph.pop()
        print("self.all_samples_name_electropherogram")
        print(self.all_samples_name_bar_graph)

        for i, each in enumerate(self.all_samples_name_bar_graph):
            frame_temp = tk.Frame(self.canvas_choose_samples_bar_graph)
            self.canvas_choose_samples_bar_graph.create_window((5, 5 + i * 30), window=frame_temp, anchor="nw")
            label = tk.Label(frame_temp, text=each[:-7])
            label.pack(side="left")
            exec('self.v{} = tk.IntVar()'.format("bar_graph" + str(i)))
            exec('self.v{}.set(1)'.format("bar_graph" + str(i)))
            exec('radiobutton_r = tk.Radiobutton(frame_temp, text="Remain", variable=self.v{},value=1)'.format("bar_graph" + str(i)))
            exec('radiobutton_c = tk.Radiobutton(frame_temp, text="Cancel", variable=self.v{},value=0)'.format("bar_graph" + str(i)))
            exec('radiobutton_r.pack(side="left")')
            exec('radiobutton_c.pack(side="left")')

        # self.choose_color_bar_electropherogram()

    def get_choose_samples_bar_graph(self):
        """获取用户选择的samples_of_bar_graph"""

        # self.all_samples_name_electropherogram用户选择所要显示sample之前所有的sample,
        # self.selected_samples_name_electropherogram 用户选择之后的samples
        self.selected_samples_name_bar_graph = []
        ### 获取用户所选的samples
        for i, each in enumerate(self.all_samples_name_bar_graph):
            loc = locals()
            exec('select_result = self.v{}.get()'.format("bar_graph" + str(i)))
            select_result = loc['select_result']
            print(select_result)

            if select_result == 1:
                self.selected_samples_name_bar_graph.append(each)
        print("self.selected_samples_name_bar_graph")
        print(self.selected_samples_name_bar_graph)

        self.choose_color_bar_bar_graph()

    def choose_color(self, event):
        color = tkinter.colorchooser.askcolor()
        # print(color)
        # print(color[1])
        print(event.widget)
        event.widget.configure(bg=color[1])
        event.widget.configure(text=color[1])

    def choose_color_bar_bar_graph(self):
        # self.frame_color_bar_bar_graph  self.canvas_color_bar_bar_graph  self.annotated_result

        # 先删除原有子组件
        for widget in self.canvas_color_bar_bar_graph.winfo_children():
            widget.destroy()

        self.canvas_color_bar_bar_graph.config(
            scrollregion=(0, 0, len(self.selected_samples_name_bar_graph) * 30,
                          len(self.selected_samples_name_bar_graph) * 30))

        for i, each in enumerate(self.selected_samples_name_bar_graph):
            frame_temp = tk.Frame(self.canvas_color_bar_bar_graph)
            self.canvas_color_bar_bar_graph.create_window((5, 5 + i * 30), window=frame_temp, anchor="nw")
            label = tk.Label(frame_temp, text=each[:-7])
            label.pack(side="left")
            exec('self.button_{}_bargraph = tk.Button(frame_temp, text="color")'.format(i))
            exec('self.button_{}_bargraph.pack(side="left", padx=5)'.format(i))
            # exec('self.button_{}_bargraph.config(command=self.choose_color)'.format(i))
            exec('self.button_{}_bargraph.bind("<Button-1>",self.choose_color)'.format(i))

    def show_bar_graph(self):
        # 先删除原有子组件
        for widget in self.frame_show_figure.winfo_children():
            widget.destroy()

        f = plt.figure()  # 创建图像窗口
        a_bar_graph = f.add_subplot(111)  # 添加子图:1行1列第1个

        ### 判断用户取值范围
        if self.var_MTU_start_bar_graph.get() > self.var_MTU_end_bar_graph.get():
            tkinter.messagebox.showinfo(title="warning", message="Invalid MTU range")
            return

        ### 获取一些参数  self.selected_samples_name_bar_graph
        self.get_annotation_bar_graph()
        self.get_legend_bar_graph()
        self.get_annotation_rotation_bar_graph()
        self.get_x_length_bar_graph()
        self.get_yticks_bar_graph()
        auto_color = 0
        color_list = []
        for i, each in enumerate(self.selected_samples_name_bar_graph):
            exec('color_list.append(self.button_{}_bargraph["text"])'.format(i))
        print(color_list)
        # if self.x_length_bar_graph == 20:
        #     pass
        # elif self.x_length_bar_graph == 30:
        #     self.canvas_show_figure_base.config(scrollregion=(0, 0, 1400, 200))
        # elif self.x_length_bar_graph == 40:
        #     self.canvas_show_figure_base.config(scrollregion=(0, 0, 2100, 200))
        # elif self.x_length_bar_graph == 50:
        #     self.canvas_show_figure_base.config(scrollregion=(0, 0, 2800, 200))

        if color_list == ["color" for i in range(len(color_list))]:
            auto_color = 1
        else:
            for each in color_list:
                if each == "color":
                    tkinter.messagebox.showinfo(title="warning", message="please choose color")
                    return

        ### 基础柱状图 根据用户所选范围截取有效数据 及所需展示的samples  self.selected_samples_name_bar_graph
        annotated_result = self.annotated_result[
            self.var_MTU_start_bar_graph.get() <= self.annotated_result["mean_MTU"]]
        annotated_result = annotated_result[annotated_result["mean_MTU"] <= self.var_MTU_end_bar_graph.get()]
        dataframe_plot = pd.DataFrame()
        for each in self.selected_samples_name_bar_graph:
            dataframe_plot[each] = annotated_result[each]
        # dataframe_plot = annotated_result.iloc[:, :-2]

        x_label = [str(i) for i in annotated_result["mean_MTU"].tolist()]  # mean_MTU
        legend_label = [i[:-7] for i in dataframe_plot.columns.values.tolist()]
        print("legend_label", legend_label)

        # 绘制
        if auto_color == 1:
            dataframe_plot.plot(kind='bar', ax=a_bar_graph)
        else:
            dataframe_plot.plot(kind='bar', ax=a_bar_graph, color=color_list)
        a_bar_graph.set_xlabel("migration time unit [MTU]")
        if self.nor_or_rel == "Normalization":
            a_bar_graph.set_ylabel("normalized signal intensity [nRFU]")
        elif self.nor_or_rel == "Relativization":
            a_bar_graph.set_ylabel("relative signal intensity [%]")
        plt.xticks(np.arange(len(x_label)), x_label)
        try:
            plt.yticks(self.yticks_bar_graph)
        except:
            tkinter.messagebox.showinfo(title="warning", message="Invalid ticks of y axis")
            return
        # a.set_xticks(x_label)  Failed to convert value(s) to axis units
        print(dataframe_plot)
        print(x_label)
        # 设置上右边框消失
        plt.gca().spines['top'].set_color('none')  # gca()获取当前坐标轴信息   .spines设置边框
        plt.gca().spines['right'].set_color('none')

        # 设置legend  https://www.jb51.net/article/191933.htm
        if self.legend_position_bar_graph == "none":
            print(a_bar_graph.legend_)
            print(type(a_bar_graph.legend_))
            a_bar_graph.legend_.remove()
        elif self.legend_position_bar_graph == "outer upper":
            a_position = a_bar_graph.get_position()  # （x0,y0,width,height）
            a_bar_graph.legend(bbox_to_anchor=(1.0, 1), loc="upper left", labels=legend_label, fontsize=8,
                               markerscale=0.8)
        elif self.legend_position_bar_graph == "outer lower":
            a_bar_graph.legend(bbox_to_anchor=(1.0, 0), loc="upper left", labels=legend_label, fontsize=8,
                               markerscale=0.8)
        else:
            a_bar_graph.legend(loc=self.legend_position_bar_graph, labels=legend_label, fontsize=8, markerscale=0.8,
                               framealpha=0.7)

        ### 是否有annotation
        if self.flag_annotation_bar_graph == "Yes":
            ### 添加标注
            text = annotated_result.iloc[:, -1].values.tolist()
            print("text")
            print(text)
            x = np.arange(len(x_label))
            y = dataframe_plot.max(axis=1).values.tolist()  # 每一行的最大值
            # a_bar_graph.set_ylim(0, max(y) + 0.1 * max(y))  # 稍微增加一下纵轴高度
            y_axis_max = plt.ylim()[1]  # 纵坐标轴最大值

            for index, each in enumerate(text):
                if each != '':
                    a_bar_graph.text(x[index], y_axis_max - 3, each, ha='center', va='bottom', fontsize=8,
                                     rotation=self.annotation_rotation_bar_graph, wrap=True)
                    a_bar_graph.plot([x[index], x[index], ], [y[index], y_axis_max - 3, ], 'k--', linewidth=0.8)
                    print('each', each)
                    print('xy', (x[index], y[index]))

        ### 增加x轴的长度
        if self.x_length_bar_graph != "normal":
            # change x internal size
            plt.gca().margins(x=0)  # 添加到轴的每个限制的填充是* margin *乘以数据间隔。 所有输入参数都必须是[0，1]范围内的浮点数
            # margins x轴和y轴分别具有特定的边距值。 这些不能与位置参数一起使用，但可以单独使用，例如仅在y轴上进行更改。
            plt.gcf().canvas.draw()
            # set size
            maxsize = self.x_length_bar_graph
            m = 0.2
            # N = len(x_label)
            N = len(self.annotated_result["mean_MTU"])
            s = maxsize / plt.gcf().dpi * N + 2 * m  # dpi 像素  s：x轴的长度 inches
            print("s:", s)
            print("plt.gcf().dpi:", plt.gcf().dpi)
            margin = m / plt.gcf().get_size_inches()[0]
            print("plt.gcf().get_size_inches()[0]:", plt.gcf().get_size_inches()[0])
            print("plt.gcf().get_size_inches()[1]:", plt.gcf().get_size_inches()[1])
            # 返回图形的当前大小（以英寸为单位)The size (width, height) of the figure in inches.
            plt.gcf().subplots_adjust(left=margin, right=1. - margin)
            plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

            self.canvas_show_figure_base.config(scrollregion=(0, 0, str(s + 10) + 'i', str(s) + 'i'))
            # 改变画布长度

        plt.show()

        # 把绘制的图形显示到tkinter窗口上
        self.canvas_show_figure = FigureCanvasTkAgg(f, self.frame_show_figure)
        self.canvas_show_figure.draw()
        self.canvas_show_figure.get_tk_widget().pack(side="top", fill="both", expand=1)

        # 把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
        toolbar = NavigationToolbar2Tk(self.canvas_show_figure,
                                       self.frame_show_figure)  # matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
        toolbar.update()
        self.canvas_show_figure._tkcanvas.pack(side="top", fill="both", expand=1)
        # get_tk_widget()得到的就是_tkcanvas

    def get_annotation_mean_SD(self, *args):
        self.flag_annotation_mean_SD = self.combobox_annotation_mean_SD.get()
        if self.flag_annotation_mean_SD == "No":
            self.combobox_annotation_rotation_mean_SD.config(state="disabled")
        else:
            self.combobox_annotation_rotation_mean_SD.config(state="readonly")

    def get_annotation_rotation_mean_SD(self, *args):
        self.annotation_rotation_mean_SD = self.combobox_annotation_rotation_mean_SD.get()

    def get_legend_mean_SD(self, *args):
        self.legend_position_mean_SD = self.combobox_legend_mean_SD.get()

    def get_yticks_mean_SD(self):
        try:
            self.yticks_mean_SD = [int(i) for i in self.entry_yticks_mean_SD.get().split(",")]
        except:
            tkinter.messagebox.showinfo(title="warning", message="Invalid ticks of y axis")

    def get_x_length_mean_SD(self, *args):
        if self.combobox_x_length_mean_SD.get() != "normal":
            self.x_length_mean_SD = int(self.combobox_x_length_mean_SD.get())
        else:
            self.x_length_mean_SD = self.combobox_x_length_mean_SD.get()

    def choose_groups_mean_SD(self):
        # self.frame_choose_samples_bar_graph  self.canvas_choose_samples_bar_graph  self.annotated_result
        self.all_group_name_mean_SD = list(self.dict_replicates_groups.keys())


        for i, each in enumerate(self.all_group_name_mean_SD):
            frame_temp = tk.Frame(self.canvas_choose_groups_mean_SD)
            self.canvas_choose_groups_mean_SD.create_window((5, 5 + i * 30), window=frame_temp, anchor="nw")
            label = tk.Label(frame_temp, text=each)
            label.pack(side="left")
            exec('self.v{} = tk.IntVar()'.format("mean_SD" + str(i)))
            exec('self.v{}.set(1)'.format("mean_SD" + str(i)))
            exec('radiobutton_r = tk.Radiobutton(frame_temp, text="Remain", variable=self.v{},value=1)'.format("mean_SD" + str(i)))
            exec('radiobutton_c = tk.Radiobutton(frame_temp, text="Cancel", variable=self.v{},value=0)'.format("mean_SD" + str(i)))
            exec('radiobutton_r.pack(side="left")')
            exec('radiobutton_c.pack(side="left")')

        # self.choose_color_bar_electropherogram()

    def get_choose_groups_mean_SD(self):
        """获取用户选择的groups_of_mean_SD"""

        # self.all_group_name_mean_SD用户选择所要显示group之前所有的group,
        # self.selected_groups_mean_SD 用户选择之后的group
        self.selected_groups_mean_SD = []
        ### 获取用户所选的samples
        for i, each in enumerate(self.all_group_name_mean_SD):
            loc = locals()
            exec('select_result = self.v{}.get()'.format("mean_SD" + str(i)))
            select_result = loc['select_result']
            print(select_result)

            if select_result == 1:
                self.selected_groups_mean_SD.append(each)

        self.choose_color_bar_mean_SD()

    def choose_color_bar_mean_SD(self):
        # self.frame_color_bar_mean_SD  self.canvas_color_bar_mean_SD  self.dict_replicates_groups

        # 先删除原有子组件
        for widget in self.canvas_color_bar_mean_SD.winfo_children():
            widget.destroy()

        self.canvas_color_bar_mean_SD.config(
            scrollregion=(0, 0, len(self.selected_groups_mean_SD) * 30,
                          len(self.selected_groups_mean_SD) * 30))

        for i, each in enumerate(self.selected_groups_mean_SD):
            frame_temp = tk.Frame(self.canvas_color_bar_mean_SD)
            self.canvas_color_bar_mean_SD.create_window((5, 5 + i * 30), window=frame_temp, anchor="nw")
            label = tk.Label(frame_temp, text=each)
            label.pack(side="left")
            exec('self.button_{}_mean_SD = tk.Button(frame_temp, text="color")'.format(i))
            exec('self.button_{}_mean_SD.pack(side="left", padx=5)'.format(i))
            # exec('self.button_{}_bargraph.config(command=self.choose_color)'.format(i))
            exec('self.button_{}_mean_SD.bind("<Button-1>",self.choose_color)'.format(i))

    def show_mean_SD(self):
        # self.annotated_result
        # self.dict_replicates_groups  {'GH': ['G07_EG07.fsa', 'H07_EG08.fsa'], 'AB': ['A08_EG09.fsa', 'B08_EG10.fsa']}

        ### 判断用户取值范围
        if self.var_MTU_start_mean_SD.get() > self.var_MTU_end_mean_SD.get():
            tkinter.messagebox.showinfo(title="warning", message="Invalid MTU range")
            return

        ### 获取一些参数
        self.get_annotation_mean_SD()
        self.get_legend_mean_SD()
        self.get_annotation_rotation_mean_SD()
        self.get_yticks_mean_SD()
        self.get_x_length_mean_SD()
        color_list = []
        auto_color = 0
        for i, each in enumerate(self.selected_groups_mean_SD):
            exec('color_list.append(self.button_{}_mean_SD["text"])'.format(i))
        print(color_list)
        # if self.x_length_mean_SD == 20:
        #     pass
        # elif self.x_length_mean_SD == 30:
        #     self.canvas_show_figure_base.config(scrollregion=(0, 0, 1400, 200))
        # elif self.x_length_mean_SD == 40:
        #     self.canvas_show_figure_base.config(scrollregion=(0, 0, 2100, 200))
        # elif self.x_length_mean_SD == 50:
        #     self.canvas_show_figure_base.config(scrollregion=(0, 0, 2800, 200))

        if color_list == ["color" for i in range(len(color_list))]:
            auto_color = 1
        else:
            for each in color_list:
                if each == "color":
                    tkinter.messagebox.showinfo(title="warning", message="please choose color")
                    return

        ### 处理数据 求均值和标准差 self.dict_dataframe_replicates_groups
        self.dict_dataframe_replicates_groups = {}  # {sample_name:dataframe, sample_name:dataframe...}
        for each in self.dict_replicates_groups.items():
            samples = [i + "_Height" for i in each[1]]

            # 根据self.dict_replicates_groups 获取相应组的dataframe
            dataframe_temp = self.annotated_result.loc[:, samples]
            dataframe_temp["mean_MTU"] = self.annotated_result["mean_MTU"]
            dataframe_temp["annotate"] = self.annotated_result["annotate"]
            # 截取MTU范围
            dataframe_temp = dataframe_temp[dataframe_temp["mean_MTU"] <= self.var_MTU_end_mean_SD.get()]
            dataframe_temp = dataframe_temp[dataframe_temp["mean_MTU"] >= self.var_MTU_start_mean_SD.get()]
            self.mean_SD_annotation = dataframe_temp["annotate"].tolist()
            # 计算均值和标准差
            dataframe_temp["mean_height"] = dataframe_temp.iloc[:, :-2].mean(axis=1)  # 最后两列是"mean_MTU""annotate"
            dataframe_temp["std"] = dataframe_temp.iloc[:, :-3].std(axis=1)  # 最后三列是"mean_MTU""annotate" "mean_height"
            print(each[0])
            print(dataframe_temp)
            self.dict_dataframe_replicates_groups[each[0]] = dataframe_temp
        print(self.dict_dataframe_replicates_groups)

        ### 创建新的做图dataframe columns=["mean_MTU", group_name1, group_name2...] self.selected_groups_mean_SD
        self.dataframe_replicates_groups_mean = pd.DataFrame()
        self.dataframe_replicates_groups_std = pd.DataFrame()
        self.dataframe_replicates_groups_meanstd = pd.DataFrame()  # 存放std+mean的值 将来出图std的真实高度
        for each in self.dict_dataframe_replicates_groups.items():
            self.dataframe_replicates_groups_mean["mean_MTU"] = each[1]["mean_MTU"]
            self.dataframe_replicates_groups_std["mean_MTU"] = each[1]["mean_MTU"]
            if each[0] in self.selected_groups_mean_SD:  # 用户选择的groups
                self.dataframe_replicates_groups_mean[each[0]] = each[1]["mean_height"]
                self.dataframe_replicates_groups_std[each[0]] = each[1]["std"]
                self.dataframe_replicates_groups_meanstd[each[0]] = each[1]["mean_height"] + each[1]["std"]

        print(self.dataframe_replicates_groups_mean)
        print(self.dataframe_replicates_groups_std)
        print(self.dataframe_replicates_groups_meanstd)

        ### 画图
        # 先删除原有子组件
        for widget in self.frame_show_figure.winfo_children():
            widget.destroy()

        f = plt.figure()  # 创建图像窗口
        a_mean_SD = f.add_subplot(111)  # 添加子图:1行1列第1个

        x_label = [str(i) for i in self.dataframe_replicates_groups_mean["mean_MTU"].tolist()]  # mean_MTU
        x = np.arange(len(x_label))  # 0,1,2,3...
        legend_label = self.dataframe_replicates_groups_mean.columns.values.tolist()[1:]
        num_group = len(legend_label)  # 计算有多少个列
        total_width = 1.4  # 设置每组总宽度
        width = total_width / num_group  # #求出每组每列宽度

        # 绘制柱形图 mean
        for i in range(num_group):
            x_value = x * 2 + i * width
            y_mean_value = self.dataframe_replicates_groups_mean[legend_label[i]].tolist()
            y_std_value = self.dataframe_replicates_groups_mean[legend_label[i]] + self.dataframe_replicates_groups_std[
                legend_label[i]]
            y_std_value = y_std_value.tolist()
            print(legend_label[i])
            print(y_mean_value)
            print(y_std_value)
            if auto_color == 1:
                a_mean_SD.bar(x_value, y_mean_value, width=width)
            else:
                a_mean_SD.bar(x_value, y_mean_value, width=width, color=color_list[i])

        x_label_position = x * 2 + 1 / 2  # 设置x轴刻度标签位置
        plt.xticks(x_label_position, x_label, rotation=-90)
        try:
            plt.yticks(self.yticks_mean_SD)
        except:
            tkinter.messagebox.showinfo(title="warning", message="Invalid ticks of y axis")
            return
        a_mean_SD.set_xlabel("migration time unit [MTU]")
        if self.nor_or_rel == "Normalization":
            a_mean_SD.set_ylabel("normalized signal intensity [nRFU]")
        elif self.nor_or_rel == "Relativization":
            a_mean_SD.set_ylabel("relative signal intensity [%]")
        if self.legend_position_mean_SD == "none":
            # 本身的图就没有legend
            pass
            # print(a_mean_SD.legend_)
            # print(type(a_mean_SD.legend_))
            # a_mean_SD.legend_.remove()
        elif self.legend_position_mean_SD == "outer upper":
            a_position = a_mean_SD.get_position()  # （x0,y0,width,height）
            a_mean_SD.legend(bbox_to_anchor=(1.0, 1), loc="upper left", labels=legend_label, fontsize=8,
                             markerscale=0.8)
        elif self.legend_position_mean_SD == "outer lower":
            a_mean_SD.legend(bbox_to_anchor=(1.0, 0), loc="upper left", labels=legend_label, fontsize=8,
                             markerscale=0.8)
        else:
            a_mean_SD.legend(loc=self.legend_position_mean_SD, labels=legend_label, fontsize=8, markerscale=0.8,
                             framealpha=0.7)

        # 绘制std
        print(round(width / 4, 1))
        for i in range(num_group):
            x_value = x * 2 + i * width
            y_mean_value = self.dataframe_replicates_groups_mean[legend_label[i]].tolist()
            y_std_value = self.dataframe_replicates_groups_mean[legend_label[i]] + self.dataframe_replicates_groups_std[
                legend_label[i]]
            y_std_value = y_std_value.tolist()
            for j in range(len(x_label)):
                # std横线
                a_mean_SD.plot([x_value[j] - width / 3, x_value[j] + width / 3, ], [y_std_value[j], y_std_value[j], ],
                               color="black", linewidth=0.8)
                # std竖线
                a_mean_SD.plot([x_value[j], x_value[j], ], [y_mean_value[j], y_std_value[j], ], color="black",
                               linewidth=0.8)

        ### 是否有annotation
        if self.flag_annotation_mean_SD == "Yes":
            y = self.dataframe_replicates_groups_meanstd.max(axis=1).values.tolist()  # 每一行的最大值
            # a_mean_SD.set_ylim(0, max(y) + 0.1 * max(y))  # 稍微增加一下纵轴高度
            y_axis_max = plt.ylim()[1]  # 纵坐标轴最大值

            for index, i in enumerate(x_label_position):
                if self.mean_SD_annotation[index] != '':
                    a_mean_SD.text(i, y_axis_max - 2, self.mean_SD_annotation[index], ha='center', va='bottom',
                                   fontsize=8,
                                   wrap=True, rotation=self.annotation_rotation_mean_SD)
                    a_mean_SD.plot([i, i, ], [y[index], y_axis_max - 2, ], 'k--', linewidth=0.8)

        # 设置上右边框消失
        plt.gca().spines['top'].set_color('none')  # gca()获取当前坐标轴信息   .spines设置边框
        plt.gca().spines['right'].set_color('none')  # 把绘制的图形显示到tkinter窗口上

        ### 增加x轴的长度
        if self.x_length_mean_SD != "normal":
            # change x internal size
            plt.gca().margins(x=0)  # 添加到轴的每个限制的填充是* margin *乘以数据间隔。 所有输入参数都必须是[0，1]范围内的浮点数
            # margins x轴和y轴分别具有特定的边距值。 这些不能与位置参数一起使用，但可以单独使用，例如仅在y轴上进行更改。
            plt.gcf().canvas.draw()
            # set size
            maxsize = self.x_length_mean_SD
            m = 0.2
            # N = len(x_label)
            N = len(self.annotated_result["mean_MTU"])
            s = maxsize / plt.gcf().dpi * N + 2 * m  # dpi 像素  s：x轴的长度 inches
            print("s:", s)
            print("plt.gcf().dpi:", plt.gcf().dpi)
            margin = m / plt.gcf().get_size_inches()[0]
            print("plt.gcf().get_size_inches()[0]:", plt.gcf().get_size_inches()[0])
            print("plt.gcf().get_size_inches()[1]:", plt.gcf().get_size_inches()[1])
            # 返回图形的当前大小（以英寸为单位)The size (width, height) of the figure in inches.
            plt.gcf().subplots_adjust(left=margin, right=1. - margin)
            plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

            self.canvas_show_figure_base.config(scrollregion=(0, 0, str(s + 10) + 'i', str(s) + 'i'))
            # 改变画布长度

        plt.show()

        # 把绘制的图形显示到tkinter窗口上
        self.canvas_show_figure = FigureCanvasTkAgg(f, self.frame_show_figure)
        self.canvas_show_figure.draw()
        self.canvas_show_figure.get_tk_widget().pack(side="top", fill="both", expand=1)

        # 把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
        toolbar = NavigationToolbar2Tk(self.canvas_show_figure,
                                       self.frame_show_figure)  # matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
        toolbar.update()
        self.canvas_show_figure._tkcanvas.pack(side="top", fill="both", expand=1)
        # get_tk_widget()得到的就是_tkcanvas

        self.button_mean_SD_download_SD.config(state="normal")
        self.button_mean_SD_download_mean.config(state="normal")
        self.button_mean_SD_download.config(state="normal")

    def mean_SD_download_mean(self):
        filename = tkinter.filedialog.asksaveasfilename()

        if not filename.endswith('.xls'):
            self.dataframe_replicates_groups_mean.to_excel(filename + '.xls')
        else:
            self.dataframe_replicates_groups_mean.to_excel(filename)

    def mean_SD_download_SD(self):
        filename = tkinter.filedialog.asksaveasfilename()

        if not filename.endswith('.xls'):
            self.dataframe_replicates_groups_std.to_excel(filename + '.xls')
        else:
            self.dataframe_replicates_groups_std.to_excel(filename)

    def mean_SD_download(self):
        # self.annotated_result # "_Height"
        # self.dict_replicates_groups  {'GH': ['G07_EG07.fsa', 'H07_EG08.fsa'], 'AB': ['A08_EG09.fsa', 'B08_EG10.fsa']}

        self.dataframe_replicates_groups_annotation = pd.DataFrame()
        self.dataframe_replicates_groups_annotation["mean_MTU"] = self.annotated_result["mean_MTU"]
        for each in self.dict_replicates_groups.items():
            # each[0] = 'GH' each[1]=['G07_EG07.fsa', 'H07_EG08.fsa']
            for sample in each[1]:  # sample='G07_EG07.fsa'
                self.dataframe_replicates_groups_annotation[each[0]+"_"+sample] = self.annotated_result[sample+"_Height"]
        self.dataframe_replicates_groups_annotation["annotate"] = self.annotated_result["annotate"]
        print(self.dataframe_replicates_groups_annotation)

        filename = tkinter.filedialog.asksaveasfilename()

        if not filename.endswith('.xls'):
            self.dataframe_replicates_groups_annotation.to_excel(filename + '.xls')
        else:
            self.dataframe_replicates_groups_annotation.to_excel(filename)



    def get_annotation_electropherogram(self, *args):
        self.flag_annotation_electropherogram = self.combobox_annotation_electropherogram.get()
        if self.flag_annotation_electropherogram == "No":
            self.combobox_annotation_rotation_electropherogram.config(state="disabled")
        else:
            self.combobox_annotation_rotation_electropherogram.config(state="readonly")

    def get_annotation_rotation_electropherogram(self, *args):
        self.annotation_rotation_electropherogram = self.combobox_annotation_rotation_electropherogram.get()

    def get_legend_electropherogram(self, *args):
        self.legend_position_electropherogram = self.combobox_legend_electropherogram.get()

    def get_yticks_electropherogram(self):
        try:
            self.yticks_electropherogram = [int(i) for i in self.entry_yticks_electropherogram.get().split(",")]
        except:
            tkinter.messagebox.showinfo(title="warning", message="Invalid ticks of y axis")

    def get_x_length_electropherogram(self, *args):
        if self.combobox_x_length_electropherogram.get() != "normal":
            self.x_length_electropherogram = int(self.combobox_x_length_electropherogram.get())
        else:
            self.x_length_electropherogram = self.combobox_x_length_electropherogram.get()

    def choose_samples_electropherogram(self):
        # self.frame_choose_samples_electropherogram  self.canvas_choose_samples_electropherogram  self.annotated_result
        self.all_samples_name_electropherogram = self.annotated_result.columns.values.tolist()
        self.all_samples_name_electropherogram.pop(), self.all_samples_name_electropherogram.pop()
        print("self.all_samples_name_electropherogram")
        print(self.all_samples_name_electropherogram)

        for i, each in enumerate(self.all_samples_name_electropherogram):
            frame_temp = tk.Frame(self.canvas_choose_samples_electropherogram)
            self.canvas_choose_samples_electropherogram.create_window((5, 5 + i * 30), window=frame_temp, anchor="nw")
            label = tk.Label(frame_temp, text=each[:-7])
            label.pack(side="left")
            exec('self.v{} = tk.IntVar()'.format(i))
            exec('self.v{}.set(1)'.format(i))
            exec('radiobutton_r = tk.Radiobutton(frame_temp, text="Remain", variable=self.v{},value=1)'.format(i))
            exec('radiobutton_c = tk.Radiobutton(frame_temp, text="Cancel", variable=self.v{},value=0)'.format(i))
            exec('radiobutton_r.pack(side="left")')
            exec('radiobutton_c.pack(side="left")')

        # self.choose_color_bar_electropherogram()

    def get_choose_samples_electropherogram(self):
        """获取用户选择的samples_of_electropherogram"""

        # self.all_samples_name_electropherogram用户选择所要显示sample之前所有的sample,
        # self.selected_samples_name_electropherogram 用户选择之后的samples
        self.selected_samples_name_electropherogram = []
        ### 获取用户所选的samples
        for i, each in enumerate(self.all_samples_name_electropherogram):
            loc = locals()
            exec('select_result = self.v{}.get()'.format(i))
            select_result = loc['select_result']
            print(select_result)

            if select_result == 1:
                self.selected_samples_name_electropherogram.append(each)
        print("self.selected_samples_name_electropherogram")
        print(self.selected_samples_name_electropherogram)

        self.choose_color_bar_electropherogram()

    def choose_color_bar_electropherogram(self):
        # self.frame_color_bar_electropherogram  self.canvas_color_bar_electropherogram  self.annotated_result
        # self.all_samples_name_electropherogram

        # 先删除原有子组件
        for widget in self.canvas_color_bar_electropherogram.winfo_children():
            widget.destroy()

        self.canvas_color_bar_electropherogram.config(
            scrollregion=(0, 0, len(self.selected_samples_name_electropherogram) * 30,
                          len(self.selected_samples_name_electropherogram) * 30))

        for i, each in enumerate(self.selected_samples_name_electropherogram):
            frame_temp = tk.Frame(self.canvas_color_bar_electropherogram)
            self.canvas_color_bar_electropherogram.create_window((5, 5 + i * 30), window=frame_temp, anchor="nw")
            label = tk.Label(frame_temp, text=each[:-7])
            label.pack(side="left")
            exec('self.button_{}_electropherogram = tk.Button(frame_temp, text="color")'.format(i))
            exec('self.button_{}_electropherogram.pack(side="left", padx=5)'.format(i))
            # exec('self.button_{}_bargraph.config(command=self.choose_color)'.format(i))
            exec('self.button_{}_electropherogram.bind("<Button-1>",self.choose_color)'.format(i))

    def show_electropherogram(self):

        ### 判断用户取值范围
        if self.var_MTU_start_electropherogram.get() > self.var_MTU_end_electropherogram.get():
            tkinter.messagebox.showinfo(title="warning", message="Invalid MTU range")
            return

        ### 获取一些参数
        self.get_annotation_electropherogram()
        self.get_legend_electropherogram()
        self.get_annotation_rotation_electropherogram()
        self.get_yticks_electropherogram()
        self.get_x_length_electropherogram()
        color_list = []
        auto_color = 0
        for i, each in enumerate(self.selected_samples_name_electropherogram):
            exec('color_list.append(self.button_{}_electropherogram["text"])'.format(i))
        print(color_list)
        # if self.x_length_electropherogram == 20:
        #     pass
        # elif self.x_length_electropherogram == 30:
        #     self.canvas_show_figure_base.config(scrollregion=(0, 0, 1400, 200))
        # elif self.x_length_electropherogram == 40:
        #     self.canvas_show_figure_base.config(scrollregion=(0, 0, 2100, 200))
        # elif self.x_length_electropherogram == 50:
        #     self.canvas_show_figure_base.config(scrollregion=(0, 0, 2800, 200))

        if color_list == ["color" for i in range(len(color_list))]:
            auto_color = 1
        else:
            for each in color_list:
                if each == "color":
                    tkinter.messagebox.showinfo(title="warning", message="please choose color")
                    return

        ### 根据用户所选范围截取有效数据 及所需展示的samples    self.selected_samples_name_electropherogram
        annotated_result = self.annotated_result[
            self.var_MTU_start_electropherogram.get() <= self.annotated_result["mean_MTU"]]
        annotated_result = annotated_result[annotated_result["mean_MTU"] <= self.var_MTU_end_electropherogram.get()]
        dataframe_plot = pd.DataFrame()
        for each in self.selected_samples_name_electropherogram:
            dataframe_plot[each] = annotated_result[each]

        legend_label = [i[:-7] for i in dataframe_plot.columns.values.tolist()]

        self.diff_electropherogram = self.var_interval_electropherogram.get()
        # 将来让用户自己调  1(linewidth)到 1/2*min_diff_of_mean_MTU之间

        ### 生成数据
        x_real = annotated_result["mean_MTU"].tolist()  # list of mean_MTU
        x = []  # list of mean_MTU + point around mean_MTU
        num_sample = dataframe_plot.shape[1]
        y = []
        for i in range(num_sample):
            y.append([])
        for i, each in enumerate(x_real):
            x.append(round(each - self.diff_electropherogram, 2))
            x.append(each)
            x.append(round(each + self.diff_electropherogram, 2))

        for i in range(num_sample):  # each column
            for j in range(len(x_real)):  # each row
                y[i].append(0)
                y[i].append(dataframe_plot.iloc[j][i])
                y[i].append(0)
        print(x)
        print(y)

        ### 画图
        # 先删除原有子组件
        for widget in self.frame_show_figure.winfo_children():
            widget.destroy()

        f = plt.figure()  # 创建图像窗口
        a_electropherogram = f.add_subplot(111)  # 添加子图:1行1列第1个

        for i in range(num_sample):
            if auto_color == 1:
                a_electropherogram.plot(x, y[i], linewidth=1.0)
            else:
                a_electropherogram.plot(x, y[i], linewidth=1.0, color=color_list[i])

        a_electropherogram.set_xlabel("migration time unit [MTU]")
        if self.nor_or_rel == "Normalization":
            a_electropherogram.set_ylabel("normalized signal intensity [nRFU]")
        elif self.nor_or_rel == "Relativization":
            a_electropherogram.set_ylabel("relative signal intensity [%]")
        if self.legend_position_electropherogram == "none":
            # 本身的图就没有legend
            pass
            # a_electropherogram.get_legend().remove()
        elif self.legend_position_electropherogram == "outer upper":
            a_position = a_electropherogram.get_position()  # （x0,y0,width,height）
            a_electropherogram.legend(bbox_to_anchor=(1.0, 1), loc="upper left", labels=legend_label, fontsize=8,
                                      markerscale=0.8)
        elif self.legend_position_electropherogram == "outer lower":
            a_electropherogram.legend(bbox_to_anchor=(1.0, 0), loc="upper left", labels=legend_label, fontsize=8,
                                      markerscale=0.8)
        else:
            a_electropherogram.legend(loc=self.legend_position_electropherogram, labels=legend_label, fontsize=8,
                                      markerscale=0.8,
                                      framealpha=0.7)

        ### 是否有annotation
        annotation = annotated_result["annotate"].tolist()
        if self.flag_annotation_electropherogram == "Yes":
            y_row_max = dataframe_plot.max(axis=1).values.tolist()  # 每一行的最大值
            a_electropherogram.set_ylim(0, max(y_row_max) + 0.2 * max(y_row_max))  # 稍微增加一下纵轴高度
            y_axis_max = plt.ylim()[1]  # 纵坐标轴最大值

            for index, i in enumerate(annotation):
                # y = max(self.dataframe_replicates_groups_meanstd.iloc[index].values.tolist())  # 虚线起始位置
                if i != '':
                    a_electropherogram.text(x_real[index], y_axis_max - 2, i, ha='center', va='bottom', fontsize=8,
                                            wrap=True, rotation=self.annotation_rotation_electropherogram)
                    a_electropherogram.plot([x_real[index], x_real[index], ], [y_row_max[index], y_axis_max - 2, ],
                                            'k--', linewidth=0.8)

        # 设置y_ticks
        try:
            plt.yticks(self.yticks_electropherogram)
        except:
            tkinter.messagebox.showinfo(title="warning", message="Invalid ticks of y axis")
            return

        # 设置上右边框消失
        plt.gca().spines['top'].set_color('none')  # gca()获取当前坐标轴信息   .spines设置边框
        plt.gca().spines['right'].set_color('none')  # 把绘制的图形显示到tkinter窗口上

        ### 增加x轴的长度
        if self.x_length_electropherogram != "normal":
            # change x internal size
            plt.gca().margins(x=0)  # 添加到轴的每个限制的填充是* margin *乘以数据间隔。 所有输入参数都必须是[0，1]范围内的浮点数
            # margins x轴和y轴分别具有特定的边距值。 这些不能与位置参数一起使用，但可以单独使用，例如仅在y轴上进行更改。
            plt.gcf().canvas.draw()
            # set size
            maxsize = self.x_length_electropherogram
            m = 0.2
            # N = len(x_label)
            N = len(self.annotated_result["mean_MTU"])
            s = maxsize / plt.gcf().dpi * N + 2 * m  # dpi 像素  s：x轴的长度 inches
            print("s:", s)
            print("plt.gcf().dpi:", plt.gcf().dpi)
            margin = m / plt.gcf().get_size_inches()[0]
            print("plt.gcf().get_size_inches()[0]:", plt.gcf().get_size_inches()[0])
            print("plt.gcf().get_size_inches()[1]:", plt.gcf().get_size_inches()[1])
            # 返回图形的当前大小（以英寸为单位)The size (width, height) of the figure in inches.
            plt.gcf().subplots_adjust(left=margin, right=1. - margin)
            plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

            self.canvas_show_figure_base.config(scrollregion=(0, 0, str(s + 10) + 'i', str(s) + 'i'))
            # 改变画布长度

        plt.show()

        # 把绘制的图形显示到tkinter窗口上
        self.canvas_show_figure = FigureCanvasTkAgg(f, self.frame_show_figure)
        self.canvas_show_figure.draw()
        self.canvas_show_figure.get_tk_widget().pack(side="top", fill="both", expand=1)

        # 把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
        toolbar = NavigationToolbar2Tk(self.canvas_show_figure,
                                       self.frame_show_figure)  # matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
        toolbar.update()
        self.canvas_show_figure._tkcanvas.pack(side="top", fill="both", expand=1)
        # get_tk_widget()得到的就是_tkcanvas

    def show_real_electropherogram(self):
        ### 判断用户取值范围
        if self.var_MTU_start_electropherogram.get() > self.var_MTU_end_electropherogram.get():
            tkinter.messagebox.showinfo(title="warning", message="Invalid MTU range")
            return

        ### 获取一些参数
        self.get_annotation_electropherogram()
        self.get_legend_electropherogram()
        self.get_annotation_rotation_electropherogram()
        self.get_x_length_electropherogram()
        color_list = []
        auto_color = 0
        for i, each in enumerate(self.selected_samples_name_electropherogram):
            exec('color_list.append(self.button_{}_bargraph["text"])'.format(i))
        print(color_list)
        # if self.x_length_electropherogram == 20:
        #     pass
        # elif self.x_length_electropherogram == 30:
        #     self.canvas_show_figure_base.config(scrollregion=(0, 0, 1400, 200))
        # elif self.x_length_electropherogram == 40:
        #     self.canvas_show_figure_base.config(scrollregion=(0, 0, 2100, 200))
        # elif self.x_length_electropherogram == 50:
        #     self.canvas_show_figure_base.config(scrollregion=(0, 0, 2800, 200))

        if color_list == ["color" for i in range(len(color_list))]:
            auto_color = 1
        else:
            for each in color_list:
                if each == "color":
                    tkinter.messagebox.showinfo(title="warning", message="please choose color")
                    return

        ### 根据用户所选范围截取有效数据 及所需展示的samples    self.selected_samples_name_electropherogram
        annotated_result = self.annotated_result[
            self.var_MTU_start_electropherogram.get() <= self.annotated_result["mean_MTU"]]
        annotated_result = annotated_result[annotated_result["mean_MTU"] <= self.var_MTU_end_electropherogram.get()]
        dataframe_plot = pd.DataFrame()
        for each in self.selected_samples_name_electropherogram:
            dataframe_plot[each] = annotated_result[each]

        legend_label = [i[:-7] for i in dataframe_plot.columns.values.tolist()]

        ### 获取数据
        x = annotated_result["mean_MTU"].tolist()  # list of mean_MTU
        num_sample = dataframe_plot.shape[1]
        y = []
        for i in range(num_sample):
            y.append([])
        for i in range(num_sample):  # each column
            for j in range(len(x)):  # each row
                y[i].append(dataframe_plot.iloc[j][i])

        ### 画图
        # 先删除原有子组件
        for widget in self.frame_show_figure.winfo_children():
            widget.destroy()

        f = plt.figure()  # 创建图像窗口
        a_electropherogram_real = f.add_subplot(111)  # 添加子图:1行1列第1个

        for i in range(num_sample):
            if auto_color == 1:
                a_electropherogram_real.plot(x, y[i], linewidth=1.0)
            else:
                a_electropherogram_real.plot(x, y[i], linewidth=1.0, color=color_list[i])

        a_electropherogram_real.set_xlabel("migration time[MTU]")
        if self.nor_or_rel == "Normalization":
            a_electropherogram_real.set_ylabel("normalized signal intensity")
        elif self.nor_or_rel == "Relativization":
            a_electropherogram_real.set_ylabel("relative signal intensity[%]")
        if self.legend_position_electropherogram == "none":
            # 本身的图就没有legend
            pass
            # a_electropherogram.get_legend().remove()
        elif self.legend_position_electropherogram == "outer upper":
            a_position = a_electropherogram_real.get_position()  # （x0,y0,width,height）
            a_electropherogram_real.legend(bbox_to_anchor=(1.0, 1), loc="upper left", labels=legend_label, fontsize=8,
                                           markerscale=0.8)
        elif self.legend_position_electropherogram == "outer lower":
            a_electropherogram_real.legend(bbox_to_anchor=(1.0, 0), loc="upper left", labels=legend_label, fontsize=8,
                                           markerscale=0.8)
        else:
            a_electropherogram_real.legend(loc=self.legend_position_electropherogram, labels=legend_label, fontsize=8,
                                           markerscale=0.8,
                                           framealpha=0.7)

        ### 是否有annotation
        annotation = annotated_result["annotate"].tolist()
        if self.flag_annotation_electropherogram == "Yes":
            y_row_max = dataframe_plot.max(axis=1).values.tolist()  # 每一行的最大值
            a_electropherogram_real.set_ylim(0, max(y_row_max) + 0.2 * max(y_row_max))  # 稍微增加一下纵轴高度
            y_axis_max = plt.ylim()[1]  # 纵坐标轴最大值

            for index, i in enumerate(annotation):
                # y = max(self.dataframe_replicates_groups_meanstd.iloc[index].values.tolist())  # 虚线起始位置
                if i != '':
                    a_electropherogram_real.text(x[index], y_axis_max - 2, i, ha='center', va='bottom', fontsize=8,
                                                 wrap=True, rotation=self.annotation_rotation_electropherogram)
                    a_electropherogram_real.plot([x[index], x[index], ], [y_row_max[index], y_axis_max - 2, ],
                                                 'k--', linewidth=0.8)

        # 设置y_ticks
        try:
            plt.yticks(self.yticks_electropherogram)
        except:
            tkinter.messagebox.showinfo(title="warning", message="Invalid ticks of y axis")
            return

        # 设置上右边框消失
        plt.gca().spines['top'].set_color('none')  # gca()获取当前坐标轴信息   .spines设置边框
        plt.gca().spines['right'].set_color('none')  # 把绘制的图形显示到tkinter窗口上

        if self.x_length_electropherogram != "normal":
            ### 增加x轴的长度
            # change x internal size
            plt.gca().margins(x=0)  # 添加到轴的每个限制的填充是* margin *乘以数据间隔。 所有输入参数都必须是[0，1]范围内的浮点数
            # margins x轴和y轴分别具有特定的边距值。 这些不能与位置参数一起使用，但可以单独使用，例如仅在y轴上进行更改。
            plt.gcf().canvas.draw()
            # set size
            maxsize = self.x_length_electropherogram
            m = 0.2
            # N = len(x_label)
            N = len(self.annotated_result["mean_MTU"])
            s = maxsize / plt.gcf().dpi * N + 2 * m  # dpi 像素  s：x轴的长度 inches
            print("s:", s)
            print("plt.gcf().dpi:", plt.gcf().dpi)
            margin = m / plt.gcf().get_size_inches()[0]
            print("plt.gcf().get_size_inches()[0]:", plt.gcf().get_size_inches()[0])
            print("plt.gcf().get_size_inches()[1]:", plt.gcf().get_size_inches()[1])
            # 返回图形的当前大小（以英寸为单位)The size (width, height) of the figure in inches.
            plt.gcf().subplots_adjust(left=margin, right=1. - margin)
            plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

            self.canvas_show_figure_base.config(scrollregion=(0, 0, str(s + 10) + 'i', str(s) + 'i'))
            # 改变画布长度

        plt.show()

        # 把绘制的图形显示到tkinter窗口上
        self.canvas_show_figure = FigureCanvasTkAgg(f, self.frame_show_figure)
        self.canvas_show_figure.draw()
        self.canvas_show_figure.get_tk_widget().pack(side="top", fill="both", expand=1)

        # 把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
        toolbar = NavigationToolbar2Tk(self.canvas_show_figure,
                                       self.frame_show_figure)  # matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
        toolbar.update()
        self.canvas_show_figure._tkcanvas.pack(side="top", fill="both", expand=1)
        # get_tk_widget()得到的就是_tkcanvas

    def creatWidge(self):
        """对应于GUI2中的self.frame_figure = ttk.Frame(self.tab)"""
        self.frame_main = ttk.Frame(self, height=640, width=1020)
        self.frame_main.pack(fill="both", expand=True)
        self.frame_main.pack_propagate(0)

        self.frame_choose_figure_of_canvas = ttk.Frame(self.frame_main, width=350)  # canvas的基底Frame  # 主界面左
        self.frame_choose_figure_of_canvas.pack_propagate(0)
        self.frame_choose_figure_of_canvas.pack(side="left", fill="y")
        self.canvas_choose_figure = tk.Canvas(self.frame_choose_figure_of_canvas,
                                              scrollregion=(0, 0, 1500, 1500))
        self.vbar_choose_figure = tk.Scrollbar(self.frame_choose_figure_of_canvas)
        self.vbar_choose_figure.pack(side="right", fill="y")
        self.vbar_choose_figure.config(command=self.canvas_choose_figure.yview)
        self.canvas_choose_figure.config(height=640, width=300)
        self.canvas_choose_figure.config(yscrollcommand=self.vbar_choose_figure.set)
        self.canvas_choose_figure.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        # self.canvas_choose_figure.pack_propagate(0)
        # self.canvas_choose_figure.bind("<MouseWheel>", self.canvas_choose_figure_mousewheel)

        self.frame_choose_figure = ttk.Frame(self.canvas_choose_figure, relief="ridge", width=280)  # 其他组件所位于的Frame
        # self.frame_choose_figure.pack(side="left", fill="y")  relief="ridge" , width=310
        self.canvas_choose_figure.create_window((0, 0), window=self.frame_choose_figure, anchor="nw")
        # , anchor="w"
        self.frame_choose_figure.bind("<Enter>", self.bound_to_canvas_choose_figure_mousewheel)
        self.frame_choose_figure.bind("<Leave>", self.unbound_to_canvas_choose_figure_mousewheel)

        self.frame_show_figure_of_canvas = ttk.Frame(self.frame_main, width=700)  # canvas的基底Frame  # 主界面右
        self.frame_show_figure_of_canvas.pack_propagate(0)
        self.frame_show_figure_of_canvas.pack(side="right", fill="y")
        self.canvas_show_figure_base = tk.Canvas(self.frame_show_figure_of_canvas, scrollregion=(0, 0, 700, 640))
        self.vbar_show_figure_base = tk.Scrollbar(self.frame_show_figure_of_canvas, orient="horizontal")
        self.vbar_show_figure_base.pack(side="bottom", fill="x")
        self.vbar_show_figure_base.config(command=self.canvas_show_figure_base.xview)
        self.canvas_show_figure_base.config(height=640, width=700)
        self.canvas_show_figure_base.config(xscrollcommand=self.vbar_show_figure_base.set)
        self.canvas_show_figure_base.pack(side="right", expand=True, fill="both", padx=5, pady=5)

        self.frame_show_figure = tk.Frame(self.canvas_show_figure_base, relief="ridge", width=700)  # 主界面右
        self.canvas_show_figure_base.create_window((0, 70), window=self.frame_show_figure, anchor="nw")

        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        self.frame_bar_graph_start = ttk.Frame(self.frame_choose_figure)
        self.frame_bar_graph_start.pack(fill='x', padx=5, pady=5)
        self.label_MTU_start_bar_graph = ttk.Label(self.frame_bar_graph_start, text="MTU_start")
        self.label_MTU_start_bar_graph.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_MTU_start_bar_graph = tk.DoubleVar()
        self.var_MTU_start_bar_graph.set(min(self.annotated_result["mean_MTU"].tolist()))
        self.scale_MTU_start_bar_graph = ttk.Scale(self.frame_bar_graph_start, from_=0,
                                                   to=max(self.annotated_result["mean_MTU"].tolist()),
                                                   variable=self.var_MTU_start_bar_graph,
                                                   command=lambda v: self.var_MTU_start_bar_graph.set(
                                                       round(float(v), 2)))
        self.scale_MTU_start_bar_graph.pack(side="left")
        self.label_show_MTU_start_bar_graph = ttk.Label(self.frame_bar_graph_start, state="readonly",
                                                        textvariable=self.var_MTU_start_bar_graph)
        self.label_show_MTU_start_bar_graph.pack(side="left", padx=5, anchor="w")

        self.frame_bar_graph_end = ttk.Frame(self.frame_choose_figure)
        self.frame_bar_graph_end.pack(fill='x', padx=5)
        self.label_MTU_end_bar_graph = ttk.Label(self.frame_bar_graph_end, text="MTU_end  ")
        self.label_MTU_end_bar_graph.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_MTU_end_bar_graph = tk.DoubleVar()
        self.var_MTU_end_bar_graph.set(max(self.annotated_result["mean_MTU"].tolist()))
        self.scale_MTU_end_bar_graph = ttk.Scale(self.frame_bar_graph_end, from_=0,
                                                 to=max(self.annotated_result["mean_MTU"].tolist()),
                                                 variable=self.var_MTU_end_bar_graph,
                                                 command=lambda v: self.var_MTU_end_bar_graph.set(
                                                     round(float(v), 2)))
        self.scale_MTU_end_bar_graph.pack(side="left")
        self.label_show_MTU_end_bar_graph = ttk.Label(self.frame_bar_graph_end, state="readonly",
                                                      textvariable=self.var_MTU_end_bar_graph)
        self.label_show_MTU_end_bar_graph.pack(side="left", padx=5, anchor="w")

        self.frame_bar_graph_annotation = ttk.Frame(self.frame_choose_figure)
        self.frame_bar_graph_annotation.pack(fill='x', padx=5)
        self.label_annotation_bar_graph = ttk.Label(self.frame_bar_graph_annotation, text="annotation")
        self.label_annotation_bar_graph.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_annotation_bar_graph = tk.StringVar()
        self.combobox_annotation_bar_graph = ttk.Combobox(self.frame_bar_graph_annotation, width=10,
                                                          textvariable=self.var_annotation_bar_graph)
        self.combobox_annotation_bar_graph.config(state='readonly')
        self.combobox_annotation_bar_graph.pack(side="left", padx=5)
        self.combobox_annotation_bar_graph["values"] = ["Yes", "No"]
        self.combobox_annotation_bar_graph.current(0)
        self.combobox_annotation_bar_graph.bind("<<ComboboxSelected>>", self.get_annotation_bar_graph)

        self.frame_bar_graph_annotation_rotation = ttk.Frame(self.frame_choose_figure)
        self.frame_bar_graph_annotation_rotation.pack(fill='x', padx=5)
        self.label_annotation_rotation_bar_graph = ttk.Label(self.frame_bar_graph_annotation_rotation,
                                                             text="rotation of annotation")
        self.label_annotation_rotation_bar_graph.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_annotation_rotation_bar_graph = tk.IntVar()
        self.combobox_annotation_rotation_bar_graph = ttk.Combobox(self.frame_bar_graph_annotation_rotation, width=10,
                                                                   textvariable=self.var_annotation_rotation_bar_graph)
        self.combobox_annotation_rotation_bar_graph.config(state='readonly')
        self.combobox_annotation_rotation_bar_graph.pack(side="left", padx=5)
        self.combobox_annotation_rotation_bar_graph["values"] = [0, 20, 30, 45, 60, 70, 90]
        self.combobox_annotation_rotation_bar_graph.current(2)
        self.combobox_annotation_rotation_bar_graph.bind("<<ComboboxSelected>>", self.get_annotation_rotation_bar_graph)

        self.frame_bar_graph_legend = ttk.Frame(self.frame_choose_figure)
        self.frame_bar_graph_legend.pack(fill='x', padx=5)
        self.label_legend_bar_graph = ttk.Label(self.frame_bar_graph_legend, text="legend position")
        self.label_legend_bar_graph.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_legend_bar_graph = tk.StringVar()
        self.combobox_legend_bar_graph = ttk.Combobox(self.frame_bar_graph_legend, width=10,
                                                      textvariable=self.var_legend_bar_graph)
        self.combobox_legend_bar_graph.config(state='readonly')
        self.combobox_legend_bar_graph.pack(side="left", padx=5)
        self.combobox_legend_bar_graph["values"] = ["none", "best", "upper right", "upper center", "upper left",
                                                    "center right", "center left", "lower right", "lower center",
                                                    "lower left", "outer upper", "outer lower"]
        self.combobox_legend_bar_graph.current(1)
        self.combobox_legend_bar_graph.bind("<<ComboboxSelected>>", self.get_legend_bar_graph)

        self.frame_bar_graph_yticks = ttk.Frame(self.frame_choose_figure)
        self.frame_bar_graph_yticks.pack(fill='x', padx=5)
        self.label_yticks_bar_graph = ttk.Label(self.frame_bar_graph_yticks, text="ticks of y axis")
        self.label_yticks_bar_graph.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_yticks_bar_graph = tk.StringVar()
        self.entry_yticks_bar_graph = ttk.Entry(self.frame_bar_graph_yticks, width=15,
                                                textvariable=self.var_yticks_bar_graph)
        self.entry_yticks_bar_graph.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_yticks_bar_graph.set("25,50,75,100")
        self.button_yticks_bar_graph = ttk.Button(self.frame_bar_graph_yticks, text="ok", width=3,
                                                  command=self.get_yticks_bar_graph)
        self.button_yticks_bar_graph.pack(side="left", pady=5, anchor="w")

        self.frame_bar_graph_x_length = ttk.Frame(self.frame_choose_figure)
        self.frame_bar_graph_x_length.pack(fill='x', padx=5)
        self.label_x_length_bar_graph = ttk.Label(self.frame_bar_graph_x_length, text="x axis length")
        self.label_x_length_bar_graph.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_x_length_bar_graph = tk.StringVar()
        self.combobox_x_length_bar_graph = ttk.Combobox(self.frame_bar_graph_x_length, width=10,
                                                        textvariable=self.var_x_length_bar_graph)
        self.combobox_x_length_bar_graph.config(state='readonly')
        self.combobox_x_length_bar_graph.pack(side="left", padx=5)
        self.combobox_x_length_bar_graph["values"] = ["normal", "20", "30", "40", "50"]
        self.combobox_x_length_bar_graph.current(1)
        self.combobox_x_length_bar_graph.bind("<<ComboboxSelected>>", self.get_x_length_bar_graph)

        self.frame_choose_samples_bar_graph_ensure = ttk.Frame(self.frame_choose_figure)
        self.frame_choose_samples_bar_graph_ensure.pack(side="top", fill="x", padx=5)
        self.label_choose_samples_bar_graph = ttk.Label(self.frame_choose_samples_bar_graph_ensure,
                                                               text="samples")
        self.label_choose_samples_bar_graph.pack(side="left", fill="x", padx=5, pady=5, anchor="w")
        self.button_ensure_choose_samples_bar_graph = ttk.Button(self.frame_choose_samples_bar_graph_ensure, text="ok",
                                                       command=self.get_choose_samples_bar_graph)
        self.button_ensure_choose_samples_bar_graph.pack(side="left", padx=5, anchor="w")

        self.frame_choose_samples_bar_graph = ttk.Frame(self.frame_choose_figure)
        self.frame_choose_samples_bar_graph.pack(side="top", fill="x", padx=5)
        self.canvas_choose_samples_bar_graph = tk.Canvas(self.frame_choose_samples_bar_graph, height=100,
                                                                scrollregion=(
                                                                    0, 0, self.len_samples * 30, self.len_samples * 30))
        self.vbar_choose_samples_bar_graph = tk.Scrollbar(self.frame_choose_samples_bar_graph)
        self.vbar_choose_samples_bar_graph.pack(side="left", fill="y")
        self.vbar_choose_samples_bar_graph.config(command=self.canvas_choose_samples_bar_graph.yview)
        self.canvas_choose_samples_bar_graph.config(height=100)  # width=290,
        self.canvas_choose_samples_bar_graph.config(yscrollcommand=self.vbar_choose_samples_bar_graph.set)
        self.canvas_choose_samples_bar_graph.pack(side="right", expand=True, fill="both", padx=5)
        self.choose_samples_bar_graph()

        self.label_color_bar_bar_graph = ttk.Label(self.frame_choose_figure, text="color bar")
        self.label_color_bar_bar_graph.pack(side="top", fill="x", padx=10, pady=5, anchor="w")
        self.frame_color_bar_bar_graph = ttk.Frame(self.frame_choose_figure)
        self.frame_color_bar_bar_graph.pack(side="top", fill="x", padx=5)
        ## 计算canvas scollregion长度    每个sample*30
        self.canvas_color_bar_bar_graph = tk.Canvas(self.frame_color_bar_bar_graph, height=100,
                                                    scrollregion=(0, 0, self.len_samples * 30, self.len_samples * 30))
        self.vbar_color_bar_bar_graph = tk.Scrollbar(self.frame_color_bar_bar_graph)
        # self.vbar_color_bar_bar_graph.pack(side="right", fill="y")
        self.vbar_color_bar_bar_graph.pack(side="left", fill="y")
        self.vbar_color_bar_bar_graph.config(command=self.canvas_color_bar_bar_graph.yview)
        self.canvas_color_bar_bar_graph.config(height=100)  # width=290
        self.canvas_color_bar_bar_graph.config(yscrollcommand=self.vbar_color_bar_bar_graph.set)
        # self.canvas_color_bar_bar_graph.pack(side="left", expand=True, fill="both", padx=5)
        self.canvas_color_bar_bar_graph.pack(side="right", expand=True, fill="both", padx=5)
        # self.choose_color_bar_bar_graph()

        self.button_bar_graph_show = ttk.Button(self.frame_choose_figure, text="bar graph", command=self.show_bar_graph,
                                                state="readonly")
        self.button_bar_graph_show.pack(padx=5, pady=5, anchor="w")

        # self.button_bar_graph_download = ttk.Button(self.frame_choose_figure, text="download")
        # self.button_bar_graph_download.pack(padx=5, pady=5, anchor="w")

        ttk.Separator(self.frame_choose_figure).pack(fill="x", pady=5)

        # --------------------------------------------------------------------------------------------------------------
        self.frame_mean_SD_start = ttk.Frame(self.frame_choose_figure)
        self.frame_mean_SD_start.pack(fill='x', padx=5)
        self.label_MTU_start_mean_SD = ttk.Label(self.frame_mean_SD_start, text="MTU_start")
        self.label_MTU_start_mean_SD.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_MTU_start_mean_SD = tk.DoubleVar()
        self.var_MTU_start_mean_SD.set(min(self.annotated_result["mean_MTU"].tolist()))
        self.scale_MTU_start_mean_SD = ttk.Scale(self.frame_mean_SD_start, from_=0,
                                                 to=max(self.annotated_result["mean_MTU"].tolist()),
                                                 variable=self.var_MTU_start_mean_SD,
                                                 command=lambda v: self.var_MTU_start_mean_SD.set(round(float(v), 2)))
        self.scale_MTU_start_mean_SD.pack(side="left")
        self.label_show_MTU_start_mean_SD = ttk.Label(self.frame_mean_SD_start, state="readonly",
                                                      textvariable=self.var_MTU_start_mean_SD)
        self.label_show_MTU_start_mean_SD.pack(side="left", padx=5, anchor="w")

        self.frame_mean_SD_end = ttk.Frame(self.frame_choose_figure)
        self.frame_mean_SD_end.pack(fill='x', padx=5)
        self.label_MTU_end_mean_SD = ttk.Label(self.frame_mean_SD_end, text="MTU_end  ")
        self.label_MTU_end_mean_SD.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_MTU_end_mean_SD = tk.DoubleVar()
        self.var_MTU_end_mean_SD.set(max(self.annotated_result["mean_MTU"].tolist()))
        self.scale_MTU_end_mean_SD = ttk.Scale(self.frame_mean_SD_end, from_=0,
                                               to=max(self.annotated_result["mean_MTU"].tolist()),
                                               variable=self.var_MTU_end_mean_SD,
                                               command=lambda v: self.var_MTU_end_mean_SD.set(round(float(v), 2)))
        self.scale_MTU_end_mean_SD.pack(side="left")
        self.label_show_MTU_end_mean_SD = ttk.Label(self.frame_mean_SD_end, state="readonly",
                                                    textvariable=self.var_MTU_end_mean_SD)
        self.label_show_MTU_end_mean_SD.pack(side="left", padx=5, anchor="w")

        self.frame_mean_SD_annotation = ttk.Frame(self.frame_choose_figure)
        self.frame_mean_SD_annotation.pack(fill='x', padx=5)
        self.label_annotation_mean_SD = ttk.Label(self.frame_mean_SD_annotation, text="annotation")
        self.label_annotation_mean_SD.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_annotation_mean_SD = tk.StringVar()
        self.combobox_annotation_mean_SD = ttk.Combobox(self.frame_mean_SD_annotation, width=8,
                                                        textvariable=self.var_annotation_mean_SD)
        self.combobox_annotation_mean_SD.config(state='readonly')
        self.combobox_annotation_mean_SD["values"] = ["Yes", "No"]
        self.combobox_annotation_mean_SD.current(0)
        self.combobox_annotation_mean_SD.pack(side="left", padx=5)
        self.combobox_annotation_mean_SD.bind("<<ComboboxSelected>>", self.get_annotation_mean_SD)

        self.frame_mean_SD_annotation_rotation = ttk.Frame(self.frame_choose_figure)
        self.frame_mean_SD_annotation_rotation.pack(fill='x', padx=5)
        self.label_annotation_rotation_mean_SD = ttk.Label(self.frame_mean_SD_annotation_rotation,
                                                           text="rotation of annotation")
        self.label_annotation_rotation_mean_SD.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_annotation_rotation_mean_SD = tk.IntVar()
        self.combobox_annotation_rotation_mean_SD = ttk.Combobox(self.frame_mean_SD_annotation_rotation, width=10,
                                                                 textvariable=self.var_annotation_rotation_mean_SD)
        # self.combobox_annotation_rotation_mean_SD.config(state='readonly')
        self.combobox_annotation_rotation_mean_SD.pack(side="left", padx=5)
        self.combobox_annotation_rotation_mean_SD["values"] = [0, 20, 30, 45, 60, 70, 90]
        self.combobox_annotation_rotation_mean_SD.current(2)
        self.combobox_annotation_rotation_mean_SD.bind("<<ComboboxSelected>>", self.get_annotation_rotation_mean_SD)

        self.frame_mean_SD_legend = ttk.Frame(self.frame_choose_figure)
        self.frame_mean_SD_legend.pack(fill='x', padx=5)
        self.label_legend_mean_SD = ttk.Label(self.frame_mean_SD_legend, text="legend position")
        self.label_legend_mean_SD.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_legend_mean_SD = tk.StringVar()
        self.combobox_legend_mean_SD = ttk.Combobox(self.frame_mean_SD_legend, width=10,
                                                    textvariable=self.var_legend_mean_SD)
        self.combobox_legend_mean_SD.config(state='readonly')
        self.combobox_legend_mean_SD.pack(side="left", padx=5)
        self.combobox_legend_mean_SD["values"] = ["none", "best", "upper right", "upper center", "upper left",
                                                  "center right", "center left", "lower right", "lower center",
                                                  "lower left", "outer upper", "outer lower"]
        self.combobox_legend_mean_SD.current(1)
        self.combobox_legend_mean_SD.bind("<<ComboboxSelected>>", self.get_legend_mean_SD)

        self.frame_mean_SD_yticks = ttk.Frame(self.frame_choose_figure)
        self.frame_mean_SD_yticks.pack(fill='x', padx=5)
        self.label_yticks_mean_SD = ttk.Label(self.frame_mean_SD_yticks, text="ticks of y axis")
        self.label_yticks_mean_SD.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_yticks_mean_SD = tk.StringVar()
        self.entry_yticks_mean_SD = ttk.Entry(self.frame_mean_SD_yticks, width=15,
                                              textvariable=self.var_yticks_mean_SD)
        self.entry_yticks_mean_SD.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_yticks_mean_SD.set("25,50,75,100")
        self.button_yticks_mean_SD = ttk.Button(self.frame_mean_SD_yticks, text="ok", width=3,
                                                  command=self.get_yticks_mean_SD)
        self.button_yticks_mean_SD.pack(side="left", pady=5, anchor="w")

        self.frame_mean_SD_x_length = ttk.Frame(self.frame_choose_figure)
        self.frame_mean_SD_x_length.pack(fill='x', padx=5)
        self.label_x_length_mean_SD = ttk.Label(self.frame_mean_SD_x_length, text="x axis length")
        self.label_x_length_mean_SD.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_x_length_mean_SD = tk.StringVar()
        self.combobox_x_length_mean_SD = ttk.Combobox(self.frame_mean_SD_x_length, width=10,
                                                      textvariable=self.var_x_length_mean_SD)
        self.combobox_x_length_mean_SD.config(state='readonly')
        self.combobox_x_length_mean_SD.pack(side="left", padx=5)
        self.combobox_x_length_mean_SD["values"] = ["normal", "20", "30", "40", "50"]
        self.combobox_x_length_mean_SD.current(1)
        self.combobox_x_length_mean_SD.bind("<<ComboboxSelected>>", self.get_x_length_mean_SD)

        self.frame_choose_groups_mean_SD_ensure = ttk.Frame(self.frame_choose_figure)
        self.frame_choose_groups_mean_SD_ensure.pack(side="top", fill="x", padx=5)
        self.label_choose_groups_mean_SD = ttk.Label(self.frame_choose_groups_mean_SD_ensure,
                                                               text="samples")
        self.label_choose_groups_mean_SD.pack(side="left", fill="x", padx=5, pady=5, anchor="w")
        self.button_ensure_choose_groups_mean_SD = ttk.Button(self.frame_choose_groups_mean_SD_ensure, text="ok",
                                                       command=self.get_choose_groups_mean_SD)
        self.button_ensure_choose_groups_mean_SD.pack(side="left", padx=5, anchor="w")

        self.frame_choose_groups_mean_SD = ttk.Frame(self.frame_choose_figure)
        self.frame_choose_groups_mean_SD.pack(side="top", fill="x", padx=5)
        self.canvas_choose_groups_mean_SD = tk.Canvas(self.frame_choose_groups_mean_SD, height=100,
                                                                scrollregion=(
                                                                    0, 0, len(self.dict_replicates_groups) * 30, len(self.dict_replicates_groups) * 30))
        self.vbar_choose_groups_mean_SD = tk.Scrollbar(self.frame_choose_groups_mean_SD)
        self.vbar_choose_groups_mean_SD.pack(side="left", fill="y")
        self.vbar_choose_groups_mean_SD.config(command=self.canvas_choose_groups_mean_SD.yview)
        self.canvas_choose_groups_mean_SD.config(height=100)  # width=290,
        self.canvas_choose_groups_mean_SD.config(yscrollcommand=self.vbar_choose_groups_mean_SD.set)
        self.canvas_choose_groups_mean_SD.pack(side="right", expand=True, fill="both", padx=5)
        self.choose_groups_mean_SD()

        self.label_color_bar_mean_SD = ttk.Label(self.frame_choose_figure, text="color bar")
        self.label_color_bar_mean_SD.pack(side="top", fill="x", padx=10, pady=5, anchor="w")
        self.frame_color_bar_mean_SD = ttk.Frame(self.frame_choose_figure)
        self.frame_color_bar_mean_SD.pack(side="top", fill="x", padx=5)
        self.canvas_color_bar_mean_SD = tk.Canvas(self.frame_color_bar_mean_SD, height=100,
                                                  scrollregion=(0, 0, 320, 320))
        self.vbar_color_bar_mean_SD = tk.Scrollbar(self.frame_color_bar_mean_SD)
        self.vbar_color_bar_mean_SD.pack(side="left", fill="y")
        self.vbar_color_bar_mean_SD.config(command=self.canvas_color_bar_mean_SD.yview)
        self.canvas_color_bar_mean_SD.config(height=100)  # width=290,
        self.canvas_color_bar_mean_SD.config(yscrollcommand=self.vbar_color_bar_mean_SD.set)
        self.canvas_color_bar_mean_SD.pack(side="right", expand=True, fill="both", padx=5)
        # self.choose_color_bar_mean_SD()

        self.button_mean_SD = ttk.Button(self.frame_choose_figure, text="mean and S.D.", command=self.show_mean_SD,
                                         state="disabled")
        self.button_mean_SD.pack(padx=5, pady=5, anchor="w")

        self.button_mean_SD_download_mean = ttk.Button(self.frame_choose_figure, text="download mean value",
                                                       command=self.mean_SD_download_mean, state="disabled")
        self.button_mean_SD_download_mean.pack(padx=5, pady=5, anchor="w")

        self.button_mean_SD_download_SD = ttk.Button(self.frame_choose_figure, text="download S.D value",
                                                     command=self.mean_SD_download_SD, state="disabled")
        self.button_mean_SD_download_SD.pack(padx=5, pady=5, anchor="w")

        self.button_mean_SD_download = ttk.Button(self.frame_choose_figure, text="download annotation result",
                                                     command=self.mean_SD_download, state="disabled")
        self.button_mean_SD_download.pack(padx=5, pady=5, anchor="w")

        if self.dict_replicates_groups != {}:
            self.button_mean_SD.config(state="readonly")
            self.canvas_color_bar_mean_SD.config(scrollregion=(0, 0, len(self.dict_replicates_groups) * 30,
                                                               len(self.dict_replicates_groups) * 30))
            # self.combobox_annotation_mean_SD["values"] = ["Yes", "No"]
            # self.combobox_annotation_bar_graph.current(0)

        ttk.Separator(self.frame_choose_figure).pack(fill="x", pady=5)

        # --------------------------------------------------------------------------------------------------------------
        """
        self.frame_electropherogram_start = ttk.Frame(self.frame_choose_figure)
        self.frame_electropherogram_start.pack(fill='x', padx=5)
        self.label_MTU_start_electropherogram = ttk.Label(self.frame_electropherogram_start, text="MTU_start:")
        self.label_MTU_start_electropherogram.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_MTU_start_electropherogram = tk.DoubleVar()
        self.var_MTU_start_electropherogram.set(min(self.annotated_result["mean_MTU"].tolist()))
        self.scale_MTU_start_electropherogram = ttk.Scale(self.frame_electropherogram_start, from_=0,
                                                          to=max(self.annotated_result["mean_MTU"].tolist()),
                                                          variable=self.var_MTU_start_electropherogram,
                                                          command=lambda v: self.var_MTU_start_electropherogram.set(
                                                              round(float(v), 2)))
        self.scale_MTU_start_electropherogram.pack(side="left")
        self.label_show_MTU_start_electropherogram = ttk.Label(self.frame_electropherogram_start, state="readonly",
                                                               textvariable=self.var_MTU_start_electropherogram)
        self.label_show_MTU_start_electropherogram.pack(side="left", padx=5, anchor="w")

        self.frame_electropherogram_end = ttk.Frame(self.frame_choose_figure)
        self.frame_electropherogram_end.pack(fill='x', padx=5)
        self.label_MTU_end_electropherogram = ttk.Label(self.frame_electropherogram_end, text="MTU_end:  ")
        self.label_MTU_end_electropherogram.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_MTU_end_electropherogram = tk.DoubleVar()
        self.var_MTU_end_electropherogram.set(max(self.annotated_result["mean_MTU"].tolist()))
        self.scale_MTU_end_electropherogram = ttk.Scale(self.frame_electropherogram_end, from_=0,
                                                        to=max(self.annotated_result["mean_MTU"].tolist()),
                                                        variable=self.var_MTU_end_electropherogram,
                                                        command=lambda v: self.var_MTU_end_electropherogram.set(
                                                            round(float(v), 2)))
        self.scale_MTU_end_electropherogram.pack(side="left")
        self.label_show_MTU_end_electropherogram = ttk.Label(self.frame_electropherogram_end, state="readonly",
                                                             textvariable=self.var_MTU_end_electropherogram)
        self.label_show_MTU_end_electropherogram.pack(side="left", padx=5, anchor="w")

        self.frame_electropherogram_interval = ttk.Frame(self.frame_choose_figure)
        self.frame_electropherogram_interval.pack(fill='x', padx=5)
        self.label_interval_electropherogram = ttk.Label(self.frame_electropherogram_interval, text="interval:     ")
        self.label_interval_electropherogram.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_interval_electropherogram = tk.DoubleVar()
        self.var_interval_electropherogram.set(round(self.min_diff_of_mean_MTU, 2))
        self.scale_interval_electropherogram = ttk.Scale(self.frame_electropherogram_interval, from_=0,
                                                         to=self.min_diff_of_mean_MTU,
                                                         variable=self.var_interval_electropherogram,
                                                         command=lambda v: self.var_interval_electropherogram.set(
                                                             round(float(v), 2)))
        self.scale_interval_electropherogram.pack(side="left")
        self.label_show_interval_electropherogram = ttk.Label(self.frame_electropherogram_interval, state="readonly",
                                                              textvariable=self.var_interval_electropherogram)
        self.label_show_interval_electropherogram.pack(side="left", padx=5, anchor="w")

        self.frame_electropherogram_annotation = ttk.Frame(self.frame_choose_figure)
        self.frame_electropherogram_annotation.pack(fill='x', padx=5)
        self.label_annotation_electropherogram = ttk.Label(self.frame_electropherogram_annotation, text="annotation")
        self.label_annotation_electropherogram.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_annotation_electropherogram = tk.StringVar()
        self.combobox_annotation_electropherogram = ttk.Combobox(self.frame_electropherogram_annotation, width=8,
                                                                 textvariable=self.var_annotation_electropherogram)
        self.combobox_annotation_electropherogram.config(state='readonly')
        self.combobox_annotation_electropherogram["values"] = ["Yes", "No"]
        self.combobox_annotation_electropherogram.current(0)
        self.combobox_annotation_electropherogram.pack(side="left", padx=5)
        self.combobox_annotation_electropherogram.bind("<<ComboboxSelected>>", self.get_annotation_electropherogram)

        self.frame_electropherogram_annotation_rotation = ttk.Frame(self.frame_choose_figure)
        self.frame_electropherogram_annotation_rotation.pack(fill='x', padx=5)
        self.label_annotation_rotation_electropherogram = ttk.Label(self.frame_electropherogram_annotation_rotation,
                                                                    text="rotation of annotation")
        self.label_annotation_rotation_electropherogram.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_annotation_rotation_electropherogram = tk.IntVar()
        self.combobox_annotation_rotation_electropherogram = ttk.Combobox(
            self.frame_electropherogram_annotation_rotation, width=10,
            textvariable=self.var_annotation_rotation_electropherogram)
        self.combobox_annotation_rotation_electropherogram.config(state='readonly')
        self.combobox_annotation_rotation_electropherogram.pack(side="left", padx=5)
        self.combobox_annotation_rotation_electropherogram["values"] = [0, 20, 30, 45, 60, 70, 90]
        self.combobox_annotation_rotation_electropherogram.current(2)
        self.combobox_annotation_rotation_electropherogram.bind("<<ComboboxSelected>>",
                                                                self.get_annotation_rotation_electropherogram)

        self.frame_electropherogram_legend = ttk.Frame(self.frame_choose_figure)
        self.frame_electropherogram_legend.pack(fill='x', padx=5)
        self.label_legend_electropherogram = ttk.Label(self.frame_electropherogram_legend, text="legend position")
        self.label_legend_electropherogram.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_legend_electropherogram = tk.StringVar()
        self.combobox_legend_electropherogram = ttk.Combobox(self.frame_electropherogram_legend, width=10,
                                                             textvariable=self.var_legend_electropherogram)
        self.combobox_legend_electropherogram.config(state='readonly')
        self.combobox_legend_electropherogram.pack(side="left", padx=5)
        self.combobox_legend_electropherogram["values"] = ["none", "best", "upper right", "upper center", "upper left",
                                                           "center right", "center left", "lower right", "lower center",
                                                           "lower left", "outer upper", "outer lower"]
        self.combobox_legend_electropherogram.current(1)
        self.combobox_legend_electropherogram.bind("<<ComboboxSelected>>", self.get_legend_electropherogram)

        self.frame_electropherogram_yticks = ttk.Frame(self.frame_choose_figure)
        self.frame_electropherogram_yticks.pack(fill='x', padx=5)
        self.label_yticks_electropherogram = ttk.Label(self.frame_electropherogram_yticks, text="ticks of y axis")
        self.label_yticks_electropherogram.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_yticks_electropherogram = tk.StringVar()
        self.entry_yticks_electropherogram = ttk.Entry(self.frame_electropherogram_yticks, width=15,
                                                       textvariable=self.var_yticks_electropherogram)
        self.entry_yticks_electropherogram.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_yticks_electropherogram.set("25,50,75,100")
        self.button_yticks_electropherogram = ttk.Button(self.frame_electropherogram_yticks, text="ok", width=3,
                                                  command=self.get_yticks_electropherogram)
        self.button_yticks_electropherogram.pack(side="left", pady=5, anchor="w")

        self.frame_electropherogram_x_length = ttk.Frame(self.frame_choose_figure)
        self.frame_electropherogram_x_length.pack(fill='x', padx=5)
        self.label_x_length_electropherogram = ttk.Label(self.frame_electropherogram_x_length, text="x axis length")
        self.label_x_length_electropherogram.pack(side="left", padx=5, pady=5, anchor="w")
        self.var_x_length_electropherogram = tk.StringVar()
        self.combobox_x_length_electropherogram = ttk.Combobox(self.frame_electropherogram_x_length, width=10,
                                                               textvariable=self.var_x_length_electropherogram)
        self.combobox_x_length_electropherogram.config(state='readonly')
        self.combobox_x_length_electropherogram.pack(side="left", padx=5)
        self.combobox_x_length_electropherogram["values"] = ["normal", "20", "30", "40", "50"]
        self.combobox_x_length_electropherogram.current(1)
        self.combobox_x_length_electropherogram.bind("<<ComboboxSelected>>", self.get_x_length_electropherogram)

        self.frame_choose_samples_electropherogram_ensure = ttk.Frame(self.frame_choose_figure)
        self.frame_choose_samples_electropherogram_ensure.pack(side="top", fill="x", padx=5)
        self.label_choose_samples_electropherogram = ttk.Label(self.frame_choose_samples_electropherogram_ensure,
                                                               text="samples")
        self.label_choose_samples_electropherogram.pack(side="left", fill="x", padx=5, pady=5, anchor="w")
        self.button_ensure_choose_samples = ttk.Button(self.frame_choose_samples_electropherogram_ensure, text="ok",
                                                       command=self.get_choose_samples_electropherogram)
        self.button_ensure_choose_samples.pack(side="left", padx=5, anchor="w")

        self.frame_choose_samples_electropherogram = ttk.Frame(self.frame_choose_figure)
        self.frame_choose_samples_electropherogram.pack(side="top", fill="x", padx=5)
        self.canvas_choose_samples_electropherogram = tk.Canvas(self.frame_choose_samples_electropherogram, height=100,
                                                                scrollregion=(
                                                                    0, 0, self.len_samples * 30, self.len_samples * 30))
        self.vbar_choose_samples_electropherogram = tk.Scrollbar(self.frame_choose_samples_electropherogram)
        self.vbar_choose_samples_electropherogram.pack(side="left", fill="y")
        self.vbar_choose_samples_electropherogram.config(command=self.canvas_choose_samples_electropherogram.yview)
        self.canvas_choose_samples_electropherogram.config(height=100)  # width=290,
        self.canvas_choose_samples_electropherogram.config(yscrollcommand=self.vbar_choose_samples_electropherogram.set)
        self.canvas_choose_samples_electropherogram.pack(side="right", expand=True, fill="both", padx=5)
        self.choose_samples_electropherogram()

        self.label_color_bar_electropherogram = ttk.Label(self.frame_choose_figure, text="color bar")
        self.label_color_bar_electropherogram.pack(side="top", fill="x", padx=10, pady=5, anchor="w")
        self.frame_color_bar_electropherogram = ttk.Frame(self.frame_choose_figure)
        self.frame_color_bar_electropherogram.pack(side="top", fill="x", padx=5)
        self.canvas_color_bar_electropherogram = tk.Canvas(self.frame_color_bar_electropherogram, height=100,
                                                           scrollregion=(0, 0, 320, 320))
        self.vbar_color_bar_electropherogram = tk.Scrollbar(self.frame_color_bar_electropherogram)
        self.vbar_color_bar_electropherogram.pack(side="left", fill="y")
        self.vbar_color_bar_electropherogram.config(command=self.canvas_color_bar_electropherogram.yview)
        self.canvas_color_bar_electropherogram.config(height=100)  # width=290,
        self.canvas_color_bar_electropherogram.config(yscrollcommand=self.vbar_color_bar_electropherogram.set)
        self.canvas_color_bar_electropherogram.pack(side="right", expand=True, fill="both", padx=5)

        self.button_electropherogram_show = ttk.Button(self.frame_choose_figure, text="electropherogram",
                                                       command=self.show_electropherogram)
        self.button_electropherogram_show.pack(padx=5, pady=5, anchor="w")

        ttk.Separator(self.frame_choose_figure).pack(fill="x", pady=5)

        # --------------------------------------------------------------------------------------------------------------
        self.button_real_electropherogram_show = ttk.Button(self.frame_choose_figure, text="real electropherogram",
                                                            command=self.show_real_electropherogram)
        self.button_real_electropherogram_show.pack(padx=5, pady=5, anchor="w")
        """



if __name__ == "__main__":
    root = tk.Tk()  # 创建跟窗口对象
    root.geometry("1200x740+100+100")
    root.title("Frame_Figure")
    database = FrameFigure(master=root)  # the object of the class Database
    root.mainloop()
