site_configuration = {
    'systems': [
        {
            'name': 'archer2',
            'descr': 'ARCHER2 cofnig for CIUK',
            'hostnames': ['ln[0-9]+'],
            'partitions': [
                {
                    'name': 'compute-node',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['--partition=standard', '--qos=short'],
                    'environs': ['cray'],
                },
            ],
        },
    ],
    'environments': [
        {
            'name': 'cray',
            'cc': 'mpicc',
            'cxx' : 'mpic++',
            'ftn': 'mpif90',
        },
    ],
}
