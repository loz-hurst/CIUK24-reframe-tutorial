import reframe as rfm
import reframe.utility.sanity as sn

from benchmarks.modules.utils import SpackTest

@rfm.simple_test
class StreamTest(SpackTest):
    valid_systems = ['*']
    valid_prog_environs = ['default']

    spack_speck = 'stream@5.10 +openmp'
    executable = 'stream_c.exe'

    threads = parameter([4, 8, 16])
    arraysize = parameter([2**10, 2**15, 2**20, 2**25])

#    reference = {
#        'archer2': {
#            'Copy': (92000, -0.1, 0.1, 'MB/s'),
#            'Scale': (73000, -0.1, 0.1, 'MB/s'),
#            'Add': (86000, -0.1, 0.1, 'MB/s'),
#            'Triad': (87000, -0.1, 0.1, 'MB/s'),
#        },
#    }

    def __init__(self):
        self.spack_spec = f'stream@5.10 +openmp stream_array_size={self.arraysize}'
        self.env_vars['OMP_NUM_THREADS'] = self.threads
        self.env_vars['OMP_PLACES'] = 'cores'
        self.num_cpus_per_task = self.threads

    @sanity_function
    def validate_solution(self):
        return sn.assert_found(r'Solution Validates', self.stdout)
    
    @performance_function('MB/s', perf_key='Copy')
    def extract_copy_perf(self):
        return sn.extractsingle(r'Copy:\s+(\S+)\s+.*', self.stdout, 1, float)
    
    @performance_function('MB/s', perf_key='Scale')
    def extract_scale_perf(self):
        return sn.extractsingle(r'Scale:\s+(\S+)\s+.*', self.stdout, 1, float)
    
    @performance_function('MB/s', perf_key='Add')
    def extract_add_perf(self):
        return sn.extractsingle(r'Add:\s+(\S+)\s+.*', self.stdout, 1, float)
    
    @performance_function('MB/s', perf_key='Triad')
    def extract_triad_perf(self):
        return sn.extractsingle(r'Triad:\s+(\S+)\s+.*', self.stdout, 1, float)
    
