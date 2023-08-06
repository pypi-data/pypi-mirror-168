# 项目简介

该项目的作用是将tunas标准数据集转换为符合dsdl标准的yaml文件

**项目安装**：

```bash
pip install tunas2dsdl
```

**项目使用**：

```bash
tunas2dsdl convert -i <dataset_info path> -a <annotation file> -w <working dir> -t <task> -s
```

**参数详解**：

| 参数                | 含义                                                        |
| ------------------- | ----------------------------------------------------------- |
| `-i/--dataset-info` | tunas标准数据集的`dataset_info.json`的路径                  |
| `-a/--annotation`   | tunas标准数据集的标注文件的路径                             |
| `-w/--working-dir`  | 生成的dsdl yaml文件存储的目录路径，目录必须存在且必须为空   |
| `-t/--task`         | 当前处理的的任务，目前只支持选项`detection`，对应了检测任务 |
| `-s/--separate-store`  | 是否将数据集中的samples单独存储到一个json文件中，当样本数量巨大的情况下可以使用该选项，默认存储的文件名为`samples.json`，保存在working-dir目录下 |

