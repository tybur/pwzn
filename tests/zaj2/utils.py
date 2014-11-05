# -*- coding: utf-8 -*-

import argparse
import importlib
import unittest


def launch_test_suite():

    parser = argparse.ArgumentParser(description='Launch tests')
    parser.add_argument('--zaj', default=2, type=int)
    parser.add_argument('--solution', default=False, action="store_true")
    parser.add_argument('--no', type=int, default=1)
    parser.add_argument('--data-dir', type=str, default='/opt/pwzn/')
    parser.add_argument('--short', default=False, action="store_true")
    args = parser.parse_args()

    if args.solution:
        package = "solutions"
    else:
        package = "tasks"

    module_name = "{}.zaj{}.zadanie{}".format(package, args.zaj, args.no)

    module = importlib.import_module(module_name)
    test_module = importlib.import_module("tests.zaj{}.zadanie{}".format(args.zaj, args.no))

    clazz = test_module.TestClass

    clazz.TESTED_MODULE = module
    clazz.DATA_DIR = args.data_dir
    clazz.SHORT = args.short

    ts = unittest.defaultTestLoader.loadTestsFromTestCase(clazz)
    tr = unittest.TextTestRunner()
    tr.run(ts)
