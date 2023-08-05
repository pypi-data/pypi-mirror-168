# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['samplics',
 'samplics.categorical',
 'samplics.datasets',
 'samplics.estimation',
 'samplics.regression',
 'samplics.sae',
 'samplics.sampling',
 'samplics.utils',
 'samplics.weighting']

package_data = \
{'': ['*'], 'samplics.datasets': ['data/*']}

install_requires = \
['matplotlib>=3.4,<4.0',
 'numpy>=1.21.4,<2.0.0',
 'pandas>=1.3,<2.0',
 'pydantic>=1.9,<2.0',
 'scipy>=1.7,<2.0',
 'statsmodels>=0.13.1,<0.14.0']

setup_kwargs = {
    'name': 'samplics',
    'version': '0.3.40',
    'description': 'Select, weight and analyze complex sample data',
    'long_description': '<img src="./img/samplics_logo.jpg" width="150" height="110" align="left" />\n\n# _Sample Analytics_\n\n[<img src="https://github.com/survey-methods/samplics/workflows/Testing/badge.svg">](https://github.com/survey-methods/samplics/actions?query=workflow%3ATesting)\n[<img src="https://github.com/survey-methods/samplics/workflows/Coverage/badge.svg">](https://github.com/survey-methods/samplics/actions?query=workflow%3ACoverage)\n[![docs](https://readthedocs.org/projects/samplics/badge/?version=latest)](https://samplics.readthedocs.io/en/latest/?badge=latest)\n[![DOI](https://joss.theoj.org/papers/10.21105/joss.03376/status.svg)](https://doi.org/10.21105/joss.03376)\n\nIn large-scale surveys, often complex random mechanisms are used to select samples. Estimates derived from such samples must reflect the random mechanism. _Samplics_ is a python package that implements a set of sampling techniques for complex survey designs. These survey sampling techniques are organized into the following four sub-packages.\n\n**Sampling** provides a set of random selection techniques used to draw a sample from a population. It also provides procedures for calculating sample sizes. The sampling subpackage contains:\n\n- Sample size calculation and allocation: Wald and Fleiss methods for proportions.\n- Equal probability of selection: simple random sampling (SRS) and systematic selection (SYS)\n- Probability proportional to size (PPS): Systematic, Brewer\'s method, Hanurav-Vijayan method, Murphy\'s method, and Rao-Sampford\'s method.\n\n**Weighting** provides the procedures for adjusting sample weights. More specifically, the weighting subpackage allows the following:\n\n- Weight adjustment due to nonresponse\n- Weight poststratification, calibration and normalization\n- Weight replication i.e. Bootstrap, BRR, and Jackknife\n\n**Estimation** provides methods for estimating the parameters of interest with uncertainty measures that are consistent with the sampling design. The estimation subpackage implements the following types of estimation methods:\n\n- Taylor-based, also called linearization methods\n- Replication-based estimation i.e. Boostrap, BRR, and Jackknife\n- Regression-based e.g. generalized regression (GREG)\n\n**Small Area Estimation (SAE).** When the sample size is not large enough to produce reliable / stable domain level estimates, SAE techniques can be used to model the output variable of interest to produce domain level estimates. This subpackage provides Area-level and Unit-level SAE methods.\n\nFor more details, visit https://samplics.readthedocs.io/en/latest/\n\n## Usage\n\nLet\'s assume that we have a population and we would like to select a sample from it. The goal is to calculate the sample size for an expected proportion of 0.80 with a precision (half confidence interval) of 0.10.\n\n> ```python\n> from samplics.sampling import SampleSize\n>\n> sample_size = SampleSize(parameter = "proportion")\n> sample_size.calculate(target=0.80, half_ci=0.10)\n> ```\n\nFurthermore, the population is located in four natural regions i.e. North, South, East, and West. We could be interested in calculating sample sizes based on region specific requirements e.g. expected proportions, desired precisions and associated design effects.\n\n> ```python\n> from samplics.sampling import SampleSize\n>\n> sample_size = SampleSize(parameter="proportion", method="wald", stratification=True)\n>\n> expected_proportions = {"North": 0.95, "South": 0.70, "East": 0.30, "West": 0.50}\n> half_ci = {"North": 0.30, "South": 0.10, "East": 0.15, "West": 0.10}\n> deff = {"North": 1, "South": 1.5, "East": 2.5, "West": 2.0}\n>\n> sample_size = SampleSize(parameter = "proportion", method="Fleiss", stratification=True)\n> sample_size.calculate(target=expected_proportions, half_ci=half_ci, deff=deff)\n> ```\n\nTo select a sample of primary sampling units using PPS method,\nwe can use code similar to the snippets below. Note that we first use the `datasets` module to import the example dataset.\n\n> ```python\n> # First we import the example dataset\n> from samplics.datasets import load_psu_frame\n> psu_frame_dict = load_psu_frame()\n> psu_frame = psu_frame_dict["data"]\n>\n> # Code for the sample selection\n> from samplics.sampling import SampleSelection\n>\n> psu_sample_size = {"East":3, "West": 2, "North": 2, "South": 3}\n> pps_design = SampleSelection(\n>    method="pps-sys",\n>    stratification=True,\n>    with_replacement=False\n>    )\n>\n> psu_frame["psu_prob"] = pps_design.inclusion_probs(\n>    psu_frame["cluster"],\n>    psu_sample_size,\n>    psu_frame["region"],\n>    psu_frame["number_households_census"]\n>    )\n> ```\n\nThe initial weighting step is to obtain the design sample weights. In this example, we show a simple example of two-stage sampling design.\n\n> ```python\n> import pandas as pd\n>\n> from samplics.datasets import load_psu_sample, load_ssu_sample\n> from samplics.weighting import SampleWeight\n>\n> # Load PSU sample data\n> psu_sample_dict = load_psu_sample()\n> psu_sample = psu_sample_dict["data"]\n>\n> # Load PSU sample data\n> ssu_sample_dict = load_ssu_sample()\n> ssu_sample = ssu_sample_dict["data"]\n>\n> full_sample = pd.merge(\n>     psu_sample[["cluster", "region", "psu_prob"]],\n>     ssu_sample[["cluster", "household", "ssu_prob"]],\n>     on="cluster"\n> )\n>\n> full_sample["inclusion_prob"] = full_sample["psu_prob"] * full_sample["ssu_prob"]\n> full_sample["design_weight"] = 1 / full_sample["inclusion_prob"]\n> ```\n\nTo adjust the design sample weight for nonresponse,\nwe can use code similar to:\n\n> ```python\n> import numpy as np\n>\n> from samplics.weighting import SampleWeight\n>\n> # Simulate response\n> np.random.seed(7)\n> full_sample["response_status"] = np.random.choice(\n>     ["ineligible", "respondent", "non-respondent", "unknown"],\n>     size=full_sample.shape[0],\n>     p=(0.10, 0.70, 0.15, 0.05),\n> )\n> # Map custom response statuses to teh generic samplics statuses\n> status_mapping = {\n>    "in": "ineligible",\n>    "rr": "respondent",\n>    "nr": "non-respondent",\n>    "uk":"unknown"\n>    }\n> # adjust sample weights\n> full_sample["nr_weight"] = SampleWeight().adjust(\n>    samp_weight=full_sample["design_weight"],\n>    adjust_class=full_sample["region"],\n>    resp_status=full_sample["response_status"],\n>    resp_dict=status_mapping\n>    )\n> ```\n\nTo estimate population parameters using Taylor-based and replication-based methods, we can use code similar to:\n\n> ```python\n> # Taylor-based\n> from samplics.datasets import load_nhanes2\n>\n> nhanes2_dict = load_nhanes2()\n> nhanes2 = nhanes2_dict["data"]\n>\n> from samplics.estimation import TaylorEstimator\n>\n> zinc_mean_str = TaylorEstimator("mean")\n> zinc_mean_str.estimate(\n>     y=nhanes2["zinc"],\n>     samp_weight=nhanes2["finalwgt"],\n>     stratum=nhanes2["stratid"],\n>     psu=nhanes2["psuid"],\n>     remove_nan=True,\n> )\n>\n> # Replicate-based\n> from samplics.datasets import load_nhanes2brr\n>\n> nhanes2brr_dict = load_nhanes2brr()\n> nhanes2brr = nhanes2brr_dict["data"]\n>\n> from samplics.estimation import ReplicateEstimator\n>\n> ratio_wgt_hgt = ReplicateEstimator("brr", "ratio").estimate(\n>     y=nhanes2brr["weight"],\n>     samp_weight=nhanes2brr["finalwgt"],\n>     x=nhanes2brr["height"],\n>     rep_weights=nhanes2brr.loc[:, "brr_1":"brr_32"],\n>     remove_nan=True,\n> )\n>\n> ```\n\nTo predict small area parameters, we can use code similar to:\n\n> ```python\n> import numpy as np\n> import pandas as pd\n>\n> # Area-level basic method\n> from samplics.datasets import load_expenditure_milk\n>\n> milk_exp_dict = load_expenditure_milk()\n> milk_exp = milk_exp_dict["data"]\n>\n> from samplics.sae import EblupAreaModel\n>\n> fh_model_reml = EblupAreaModel(method="REML")\n> fh_model_reml.fit(\n>     yhat=milk_exp["direct_est"],\n>     X=pd.get_dummies(milk_exp["major_area"], drop_first=True),\n>     area=milk_exp["small_area"],\n>     error_std=milk_exp["std_error"],\n>     intercept=True,\n>     tol=1e-8,\n> )\n> fh_model_reml.predict(\n>     X=pd.get_dummies(milk_exp["major_area"], drop_first=True),\n>     area=milk_exp["small_area"],\n>     intercept=True,\n> )\n>\n> # Unit-level basic method\n> from samplics.datasets import load_county_crop, load_county_crop_means\n>\n> # Load County Crop sample data\n> countycrop_dict = load_county_crop()\n> countycrop = countycrop_dict["data"]\n> # Load County Crop Area Means sample data\n> countycropmeans_dict = load_county_crop_means()\n> countycrop_means = countycropmeans_dict["data"]\n>\n> from samplics.sae import EblupUnitModel\n>\n> eblup_bhf_reml = EblupUnitModel()\n> eblup_bhf_reml.fit(\n>     countycrop["corn_area"],\n>     countycrop[["corn_pixel", "soybeans_pixel"]],\n>     countycrop["county_id"],\n> )\n> eblup_bhf_reml.predict(\n>     Xmean=countycrop_means[["ave_corn_pixel", "ave_corn_pixel"]],\n>     area=np.linspace(1, 12, 12),\n> )\n>\n> ```\n\n## Installation\n\n`pip install samplics`\n\nPython 3.7 or newer is required and the main dependencies are [numpy](https://numpy.org), [pandas](https://pandas.pydata.org), [scpy](https://www.scipy.org), and [statsmodel](https://www.statsmodels.org/stable/index.html).\n\n## Contribution\n\nIf you would like to contribute to the project, please read [contributing to samplics](https://github.com/samplics-org/samplics/blob/main/CONTRIBUTING.md)\n\n## License\n\n[MIT](https://github.com/survey-methods/samplics/blob/master/license.txt)\n\n## Contact\n\ncreated by [Mamadou S. Diallo](https://twitter.com/MamadouSDiallo) - feel free to contact me!\n',
    'author': 'Mamadou S Diallo',
    'author_email': 'msdiallo@samplics.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://samplics.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
