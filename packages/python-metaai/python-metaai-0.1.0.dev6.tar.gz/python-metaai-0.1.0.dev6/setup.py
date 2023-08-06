# -*- coding: utf-8 -*-
from setuptools import setup


EXTRAS_REQUIRE = {
    "lightgbm": ["lightgbm"],
    "pmml": ["pmml"],
    "sklearn": ["scikit-learn"],
    "torch": ["torch"],
    "xgboost": ["xgboost"],
    "base": ["serving"],
    "serving": [],
    "pipeline": [],
}


setup(extras_require=EXTRAS_REQUIRE)
