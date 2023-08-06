# 流程使用

bioflowgrah 定位是一个轻量级、随时迁移的流程任务自动投递工具。

## 运行任务图

```
python tg.py run call_snv ...
```

参数如下：

- `-g`：导出任务图类的 py 文件（未实现）
- `-s`：样本列表文件，默认为工作目录下的 *sample_list.tsv*
- `-e`：环境文件，默认为工作目录下的 *env.toml*
- `-w`：流程工作目录，默认为 */tmp/bioflowgraph/graphs/*
- `-q`：运行任务队列大小，默认 2
- `-r`：任务状态刷新时间间隔，默认 10 秒

默认情况下，上述命令运行的流程的结果和状态会保存到 */tmp/bioflowgraph/graphs/call_snv/* 目录中，其结构如下：

![image-20220923110141204](https://img.barwe.cc/2022/09/20220923110141.png)

- call_snv 下的子目录是各个子任务的执行结果和状态
    - 计划执行的 shell 命令
    - 执行过程的 STDOUT 和 STDERR
    - 执行成功的标志文件
- taskgraph.gv.png 是任务图结构
- taskgraph.status.gv.png 是任务执行情况

运行任务图会创建一个监测主进程，所有任务都会在其<u>子进程</u>中运行，所以请保证主程序一直在前台或者后台运行。

停止监测程序，所有运行中的任务会被中断。再次运行监测程序，上次中断的任务和失败的任务会重新运行，所以在重新运行之前检查任务失败的原因并修复。

<u>小技巧</u>：在 screen 里面可以一直让监测程序在前台运行



## 网页监测工具

```
python tg.py watch call_snv
```



## 运行前准备

运行一个流程需要以下几个要素：

- `graph_name`: **必须**，流程本次运行的名称，程序根据这个名称在工作目录下建立对应的目录
    如果是已有流程任务的名称，则会尝试从上次中断的地方继续运行
- `sample_list_file`:**必须**， 样本列表文件，列举出所有原始 fq 文件路径
    该文件是一个 tsv 文件，至少包含下面四列：
    1. <u>Patient</u>: 例如 zhangsan
    2. <u>Sample</u>: 样本名称，例如 zhangsan-tumor, zhangsan-normal
    3. <u>Type</u>: fq 文件类型，可选值四个 T1, T2, N1, N2，标识了 fq 文件所属的 tumor/normal 和 fq1/fq2 类别
    4. <u>RawFq</u>: fq 文件的绝对路径
- `working_dir`: **可选**，流程运行的工作目录，<u>默认是 /tmp/bioflowgraph/graphs</u>，会在工作目录下创建与`graph_name`指定名称同名的目录
- `env_file`: **可选**，流程运行需要用到的各种软件路径、参考数据库路径和<u>注册的 units 位置</u>，默认是与脚本同级目录下的 env.toml 文件
- `params_file`: **建议**，流程运行时各个子任务需要的分析参数

### sample list

一个规范的样本列表文件例子：

```
Patient	Sample	Type	RawFq
noname	noname-tumor	T1	/tumor_1.fq.gz
noname	noname-tumor	T2	/tumor_2.fq.gz
noname	noname-normal	N1	/normal_1/normal_1_test.part_001.fq.gz
noname	noname-normal	N1	/normal_1/normal_1_test.part_002.fq.gz
noname	noname-normal	N2	/normal_2.fq.gz
```

如果一个 fq 文件被拆分成了多个，需要按顺序列出它们，否则会导致拼接结果错误。

### env file

一个 toml 文件，缺省时使用执行脚本统计目录下的 env.toml 文件。

一个例子：

```toml
registered_units = ["data/units", "data/units/common", "data/units/test"]

[executors]
python3 = "/home/barwe/miniconda3/bin/python"
bwamem2 = "/home/ynwang/biosoft/bwa-mem2-2.0pre2_x64-linux/bwa-mem2"
gatk = "/home/ynwang/biosoft/gatk-4.1.9.0/gatk"
annovar = "/home/ynwang/biosoft/annovar"

[scripts]
fake_bwamem2 = "/home/barwe/projects/bioflowgraph/data/fake_bwamem2.py"

[databases]
hg38_fa = "/home/ynwang/database/gatk/hg38.bwa2.index/hg38.fa"
hg38_vcf_gz = "/home/ynwang/database/gatk/somatic-hg38_small_exac_common_3.hg38.vcf.gz"
humandb = "/home/ynwang/biosoft/annovar/humandb/"
```

- `registered_units`: 固定 key，注册自定义的 unit 文件。<u>一般作为用户使用流程时，这些 units 都会被内置，注释掉这行即可</u>。
- `executors`: 流程运行依赖的系统软件路径
- `scripts`: 流程需要用到的脚本路径
- `databases`: 流程需要用到的参数文件和数据库路径

### params file

流程运行需要的参数，例如

```json
{
    "bwamem2": {
        "threads": 12
    }
}
```

**注**：现在只能为 unit 设置参数，如果不同的 task 需要使用同一个 unit 和不同的参数，<u>后面可考虑改成为 task 设置参数</u>。



### 其他

某些软件例如 gatk 需要 java 环境，现在需要手动加到用户环境变量里面。

<u>后面考虑改成执行命令时临时设置环境变量</u>（需要加一个接受环境变量的接口）。



# 流程开发

大致分为两步：写 unit，写任务图。

## unit 开发

一条需要执行的命令就是一个 unit，大到 bwa，小到 cp 都可以看做 unit。

一个 unit 对应一个 json 文件，里面详细记录了这个命令需要用到的参数。

<u>unit 文件是对软件及其参数的描述</u>，这些信息基本上在软件的帮助文档里面找得到。

下面是一个 bwa 命令：

```
bwamem2 mem -v 3 -t 24 -Y -R "@RG\tID:${ID}\tSM:${ID}\tPL:Illumina"  /home/ynwang/database/gatk/hg38.bwa2.index/hg38.fa $1 $2 >${ID}.raw.sam
```

它对应的 unit 文件是：

```json|bwamem2.json
{
    "executor": "bwamem2",
    "sub_executor": "mem",
    "parameters": [
        { "name": "v", "flag": "-v", "type": "int", "default": 3 },
        { "name": "threads", "flag": "-t", "type": "integer", "default": 24 },
        { "name": "Y", "flag": "-Y", "type": "bool", "default": true },
        { "name": "R", "flag": "-R", "default": "\"@RG\\tID:${SampleID}\\tSM:${SampleID}\\tPL:Illumina\"" },
        { "name": "bwa_index", "type": "ref", "default": "hg38_fa" },
        { "name": "fq_1", "is_input": true },
        { "name": "fq_2", "is_input": true },
        { "name": "samfile", "type": "stdout", "default": "${SampleID}.raw.sam" }
    ]
}
```

主体由三部分组成：

- executor 执行主程序，必须有
- sub_executor 子程序或者执行的脚本，可选
- parameters 参数配置，配置常用参数，使用时不给值就不会添加该参数，所以多个流程相同的 unit 基本上可以复用

对参数进行详细的描述可以方便的串联起不同的模块，在平台调用时参数可完全由用户控制。

下面是描述参数的几个属性。

### name

参数名称，取一个有意义的名称，能够一眼直到这个参数是干啥的。

建议 snake_case 形式。

可以从程序帮助文档中查阅到。

### flag & long_flag

参数的长短标，位置参数不用写这两个。

一般可选参数都会有长标(`--`开头的），不一定有短标（`-`开头的）。

可以从程序帮助文档中查阅到，如果有的话都写上。

### desc

参数的功能描述，可以从程序帮助文档中查阅到，有的话就抄过来。

### type

参数类型，这个需要自己推测。常见的类型就三种：字符串、数值和布尔值。

如果是普通字符串的话可以不写这个属性，默认 str。

数值可以根据文档描述或者字面值写成 int 或者 float，例如线程数肯定是 int，p 值肯定就是 float。

如果参数只有参数标志没有参数值，例如`--show-log`，它就是一个 bool 参数。

对于字符串参数，除了普通字符串之外，还定义了一些特殊的字符串类型，根据参数的含义选择就行了。

**ref**

表示该参数需要引用服务器上的一个路径，例如 bwa 需要用到的参考基因组文件。

既然是服务器路径，就需要从环境文件中引入，所以直接在 default 属性里面写上 key 就行了。

自定义程序使用的脚本路径也应该写到环境文件里面，然后在描述 unit 时使用 key。

**path**

该参数表示一个路径，例如临时目录。

一般用不上。

**stdout** & **stderr**

将一个参数声明为 stdout 或者 stderr，如果不用这两个类型，程序会自动加上对应的参数。

可以在定义流程时禁用这两个参数。

这个主要用来替换默认设置，例如 bwa 通过 stdout 保存结果，我又需要给它的输出接口取一个形象点的名字例如 samfile，就将一个参数显式声明为 stdout，否则就会使用默认的名称。

**list**

参数是一个列表参数，例如`-I a b c d`，或者`-I a -I b -I c -I d`这两种形式。

后者尚未实现。

### is_input & is_output

这两个属性很重要，它决定了 unit 暴露哪些参数作为输入接口，那些参数作为输出接口。

输入接口、输出接口都是指的文件：unit 读哪些文件，输出到哪些文件。

只有输入接口才能和上一步的 unit 连接，只有输出接口才能和下一步的 unit 连接。

stdout 类型的参数本身就是一种输出，它自动称为输出接口。

例如 bwa 有两个输入接口 fq_1, fq_2 和一个输出接口 samfile。

**输入接口和输出接口是组装流程的关键。**

### default

参数默认值。一般依赖于具体数据的参数不要设置默认值。

参数的默认值可以在运行流程时通过参数文件覆盖掉。

下面几种情况建议设置默认值：

- 线程数这种与生信无关的参数设置一个兜底值
- ref 类型的参数需要设置默认值为环境文件中的 key
- path 类型的参数需要设置默认值为环境文件中的 key
- is_output 的参数通过默认值描述 unit 输出文件的名称格式
- stderr 类型的参数与 is_output 类似

标记为 is_output 的参数、stderr 类型的参数都表示一种输出，stderr 不计入输入接口。

在表示输出路径参数的默认值中，可以使用 **模板变量** 替换样本名称、任务名称之类的信息。

默认可使用的模板变量：SampleID or SampleName, 以及其他的例如 TaskName, UnitName, WorkingDir, OutputDir, ShellDir, StdxxDir 等。

上述模板变量会在运行任务时自动计算和替换。

**自定义模板变量**：部分 unit 可能需要自己的模板变量，例如下面是 cat 指令的 unit：

```json
{
  "executor": "cat",
  "parameters": [
    {
      "name": "targets",
      "type": "list",
      "required": true,
      "is_input": true
    },
    {
      "name": "dest",
      "type": "stdout",
      "default": "${dest}"
    }
  ]
}
```

该 unit 使用了一个模板变量 dest，需要在定义任务图时显式传递该模板变量，否则不能成功构建。

## unit 注册

成熟的 unit 可以内置于包中，不需要用户显式注册。

自定义的需要在 env.toml的<u>registered_units</u>中注册。

```env.toml
registered_units = ["data/units", "data/units/common", "data/units/test"]
```

## 任务图开发

继承 TaskGraph 类，实现其 define_graph() 方法即可。

```python
from bioflowgraph import TaskGraph

class TumorSnvCallingTaskGraph(TaskGraph):

    # override
    def define_graph(self, sl_file: str):
        pass
```

define_graph() 方法的第一个参数是样本列表文件，只要在内部遍历样本添加任务即可。

先明晰几个概念：

> Unit：一个命令及其参数的描述（不含参数值）
>
> Task：unit 及其一次运行的状态管理，例如每次用 bwa 跑一个样本就是一个 task
>
> TaskGraph: task 之间的依赖关系以及运行状态管理
>
> TaskPolling: 运行 TaskGraph 对象

如果使用标准的样本列表文件格式，bioflowgraph 已经提供了一个文件解析器来读这个文件。

这个文件解析器返回的数据格式为：

```json
{
    "PATIENT": {
        "tumor": {
            "raw_fq_1": Row[],
            "raw_fq_2": Row[]
        },
        "normal": {
            "raw_fq_1": Row[],
            "raw_fq_2": Row[]
        },
    }
}
```

该解析器自动聚合了可能存在的分段文件。

然后遍历成对的样本添加任务即可：

```python
class TumorSnvCallingTaskGraph(TaskGraph):

    # override
    def define_graph(self, sl_file: str):
        rd = FragmentedSampleListReader(sl_file)

        annovars: List[Task] = []
        for patient, patientd in rd.grouped_samples.items():
            td = patientd['tumor']
            nd = patientd['normal']
            t_name = td['sample']  # tumor sample name
            n_name = nd['sample']  # normal sample name
            teps = {'Tumor': t_name, 'Normal': n_name}

            bwa_t = self.add_bwa(t_name, rd.get_fqs(patient, 'tumor', 1), rd.get_fqs(patient, 'tumor', 2))
            bwa_n = self.add_bwa(n_name, rd.get_fqs(patient, 'normal', 1), rd.get_fqs(patient, 'normal', 2))
            
            md_t = self.add_task(t_name, 'markdup', bwa_t)
            md_n = self.add_task(n_name, 'markdup', bwa_n)

```

`add_bwa()`方法接受 fq 文件路径，添加可能的 cat 任务和必要的 bwa 任务。它实际上也是调用了`add_task()`方法，详情可看代码。

使用`add_task()`方法向任务图中添加任务，并指定任务间的依赖关系。基本参数：

- `sample_name`: 处理单个样本的任务就用样本名，处理成对样本的任务就用 patient 名，处理所有 patient 的任务就自己取一个
- `unit_name`: 任务需要使用的 unit，必须是已注册的 unit，填其文件名即可
- `dependencies`: 可选，该任务依赖的父任务，下面再讲
- `templates`: 可选，该任务 unit 需要的自定模板变量，例如 cat 的 dest 模板
- `inputs`: 可选，直接指定任务某个参数的值，优先级比默认值高，但是比运行时传入的参数文件低
- `STDOUT`: 可选，默认 True, enable stdout
- `STDERR`: 同上

依赖的形式是：

```json
{"当前任务的输入接口": (依赖于哪一个任务, 依赖于前面任务的哪一个输出接口)}
```

当依赖的任务除了 stdout 参数之外只有一个输出接口时，可以简写为：

```json
{"当前任务的输入接口": 依赖于哪一个任务}
```

当当前任务只有一个输入接口时，可以进一步简写：

```json
依赖于哪一个任务
```

此外如果需要对依赖任务的输出路径做一些转换和处理，可以再传入一个函数，参数是依赖任务的输出路径：

```json
{"CUR_INPUT": (dep_task, DEP_OUTPUT, lambda fp: fp)}
```

模板变量也可以指定为一个函数，对

下面是一个完整的例子：

```python
class TumorSnvCallingTaskGraph(TaskGraph):

    # override
    def define_graph(self, sl_file: str):
        rd = FragmentedSampleListReader(sl_file)

        annovars: List[Task] = []
        for patient, patientd in rd.grouped_samples.items():
            td = patientd['tumor']
            nd = patientd['normal']
            t_name = td['sample']  # tumor sample name
            n_name = nd['sample']  # normal sample name
            teps = {'Tumor': t_name, 'Normal': n_name}

            bwa_t = self.add_bwa(t_name, rd.get_fqs(patient, 'tumor', 1), rd.get_fqs(patient, 'tumor', 2))
            bwa_n = self.add_bwa(n_name, rd.get_fqs(patient, 'normal', 1), rd.get_fqs(patient, 'normal', 2))

            md_t = self.add_task(t_name, 'markdup', bwa_t)
            md_n = self.add_task(n_name, 'markdup', bwa_n)

            sb_t = self.add_task(t_name, 'sortbam', {'bamfile': (md_t, 'bamfile')})
            sb_n = self.add_task(n_name, 'sortbam', {'bamfile': (md_n, 'bamfile')})

            _ = {'t_bamfile': (sb_t, 'sorted_bamfile'), 'n_bamfile': (sb_n, 'sorted_bamfile')}
            mutect2 = self.add_task(patient, 'mutect2', _, teps)

            lrom = self.add_task(patient, 'LearnReadOrientationModel', (mutect2, 'f1r2_targz_file'), teps)

            t_gps = self.add_task(t_name, 'GetPileupSummaries', {'bamfile': (sb_t, 'sorted_bamfile')})
            n_gps = self.add_task(n_name, 'GetPileupSummaries', {'bamfile': (sb_n, 'sorted_bamfile')})

            _ = {'table_file': (t_gps, 'table_file'), 'matched': (n_gps, 'table_file')}
            cc = self.add_task(patient, 'CalculateContamination', _, teps)

            _ = {
                'contamination_table_file': (cc, 'contamination_table_file'),
                'ob_priors': (lrom, 'read_orientation_model_file'),
                'vcfgz_file': (mutect2, 'vcfgz_file')
            }
            fmc = self.add_task(patient, 'FilterMutectCalls', _, teps)

            annovar = self.add_task(patient, 'annovar', {'filter_vcfgz_file': (fmc, 'filter_vcfgz_file')}, teps)

            annovars.append(annovar)

        cat = self.add_task('total', 'cat', params={'dest': 'cat-annovar.txt'})

        f = lambda fp: f'{fp}.hg38_multianno.txt'
        for annovar in annovars:
            cat.set_dep(annovar, 'output_prefix', 'targets', f)

```

模板检查发生在参数赋值之后，所以上面第 46 行直接给 dest 参数赋值覆盖了模板变量。

# 代码

http://120.25.166.92/barwe/bioflowgraph



# 后续

unit：

- [ ] snv calling units 参数修改，需要查阅软件文档，特别是参数名称，写规范一点；需要修改对应的任务图脚本
- [ ] 将流程中可能用到系统命令转化为 unit，能想到就是 cp, rm, mv, cat, ...



运行问题：

- [ ] 检测占用的内存和cpu，动态调节队列大小，防止服务器卡死，通过 psutils 检测
- [ ] 通过 key 动态指定流程，tg.py 现在默认使用 TumorSnvCallingTaskGraph，预留了 `--graph-class-file` 参数
- [ ] 任务失败时，解决完问题，监测程序自动重新执行任务，不需要停止重启
- [ ] 支持单任务直接启动，不需要构建任务图
- [ ] 现在的任务图都需要预定义。给定一组 units，参数和输入，通过程序快速组装出任务图，给平台流程组装留接口
- [ ] 兼容 sge：需要修改投递任务和刷新任务的方式



网页端监控：

- [ ] 网页端加上自动刷新
- [ ] 启动网页监测服务使用随机端口或者检测端口是否被占用
- [ ] 公网端口映射，能在外网访问

