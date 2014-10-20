# -*- coding: utf-8 -*-

import argparse
import importlib
import unittest


def launch_test_suite():

    parser = argparse.ArgumentParser(description='Launch tests')
    parser.add_argument('--solution', default=False, action="store_true")
    parser.add_argument('--no', type=int, default=1)
    args = parser.parse_args()

    if args.solution:
        package = "solutions"
    else:
        package = "tasks"

    module_name = "{}.zaj2.zadanie{}".format(package, args.no)

    module = importlib.import_module(module_name)
    test_module = importlib.import_module("tests.zaj2.zadanie{}".format(args.no))

    clazz = test_module.TestClass

    clazz.TESTED_MODULE = module

    ts = unittest.defaultTestLoader.loadTestsFromTestCase(clazz)
    tr = unittest.TextTestRunner()
    tr.run(ts)
