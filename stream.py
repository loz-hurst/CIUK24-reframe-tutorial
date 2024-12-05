import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class StreamTest(rfm.RegressionTest):
    valid_systems = ['archer2']
    valid_prog_environs = ['cray']

    sourcesdir = 'https://github.com/jeffhammond/STREAM'

    #env_vars['OMP_NUM_THREADS'] = 4
    #env_vars['OMP_PLACES'] = 'cores'
    threads = parameter([4, 8, 16])

    build_system = 'SingleSource'
    sourcepath = 'stream.c'

    #arraysize = 2**20
    arraysize = parameter([2**10, 2**15, 2**20, 2**25])

    reference = {
        'archer2': {
            'Copy': (92000, -0.1, 0.1, 'MB/s'),
            'Scale': (73000, -0.1, 0.1, 'MB/s'),
            'Add': (86000, -0.1, 0.1, 'MB/s'),
            'Triad': (87000, -0.1, 0.1, 'MB/s'),
        },
    }

    @run_before('compile')
    def set_compiler_flags(self):
        self.build_system.ccpflags = [ f'-DSTREAM_ARRAY_SIZE={self.arraysize}' ]
        self.build_system.cflags = [ '-fopenmp', '-O3' ]

    @run_before('run')
    def set_env_vars(self):
        self.env_vars['OMP_NUM_THREADS'] = self.threads
        self.env_vars['OMP_PLACES'] = 'cores'

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
    
