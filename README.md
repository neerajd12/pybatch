# pybatch
Library for easy parallel processing of python code.

Allows you to easily run the your python code on multiple cores of your machine.

## Installation

pip install pybatch

or Download from

https://pypi.python.org/pypi/pybatch/0.1

## Usage

* Import the necessary files
```code
from pybatch.executor import DEFAULT_PARTITION_KEY, Parallelize, PipedJobExecutor, ExecutorCommType
from pybatch.partitioner import SimpleListPartitioner
from pybatch.results import ListResultManager, JobResult, JobSuccess, JobError
```

### Using the JobExecutor API

* Create your processing function. Use "DEFAULT_PARTITION_KEY" to get data from the kwargs. Example

```python
def test_worker(*args, **kwargs):
    data = kwargs[DEFAULT_PARTITION_KEY]
    # Actual processing
    return [i*i for i in data]

```

* Create a JobExecutor instance with your worker function and call execute on it.

```python
# You can extend DataPartitioner class create your custom partitioner.
# Extend ResultManager to process the result as you wish. 
result = PipedJobExecutor(worker=test_worker,
                            data_partitioner=SimpleListPartitioner(data_proxy=Data, processors=4),
                            result_manager=ListResultManager()).execute().show_results()
```

### Using the Decorator

* Create your processing function and add decorate it with "@Parallelize" decorator. Use "DEFAULT_PARTITION_KEY" to get data from the kwargs

```python
# You can extend DataPartitioner class create your custom partitioner.
# Extend ResultManager to process the result as you wish. 
@Parallelize(executor_type=ExecutorCommType.pipe,
             data_partitioner=SimpleListPartitioner(data_proxy=Data, processors=4),
             result_manager=ListResultManager())
def test_worker(*args, **kwargs):
    data = kwargs[DEFAULT_PARTITION_KEY]
    # Actual processing
    return [i*i for i in data]
    
# or create a job factory and return your own

```

* Call the function and use the result

```python
result = test_worker().show_results()
```

## Samples coming soon.
