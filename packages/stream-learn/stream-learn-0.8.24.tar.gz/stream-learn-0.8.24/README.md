# stream-learn

[![CircleCI](https://circleci.com/gh/w4k2/stream-learn.svg?style=svg)](https://app.circleci.com/pipelines/github/w4k2/stream-learn)
[![codecov](https://codecov.io/gh/w4k2/stream-learn/branch/master/graph/badge.svg?token=B0CecEoaFi)](https://codecov.io/gh/w4k2/stream-learn)
[![Documentation Status](https://readthedocs.org/projects/stream-learn/badge/?version=latest)](http://stream-learn.readthedocs.io)
[![PyPI version](https://badge.fury.io/py/stream-learn.svg)](https://badge.fury.io/py/stream-learn)

![](docs/source/plots/hello.gif)

The `stream-learn` module is a set of tools necessary for processing data streams using `scikit-learn` estimators. The batch processing approach is used here, where the dataset is passed to the classifier in smaller, consecutive subsets called `chunks`. The module consists of five sub-modules:

- [`streams`](https://w4k2.github.io/stream-learn/streams.html) - containing a data stream generator that allows obtaining both stationary and dynamic distributions in accordance with various types of concept drift (also in the field of a priori probability, i.e. dynamically unbalanced data) and a parser of the standard ARFF file format.
- [`evaluators`](https://w4k2.github.io/stream-learn/evaluators.html) - containing classes for running experiments on stream data in accordance with the Test-Then-Train and Prequential methodology.
- [`classifiers`](https://w4k2.github.io/stream-learn/classifiers.html) - containing sample stream classifiers,
- [`ensembles`](https://w4k2.github.io/stream-learn/ensembles.html) - containing standard team models of stream data classification,
- [`utils`](https://w4k2.github.io/stream-learn/evaluators.html) - containing typical classification quality metrics in data streams.

You can read more about each module in the [documentation page](https://stream-learn.readthedocs.io/en/latest/).

## Citation policy

If you use stream-learn in a scientific publication, we would appreciate citation to the following paper:

<!-- ```
@article{ksieniewicz2020stream,
  title={stream-learn--open-source Python library for difficult data stream batch analysis},
  author={Ksieniewicz, Pawe{\l} and Zyblewski, Pawe{\l}},
  journal={arXiv preprint arXiv:2001.11077},
  year={2020}
}
``` -->

```
@article{Ksieniewicz2022,
  doi = {10.1016/j.neucom.2021.10.120},
  url = {https://doi.org/10.1016/j.neucom.2021.10.120},
  year = {2022},
  month = jan,
  publisher = {Elsevier {BV}},
  author = {P. Ksieniewicz and P. Zyblewski},
  title = {stream-learn {\textemdash} open-source Python library for difficult data stream batch analysis},
  journal = {Neurocomputing}
}
```

## Quick start guide

### Installation

To use the `stream-learn` package, it will be absolutely useful to install it. Fortunately, it is available in the *PyPI* repository, so you may install it using `pip`:

```shell
pip3 install -U stream-learn
```

`stream-learn` is also avaliable with `conda`:

```shell
conda install stream-learn -c w4k2 -c conda-forge
```

You can also install the module cloned from Github using the setup.py file if you have a strange, but perhaps legitimate need:

```shell
git clone https://github.com/w4k2/stream-learn.git
cd stream-learn
make install
```

### Preparing experiments

#### 1. Classifier

In order to conduct experiments, a declaration of four elements is necessary. The first is the estimator, which must be compatible with the `scikit-learn` API and, in addition, implement the `partial_fit()` method, allowing you to re-fit the already built model. For example, we'll use the standard *Gaussian Naive Bayes* algorithm:

```python
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
```

#### 2. Data Stream

The next element is the data stream that we aim to process. In the example we will use a synthetic stream consisting of shocking number of 100 chunks and containing precisely one concept drift. We will prepare it using the `StreamGenerator()` class of the `stream-learn` module:

```python
from strlearn.streams import StreamGenerator
stream = StreamGenerator(n_chunks=100, n_drifts=1)
```

#### 3. Metrics

The third requirement of the experiment is to specify the metrics used in the evaluation of the methods. In the example, we will use the *accuracy* metric available in `scikit-learn` and the *precision* from the `stream-learn` module:

```python
from sklearn.metrics import accuracy_score
from strlearn.metrics import precision
metrics = [accuracy_score, precision]
```

#### 4. Evaluator

The last necessary element of processing is the evaluator, i.e. the method of conducting the experiment. For example, we will choose the *Test-Then-Train* paradigm, described in more detail in [User Guide](https://w4k2.github.io/stream-learn/evaluators.html). It is important to note, that we need to provide the metrics that we will use in processing at the point of initializing the evaluator. In the case of none metrics given, it will use default pair of *accuracy* and *balanced accuracy* scores:

```python
from strlearn.evaluators import TestThenTrain
evaluator = TestThenTrain(metrics)
```

### Processing and understanding results

Once all processing requirements have been met, we can proceed with the evaluation. To start processing, call the evaluator's process method, feeding it with the stream and classifier::

```python
evaluator.process(stream, clf)
```

The results obtained are stored in the `scores` atribute of evaluator. If we print it on the screen, we may be able to observe that it is a three-dimensional numpy array with dimensions `(1, 29, 2)`.

- The first dimension is the **index of a classifier** submitted for processing. In the example above, we used only one model, but it is also possible to pass a tuple or list of classifiers that will be processed in parallel (See [User Guide](https://w4k2.github.io/stream-learn/evaluators.html)).
- The second dimension specifies the **instance of evaluation**, which in the case of *Test-Then-Train* methodology directly means the index of the processed chunk.
- The third dimension indicates the **metric** used in the processing.

Using this knowledge, we may finally try to illustrate the results of our simple experiment in the form of a plot::

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(6,3))

for m, metric in enumerate(metrics):
    plt.plot(evaluator.scores[0, :, m], label=metric.__name__)

plt.title("Basic example of stream processing")
plt.ylim(0, 1)
plt.ylabel('Quality')
plt.xlabel('Chunk')

plt.legend()
```

![](https://w4k2.github.io/stream-learn/_images/simplest.png)
