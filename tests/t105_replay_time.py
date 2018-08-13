#!/usr/bin/env python

from runtest import TestBase
import subprocess as sp

TDIR='xxx'

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'sleep', result="""
# DURATION    TID     FUNCTION
            [32537] | main() {
            [32537] |   foo() {
            [32537] |     bar() {
            [32537] |       usleep() {
   2.068 ms [32537] |         /* linux:schedule */
   2.080 ms [32537] |       } /* usleep */
   2.084 ms [32537] |     } /* bar */
   2.102 ms [32537] |   } /* foo */
   2.103 ms [32537] | } /* main */
""")

    def pre(self):
        record_cmd = '%s record -d %s %s' % (TestBase.uftrace_cmd, TDIR, 't-' + self.name)
        sp.call(record_cmd.split())
        return TestBase.TEST_SUCCESS

    def runcmd(self):
        return '%s replay -t 1ms -d %s' % (TestBase.uftrace_cmd, TDIR)

    def post(self, ret):
        sp.call(['rm', '-rf', TDIR])
        return ret
