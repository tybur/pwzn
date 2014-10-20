# -*- coding: utf-8 -*-
import pickle
import unittest
import math


class TestClass(unittest.TestCase):

    TESTED_MODULE = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Integrator = cls.TESTED_MODULE.Integrator

    def test_sin(self):
        for ii in range(2, 12):
            with self.subTest(ii):
                integrator = self.Integrator(ii)
                self.assertAlmostEqual(0, integrator.integrate(math.sin, (0, math.pi*2), 30))

    def test_xsquared(self):
        for ii in range(2, 12):
            with self.subTest(ii):
                integrator = self.Integrator(ii)
                self.assertAlmostEqual(1/3, integrator.integrate(lambda x: x*x, (0, 1), 40), places=min(ii-1, 7))
