import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class HelloTest(rfm.RegressionTest):
    valid_systems = ['*']
    valid_prog_environs = ['*']

    sourcepath = 'hello.c'

    @sanity_function
    def assert_hello(self):
        return sn.assert_found(r'Hello, World\!', self.stdout)

