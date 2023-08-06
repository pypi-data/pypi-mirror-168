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

或

```bash
tunas2dsdl convert -d <dataset_path> -w <working dir> -t <task> -s
```

**注意：**

* 如果已经通过 `-i` 和 `-a` 指定了 `dataset_info.json`和相应的 标注文件，则不可以使用 `-d` 选项；
* 如果已经使用了 `-d` 选项，则不可以使用 `-i` 与 `-a` 选项

**参数详解**：

| 参数                | 含义                                                        |
| ------------------- | ----------------------------------------------------------- |
| `-d/--directory` | tunas标准数据集的目录路径`<dataset_path>`，该目录下必须包含`<dataset_path>/dataset_info.json`、`<dataset_path>/annotations/json/<json_file>`等内容 |
| `-i/--dataset-info` | tunas标准数据集的`dataset_info.json`的路径                  |
| `-a/--annotation`   | tunas标准数据集的标注文件的路径                             |
| `-w/--working-dir`  | 生成的dsdl yaml文件存储的目录路径，最终代码会在该目录中生成与segment name同名的文件夹，并将所有的内容保存到该文件夹中 |
| `-t/--task`         | 当前处理的的任务，目前只支持选项`detection`，对应了检测任务 |
| `-s/--separate-store`  | 是否将数据集中的samples单独存储到一个json文件中，当样本数量巨大的情况下可以使用该选项，默认存储的文件名为`samples.json`，保存在working-dir目录下 |
| `-c/--config` | 如果要从aliyun oss上读取文件，则需要通过该选项指定配置文件路径 |

> 阿里云OSS配置文件为一个json文件，内容如下：
>
> ```json
> {
>     "access_key_secret": "your secret access key",
>     "endpoint": "your endpoint",
>     "access_key_id": "your access key id"
> }
> ```
