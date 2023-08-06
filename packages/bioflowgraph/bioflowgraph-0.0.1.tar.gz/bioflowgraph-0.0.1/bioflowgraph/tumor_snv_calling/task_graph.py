# coding=utf-8
from exuse.exlogging import init_logging
from exuse.extypings import Callable
from bioflowgraph import TaskGraph, FragmentedSampleListReader

GetIndexFn = Callable[[str], int]
GetMergeFn = Callable[[str], str]

init_logging()


class TumorSnvCallingTaskGraph(TaskGraph):

    # override
    def define_graph(self, sl_file: str, index: GetIndexFn = None, output_filename: GetMergeFn = None):
        rd = FragmentedSampleListReader(sl_file, index)
        for group_name, group_data in rd.grouped_samples.items():
            td = group_data['tumor']
            nd = group_data['normal']
            t_name = td['sample']  # tumor sample name
            n_name = nd['sample']  # normal sample name
            teps = {'Tumor': t_name, 'Normal': n_name}

            t_fq_1 = self.feed_fq(f'{t_name}-fq1', rd.get_fqs(group_name, 'tumor', 1), output_filename)
            t_fq_2 = self.feed_fq(f'{t_name}-fq2', rd.get_fqs(group_name, 'tumor', 2), output_filename)
            n_fq_1 = self.feed_fq(f'{n_name}-fq1', rd.get_fqs(group_name, 'normal', 1), output_filename)
            n_fq_2 = self.feed_fq(f'{n_name}-fq2', rd.get_fqs(group_name, 'normal', 2), output_filename)

            t_bwa = self.add_task(t_name, 'bwamem2', {'fq_1': t_fq_1, 'fq_2': t_fq_2})
            n_bwa = self.add_task(n_name, 'bwamem2', {'fq_1': n_fq_1, 'fq_2': n_fq_2})

            t_markdup = self.add_task(t_name, 'markdup', t_bwa)
            n_markdup = self.add_task(n_name, 'markdup', n_bwa)

            t_sortbam = self.add_task(t_name, 'sortbam', (t_markdup, 'bamfile'))
            n_sortbam = self.add_task(n_name, 'sortbam', (n_markdup, 'bamfile'))

            _ = {'t_bamfile': (t_sortbam, 'sorted_bamfile'), 'n_bamfile': (n_sortbam, 'sorted_bamfile')}
            mutect2 = self.add_task(group_name, 'mutect2', _, teps)

            lrom = self.add_task(group_name, 'LearnReadOrientationModel', (mutect2, 'f1r2_targz_file'), teps)

            t_gps = self.add_task(t_name, 'GetPileupSummaries', {'bamfile': (t_sortbam, 'sorted_bamfile')})
            n_gps = self.add_task(n_name, 'GetPileupSummaries', {'bamfile': (n_sortbam, 'sorted_bamfile')})

            _ = {'table_file': (t_gps, 'table_file'), 'matched': (n_gps, 'table_file')}
            cc = self.add_task(group_name, 'CalculateContamination', _, teps)

            _ = {
                'contamination_table_file': cc,
                'ob_priors': (lrom, 'read_orientation_model_file'),
                'vcfgz_file': (mutect2, 'vcfgz_file')
            }
            fmc = self.add_task(group_name, 'FilterMutectCalls', _, teps)

            self.add_task(group_name, 'annovar', fmc, teps)
