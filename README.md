<div align="center">
<h1 align="center">Post-Plaxis</h1>
</div>

## 0.项目简介

这个项目主要是介绍如何利用远程脚本服务器从 `Plaxis 2D/3D Output Viewer` 中高效、快速的导出结果。这个项目提供了一个二维基坑开挖的参数敏感性算例，使用python提取地连墙位移和地表土体沉降，其中使用到了上海本构模型(Shanghai Model)进行了计算。


## 1.本构程序安装

在文件夹`usdm`中有本构子程序`20230801-UnifiedModel64.dll`，复制该`.dll`文件到您本地的`...Plaxis\3D\udsm\`中，即可完成本构子程序的安装。

![images/dll_install.png](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/dll_install.png)


## 2.Python环境依赖

这个项目提供了两种环境配置方案，分别是`environment.yaml`和`requirements.txt`的方式。
1. 利用`yaml`配置环境
   
   你可以在这个项目文件夹下，右键运行`cmd`进入控制台，然后运行下面代码:

        conda env create -f environment.yaml

3. 利用`txt`配置环境
   
   如果想要利用`requirements.txt`文件来配置环境，右键打开`cmd`进入控制台，依次输入下面代码：

        conda crate -n plaxis37 python=3.7 #创建名为pyplaxis37的python环境
        conda activate plaxis37            # 在当前目录下激活pyabaqus37环境
        pip install -r requirements.txt   # 安装基础依赖库


这里已经默认您的电脑安装了`Anaconda`软件，无论你采用哪一种方式，在完成上面的环境配置之后，会在`.../Anaconda/envs/`目录下会生成文件夹`plaxis37`用于存放相关的依赖文件，如下所示：
![envir_dir.png](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/envir_dir.png)


使用Python在Plaxis中进行后处理，最重要的库是`plxscripting`，但是这个库无法通过`pip`指令进行安装，需要借助Plaxis才能安装。这里你打开文件夹`model`，然后打开`2Dmodel.p2dx`进入到Plaxis 2D软件中，此时点击上方`专业`→`Python`→`配置Python解释器`依次点击，如下所示：
![Py_interpreter.png](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/Py_interpreter.png)
然后需要在弹出来的配置窗口中，选择新创建的`plaxis37`环境下的python解释器，然后点击`安装所需组件`，等待安装完成即可，流程如下所示：
![plxscripting_install.gif](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/plxscripting_install.gif)

完成安装后，Plaxis 后处理所依赖的python环境已经全部配置完成。


# 2.程序运行说明
提供的算例是一个二维基坑开挖，这个算例旨在通过一个简单的均匀地基中基坑开挖平面应变算例，来分析本构参数对地连墙侧向位移与地表土体沉降的敏感程度。算例的基本情况如下所示：
![model_description.png](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/model_description.png)
开展的本构敏感性分析，其参数的取值分别如下所示：

| 本构参数          | 基准值    | 敏感性定性分析|
|------------       |--------|----------------|
| 初始孔隙比e0      | 0.9    | 0.6→0.9→1.2    | 
| 泊松比ν           | 0.3    | 0.3→0.4→0.45   |
| 临界状态线斜率M   | 1.2    | 0.9→1.2→1.5    |
| 小应变参数γ0.7    | 0.0002 | 0.0001→0.001→1 | 
| 压缩指数λ         | 0.2    | 0.04→0.1→0.2   | 
| 回弹指数κ         | 0.02   | 0.02→0.04→0.08 |
| 超固结控制参数m   | 2.5    | 0.2→1.0→5.0    |
| 结构性控制参数a   | 1      | 0.1→0.5→2.0    |
| 初始超固结参数OCR | 5      | 1→5→10         |
| 初始结构性参数R0* | 0.5    | 0.01→0.1→1     |

在设置好参数、计算工况等相关准备后，运行计算，在求解完成后，查看计算结果，如下图所示：
![run_calculation.gif](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/run_calculation.gif)


在查看计算结果后，进入到 Plaxis 2D Output Viewer 中，此时点击`专业`→`配置远程脚本服务器`，如下所示：
![set_button.png](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/set_button.png)


根据个人需求，配置远程服务器中的`端口`和`配置密码`，这里选择端口`<10001>`，配置密码为`<user>`，如下所示：
![set_servicer.png](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/set_servicer.png)

然后打开`main.py`，在文件中找到下面代码，修改端口和密码，要求与在Plaxis中配置的一致。

        # TODO 配置 Plaxis 2D Output 的服务器参数设置
        s_o, g_o = new_server('localhost', '10001', password='user')
此时，运行`main.py`，即可完成计算结果提取。如下所示：

![extract_results.gif](https://raw.githubusercontent.com/ZhouChaunge/Post-Plaxis/main/image/extract_results.gif)
