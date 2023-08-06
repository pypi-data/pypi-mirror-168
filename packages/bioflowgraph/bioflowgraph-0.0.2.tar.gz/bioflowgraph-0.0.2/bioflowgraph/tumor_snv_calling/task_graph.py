# coding=utf-8
from typing import List
from exuse.exlogging import init_logging
from exuse.extypings import Callable
from bioflowgraph import TaskGraph, FragmentedSampleListReader
from bioflowgraph.task import Task
from exuse.expath import join, basename, dirname

GetIndexFn = Callable[[str], int]
GetMergeFn = Callable[[str], str]

init_logging()


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
