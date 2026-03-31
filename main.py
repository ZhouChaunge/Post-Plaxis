import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from plxscripting.easy import *

parameter = 'e0=0.9'  # 输入本构参数值,请务必使用 "参数名=数值"的格式进行书写
                     # Enter constitutive parameter value in "name=value" format.
                     # The string will be split by '=' to extract the parameter name
                     # and create a corresponding folder under 'output'.

# TODO 配置 Plaxis 2D Output 的服务器参数设置
# Configure Plaxis 2D Output remote scripting server
s_o, g_o = new_server('localhost', '10001', password='user')

# TODO 地连墙(Plate)和地表土体(Soil)的几何尺寸和参考点选择
# Geometry dimensions and reference points for Plate (diaphragm wall) and Soil
plate_x_val = 50      # 地连墙x坐标 / Plate x-coordinate
plate_y_start = 20    # 地连墙y起点 / Plate y-start
plate_y_end = -20     # 地连墙y终点 / Plate y-end
plate_y_step = -0.25  # 竖直方向步长 / Vertical step size

soil_y_val = 20       # 地表土体y坐标 / Surface soil y-coordinate
soil_x_start = 0      # 地表土体x起点 / Soil x-start
soil_x_end = 50       # 地表土体x终点 / Soil x-end
soil_x_step = 0.5     # 水平方向步长 / Horizontal step size

# 施工阶段配置: (phase对象属性名, 显示标签)
# Construction phase config: (phase attribute name, display label)
PHASES = [
    ('phase_2', 'Phase1'),
    ('phase_3', 'Phase2'),
    ('phase_4', 'Phase3'),
    ('phase_5', 'Phase4'),
]

# 生成地连墙沿着竖直方向上的特征点
# Generate vertical reference points along the diaphragm wall
plate_y_values = np.arange(plate_y_start,
                           plate_y_end + plate_y_step,
                           plate_y_step)

# 生成地表土体沿着水平方向上的特征点
# Generate horizontal reference points along the ground surface
soil_x_values = np.arange(soil_x_start,
                          soil_x_end + soil_x_step,
                          soil_x_step)


def get_para_name():
    return parameter.split('=')[0]


def save_dataframe_to_excel(df, output_filename, sheet_name):
    """将 DataFrame 保存到 Excel 文件（支持追加工作表）
    Save a DataFrame to an Excel file (supports appending sheets)."""
    if os.path.exists(output_filename):
        with pd.ExcelWriter(output_filename, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
    else:
        df.to_excel(output_filename, index=False, sheet_name=sheet_name)


para_path = os.path.join(os.getcwd(), 'output', get_para_name())
os.makedirs(para_path, exist_ok=True)


# TODO 提取地连墙的水平数据
# Extract horizontal displacement of diaphragm wall (Plate)
class PlateDisplacement:

    def __init__(self, phase):
        self.phase = phase
        self.plate_y_val = []
        self.plate_ux_val = []
        self._extract()

    def _extract(self):
        for y in plate_y_values:
            ux = g_o.getsingleresult(self.phase,
                                     g_o.ResultTypes.Plate.Ux,
                                     plate_x_val, y)
            self.plate_y_val.append(y - plate_y_start)
            self.plate_ux_val.append(ux * 1000)

    def plot(self, label):
        plt.plot(self.plate_ux_val, self.plate_y_val,
                 linestyle='-', label=label)

    def save(self, output_filename, sheet_name):
        df = pd.DataFrame({'y': self.plate_y_val, 'ux': self.plate_ux_val})
        save_dataframe_to_excel(df, output_filename, sheet_name)


# TODO 提取地表土体的竖向数据
# Extract vertical displacement of surface soil
class SoilDisplacement:

    def __init__(self, phase):
        self.phase = phase
        self.soil_x_val = []
        self.soil_uy_val = []
        self._extract()

    def _extract(self):
        for x in soil_x_values:
            uy = g_o.getsingleresult(self.phase,
                                     g_o.ResultTypes.Soil.Uy,
                                     x, soil_y_val)
            self.soil_x_val.append(soil_x_end - x)
            self.soil_uy_val.append(uy * 1000)

    def plot(self, label):
        plt.plot(self.soil_x_val, self.soil_uy_val,
                 linestyle='-', label=label)

    def save(self, output_filename, sheet_name):
        df = pd.DataFrame({'x': self.soil_x_val, 'uy': self.soil_uy_val})
        save_dataframe_to_excel(df, output_filename, sheet_name)


if __name__ == '__main__':

    plate_file = f'{para_path}/plate-ux-{parameter}.xlsx'
    soil_file = f'{para_path}/soil-uy-{parameter}.xlsx'

    plate_outputs = []
    soil_outputs = []

    for phase_attr, label in PHASES:
        phase = getattr(g_o, phase_attr)

        plate = PlateDisplacement(phase)
        plate.save(plate_file, label)
        plate_outputs.append((plate, label))

        soil = SoilDisplacement(phase)
        soil.save(soil_file, label)
        soil_outputs.append((soil, label))

    # 绘制地连墙水平位移曲线 / Plot plate wall horizontal displacement
    plt.figure(figsize=(4, 5))
    for plate, label in plate_outputs:
        plate.plot(label)
    plt.xlabel('Horizontal Displacement, ux(mm)')
    plt.ylabel('Depth(m)')
    plt.title('Displacement of Plate Wall')
    plt.grid(True)
    plt.legend()
    plt.savefig(f'{para_path}/Plate-ux-{parameter}.png')

    # 绘制地表土体竖向位移曲线 / Plot surface soil vertical displacement
    plt.figure(figsize=(8, 4))
    for soil, label in soil_outputs:
        soil.plot(label)
    plt.xlabel('Soil horizontal point, x(m)')
    plt.ylabel('Vertical displacement, uy(mm)')
    plt.title('Displacement of Surface Soil')
    plt.grid(True)
    plt.legend()
    plt.savefig(f'{para_path}/Soil_uy-{parameter}.png')

    plt.show()
