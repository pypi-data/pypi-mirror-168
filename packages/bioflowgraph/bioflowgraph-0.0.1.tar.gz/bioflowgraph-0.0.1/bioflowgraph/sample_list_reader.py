from curses import panel
from os.path import exists
from collections import OrderedDict

from exuse.extypings import Callable, RecordList


class SampleListReader:

    def __init__(self, fp: str):
        assert exists(fp)
        self.sample_list_file = fp
        self.records: RecordList = None
        self._parse_sample_list_file()

    def _parse_sample_list_file(self):
        records = []
        with open(self.sample_list_file) as rd:
            headers = next(rd).strip().split('\t')
            for line in rd:
                if line.strip() == '':
                    continue
                row = line.strip().split('\t')
                records.append({k: v for k, v in zip(headers, row)})
        self.records = records


class FragmentedSampleListReader(SampleListReader):
    """
    样本的 fq1 或者 fq2 被分成了几段，需要先将分段文件合并为一个完整文件。

    样本列表文件格式：
    - `Patient`: 患者名称，一个患者通常有 tumor 和 normal 两个样本
    - `Sample`: 样本名称
    - `Type`: 该文件所属的类型 T1 T2 N1 N2
    - `RawFq`: 文件路径

    调用 group_samples() 获取分组信息。
    """

    def __init__(self, fp: str, index_fn: Callable[[str], int] = None):
        """
        Args:
            index_fn (Callable[[str], int], optional): 对于分段fq文件，需要提供一个函数用于从文件名中提取出分段顺序。
            默认使用样本列表文件中定义的顺序。
        """
        super().__init__(fp)
        self.index_fn = index_fn
        self.__grouped_samples = None

    def get_fqs(self, pname: str, tntype: str, fqtype: int):
        records = self.grouped_samples[pname][tntype][f'raw_fq_{fqtype}']
        return [r['RawFq'] for r in records]

    @property
    def grouped_samples(self):
        """
        {
            [patient: str]: {
                [type: 'tumor' | 'normal']: {
                    raw_fq_1: Record[]
                    raw_fq_2: Record[]
                }
            }
        }
        """
        if self.__grouped_samples is not None:
            return self.__grouped_samples

        Q_TN = {'T': 'tumor', 'N': 'normal'}
        Q_12 = {'1': 'raw_fq_1', '2': 'raw_fq_2'}

        def getks(t):
            return (Q_TN[t[0]], Q_12[t[1]])

        def geti(x):
            return self.index_fn(x['RawFq'])

        pd = OrderedDict()
        for r in self.records:
            pn = r['Patient']
            if pn not in pd:
                pd[pn] = {
                    'tumor': {
                        'raw_fq_1': [],
                        'raw_fq_2': []
                    },
                    'normal': {
                        'raw_fq_1': [],
                        'raw_fq_2': []
                    },
                }
            x = getks(r['Type'])
            pd[pn][x[0]]['sample'] = r['Sample']
            pd[pn][x[0]][x[1]].append(r)

        if self.index_fn is not None:
            for d in pd.values():
                for t in ('tumor', 'normal'):
                    for f in ('raw_fq_1', 'raw_fq_2'):
                        if len(d[t][f]) > 1:
                            d[t][f] = sorted(d[t][f], key=geti)

        self.__grouped_samples = pd
        return pd
