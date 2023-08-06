# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['casual_inference', 'casual_inference.dataset', 'casual_inference.evaluator']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.2,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'plotly>=5.10.0,<6.0.0',
 'scipy>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'casual-inference',
    'version': '0.2.0',
    'description': '',
    'long_description': '[![ci](https://github.com/shyaginuma/casual_inference/actions/workflows/config.yml/badge.svg)](https://github.com/shyaginuma/casual_inference/actions/workflows/config.yml)\n[![PyPI version](https://badge.fury.io/py/casual_inference.svg)](https://badge.fury.io/py/casual_inference)\n\n# casual_inference\n\nThe `casual_inference` is a Python package provides a simple interface to do causal inference.\nDoing causal analyses is a complicated stuff. We have to pay attention to many things to do such analyses properly.\nThe `casual_inference` is developed aiming to reduce such effort.\n\n## Installation\n\n```shell\npip install casual-inference\n```\n\n## Overview\n\nThis package will provide several types of **`evaluator`**. They have `evaluate()` and some `summary_xxx()` methods. The `evaluate()` method evaluates treatment impact by calculating several statistics in it, and the `summary_xxx()` methods summarize such statistics in some ways. (e.g., table style, bar chart style, ...)\n\nThe `evaluate()` method expects that the data which has a schema like as follows will be passed.\n\n|unit|variant|metric_A|metric_B|...|\n|----|-------|--------|--------|---|\n|1   |1      |0       |0.01    |...|\n|2   |1      |1       |0.05    |...|\n|3   |2      |0       |0.02    |...|\n|... |...    |...     |...     |...|\n\nThe table has been already aggregated by the `unit` column. (i.e. The `unit` column should be the primary key)\n\n### Columns\n\n- `unit`: The unit you want to conduct analysis on. Typically it will be user_id, session_id, ... in the web service domain.\n- `variant`: The group of intervention. This package always assumes `1` is a variant of control group.\n- `metrics`: metrics you want to evaluate. e.g., The number of purchases, conversion rate, ...\n\n## Quick Start\n\nThe current version of `casual_inference` only supports evaluation of A/B testing and A/A testing.\n\n### A/B test evaluation\n\n```python\nfrom casual_inference.dataset import create_sample_ab_result\nfrom casual_inference.evaluator import ABTestEvaluator\n\ndata = create_sample_ab_result(n_variant=3, sample_size=1000000, simulated_lift=[-0.01, 0.01])\n\nevaluator = ABTestEvaluator()\nevaluator.evaluate(\n    data=data,\n    unit_col="rand_unit",\n    variant_col="variant",\n    metrics=["metric_bin", "metric_cont"]\n)\n\nevaluator.summary_barplot()\n```\n\n![eval_result](examples/images/plot_abtestevaluator_result.png)\n\nYou can also see the [example notebook](https://github.com/shyaginuma/casual_inference/blob/main/examples/ab_test_evaluator.ipynb) to see more detailed example.\n\n### A/A test evaluation\n\n```python\nfrom casual_inference.dataset import create_sample_ab_result\nfrom casual_inference.evaluator import AATestEvaluator\n\ndata = create_sample_ab_result(n_variant=2, sample_size=1000000, simulated_lift=[0.0])\n\nevaluator = AATestEvaluator()\nevaluator.evaluate(\n    data=data,\n    unit_col="rand_unit",\n    metrics=["metric_bin", "metric_cont"]\n)\n\nevaluator.summary_plot()\n```\n\n![eval_result](examples/images/plot_aatestevaluator_result.png)\n\nYou can also see the [example notebook](https://github.com/shyaginuma/casual_inference/blob/main/examples/aa_test_evaluator.ipynb) to see more detailed example.\n\n## References\n\n- Kohavi, Ron, Diane Tang, and Ya Xu. 2020. \u200bTrustworthy Online Controlled Experiments: A Practical Guide to A/B Testing. Cambridge University Press. https://experimentguide.com/\n  - A Great book covering comprehensive topics around practical A/B testing. I do recommend to read this book for all people who works on A/B testing.\n- Alex Deng, Ulf Knoblich, and Jiannan Lu. 2018. Applying the Delta Method in Metric Analytics: A Practical Guide with Novel Ideas. In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (KDD \'18). Association for Computing Machinery, New York, NY, USA, 233–242. https://doi.org/10.1145/3219819.3219919\n  - Describing how to approximate variance of relative difference, and when the analysis unit was more granular than the randomization unit.\n',
    'author': 'yaginuuun',
    'author_email': 'yaginuuun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shyaginuma',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
