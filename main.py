import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from plxscripting.easy import *

parameter = 'e0=0.9'  # 输入本构参数值,请务必使用 “参数名=数值”的格式进行书写，
                     # 因为后面将按照 '=' 对该字符串进行切分，获取参数名，并在 ‘output’ 中创建相应的文件夹

# TODO 配置 Plaxis 2D Output 的服务器参数设置
s_o, g_o = new_server('localhost', '10001', password='user')

# TODO 地连墙(Plate)和地表土体(Soil)的几何尺寸和参考点选择
plate_x_val = 50      # 输入地连墙x方向的坐标值
plate_y_start = 20    # 输入地连墙y方向的坐标值起始点
plate_y_end = -20     # 输入地连墙y方向的坐标值结束点
plate_y_step = -0.25  # 输入地连墙沿着竖直方向的间隔步长

soil_y_val = 20       # 输入地连墙x方向的坐标值
soil_x_start = 0      # 输入地连墙y方向的坐标值起始点
soil_x_end = 50       # 输入地连墙y方向的坐标值结束点
soil_x_step = 0.5     # 输入地连墙沿着竖直方向的间隔步长

#  生成地连墙沿着竖直方向上的特征点
plate_y_values = np.arange(plate_y_start,
                           plate_y_end + plate_y_step,
                           plate_y_step)

#  生成地表土体沿着水平方向上的特征点
soil_x_values = np.arange(soil_x_start,
                          soil_x_end + soil_x_step,
                          soil_x_step)


def get_para_name():
    para_name = parameter.split('=')[0]
    return para_name


para_path = os.path.join(os.getcwd(), 'output', get_para_name())
if not os.path.exists(para_path):
    os.makedirs(para_path)

# TODO 提取地连墙的水平数据
class Output_Plate_Displacement:

    def __init__(self):
        self.plate_y_val = []
        self.plate_ux_val = []

    def get_plate_ux(self, plate_y_values, phase):
        '''
        提取地连墙的水平位移数据
        :param plate_y_values: 地连墙竖向参考点
        :param phase: 施工计算阶段
        :return: 地连墙各个竖向位移参考点的水平位移
        '''
        for plate_y_val in plate_y_values:
            plate_ux_val = g_o.getsingleresult(phase,
                                               g_o.ResultTypes.Plate.Ux,
                                               plate_x_val, plate_y_val)
            plate_ux_val = 1000 * plate_ux_val
            self.plate_y_val.append(plate_y_val-plate_y_start)
            self.plate_ux_val.append(plate_ux_val)

    def plot_plate_ux(self, phase):
        '''
        绘制地连墙水平位移曲线
        :param phase: 施工计算阶段
        :return: 该施工阶段的地连墙水平位移曲线
        '''
        plt.plot(self.plate_ux_val, self.plate_y_val,
                 linestyle='-', label=phase)
        plt.xlabel('Horizontal Displacement, ux(mm)')
        plt.ylabel('Depth(m)')
        plt.title(f'Displacement of Plate Wall')
        plt.grid(True)
        plt.legend()

    def save_plate_data(self, output_filename, sheet_name):
        '''
        保存地连墙水平位移数据到excel文件中
        :param output_filename: 输入保存的Excel文件名称
        :param sheet_name: 输入每个Excel文件中工作表的名称
        :return: 地连墙位移数据的Excel文件
        '''
        data = {'y': self.plate_y_val,
                'ux': self.plate_ux_val}
        df = pd.DataFrame(data)
        if os.path.exists(output_filename):
            with pd.ExcelWriter(output_filename,
                                engine='openpyxl',
                                mode='a') as writer:
                df.to_excel(writer,
                            index=False,
                            sheet_name=sheet_name)
        else:
            df.to_excel(output_filename,
                        index=False,
                        sheet_name=sheet_name)


# TODO 提取地表土体的竖向数据
class Output_Soil_Displacement:

    def __init__(self):
        self.soil_x_val = []  # 添加这行
        self.soil_uy_val = []  # 添加这行

    def get_soil_uy(self, soil_x_values, phase):
        for soil_x_val in soil_x_values:
            soil_uy_val = g_o.getsingleresult(phase,
                                              g_o.ResultTypes.Soil.Uy,
                                              soil_x_val, soil_y_val)
            soil_uy_val = 1000 * soil_uy_val
            self.soil_x_val.append(soil_x_end-soil_x_val)
            self.soil_uy_val.append(soil_uy_val)

    def plot_soil_uy(self, phase):
        plt.plot(self.soil_x_val, self.soil_uy_val,
                 linestyle='-', label=phase)
        plt.xlabel('Soil horizontal point, x(m)')
        plt.ylabel('Vertical displacement, uy(mm)')
        plt.title(f'Displacement of Surface Soil')
        plt.grid(True)
        plt.legend()

    def save_soil_data(self, output_filename, sheet_name):
        data = {'x': self.soil_x_val,
                'uy': self.soil_uy_val}
        df = pd.DataFrame(data)
        if os.path.exists(output_filename):
            with pd.ExcelWriter(output_filename,
                                engine='openpyxl',
                                mode='a') as writer:
                df.to_excel(writer,
                            index=False,
                            sheet_name=sheet_name)
        else:
            df.to_excel(output_filename,
                        index=False,
                        sheet_name=sheet_name)


if __name__ == '__main__':

    # TODO 提取地连墙的侧向位移uy数据
    plate_output1 = Output_Plate_Displacement()
    plate_output1.get_plate_ux(plate_y_values, g_o.phase_2)
    plate_output1.save_plate_data(f'{para_path}/plate-ux-{parameter}.xlsx', 'Phase1')

    plate_output2 = Output_Plate_Displacement()
    plate_output2.get_plate_ux(plate_y_values, g_o.phase_3)
    plate_output2.save_plate_data(f'{para_path}/plate-ux-{parameter}.xlsx', 'Phase2')

    plate_output3 = Output_Plate_Displacement()
    plate_output3.get_plate_ux(plate_y_values, g_o.phase_4)
    plate_output3.save_plate_data(f'{para_path}/plate-ux-{parameter}.xlsx', 'Phase3')

    plate_output4 = Output_Plate_Displacement()
    plate_output4.get_plate_ux(plate_y_values, g_o.phase_5)
    plate_output4.save_plate_data(f'{para_path}/plate-ux-{parameter}.xlsx', 'Phase4')

    plt.figure(figsize=(4, 5))  # 设置图像的宽度为10英寸，高度为6英寸
    plate_output1.plot_plate_ux('Phase1')
    plate_output2.plot_plate_ux('Phase2')
    plate_output3.plot_plate_ux('Phase3')
    plate_output4.plot_plate_ux('Phase4')

    plt.savefig(f'{para_path}/Plate-ux-{parameter}.png')


    # TODO 提取地表土体的竖向位移数据uy
    soil_output1 = Output_Soil_Displacement()
    soil_output1.get_soil_uy(soil_x_values, g_o.phase_2)
    soil_output1.save_soil_data(f'{para_path}/soil-uy-{parameter}.xlsx', 'Phase1')

    soil_output2 = Output_Soil_Displacement()
    soil_output2.get_soil_uy(soil_x_values, g_o.phase_3)
    soil_output2.save_soil_data(f'{para_path}/soil-uy-{parameter}.xlsx', 'Phase2')

    soil_output3 = Output_Soil_Displacement()
    soil_output3.get_soil_uy(soil_x_values, g_o.phase_4)
    soil_output3.save_soil_data(f'{para_path}/soil-uy-{parameter}.xlsx', 'Phase3')

    soil_output4 = Output_Soil_Displacement()
    soil_output4.get_soil_uy(soil_x_values, g_o.phase_5)
    soil_output4.save_soil_data(f'{para_path}/soil-uy-{parameter}.xlsx', 'Phase4')

    plt.figure(figsize=(8, 4))  # 设置图像的宽度为8英寸，高度为4英寸
    soil_output1.plot_soil_uy('Phase1')
    soil_output2.plot_soil_uy('Phase2')
    soil_output3.plot_soil_uy('Phase3')
    soil_output4.plot_soil_uy('Phase4')

    plt.savefig(f'{para_path}/Soil_uy-{parameter}.png')

    plt.show()