import itertools
import os
import sys
import typing
import unittest
from contextvars import ContextVar

import fasteners
import multiprocessing as mp

lock = fasteners.InterProcessLock('.multiunit.lock')

worker_info = ContextVar('worker_id')
test_counter = ContextVar('test_counter', default=0)


class WorkerInfo(typing.NamedTuple):
    id: int
    count: int


class TestResult(unittest.TextTestResult):

    def printErrors(self):
        with lock:
            super().printErrors()


class TestRunner(unittest.TextTestRunner):
    resultclass = TestResult


class TestLoader(unittest.TestLoader):

    def loadTestsFromTestCase(self, testCaseClass):
        counter = test_counter.get()
        test_counter.set(counter + 1)
        worker_id, workers = worker_info.get()
        if counter % workers == worker_id:
            return super().loadTestsFromTestCase(testCaseClass)
        return unittest.TestSuite()


class TestProgram(unittest.TestProgram):
    initialized = False

    def __init__(self, *args, testLoader=TestLoader(), **kwargs):
        super().__init__(*args, testLoader=testLoader, **kwargs)
        self.initialized = True

    @property
    def runTests(self):
        if not self.initialized:
            return lambda *args: None
        return super().runTests

    def _getParentArgParser(self):
        parser = super()._getParentArgParser()
        parser.add_argument('--workers', type=int, default=4,
                            help='The number of worker processes')
        parser.add_argument('--id', type=int, dest='workerid',
                            help='Launch just the worker with given id')
        return parser


def work(id, argv, count):
    info = WorkerInfo(id, count)
    worker_info.set(info)
    program = TestProgram(argv=argv, module=None)
    program.runTests()


def main():
    (program := TestProgram()).parseArgs(sys.argv)
    count = program.workers
    if workerid := program.workerid:
        work(workerid, sys.argv, count)
        sys.exit(0) #TODO
    args = itertools.product(
        range(count), [sys.argv], [count]
    )
    procs = [
        mp.Process(target=work, args=args)
        for args in args
    ]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
