# pybatch
Framework  for easy parallel processing of python code.

Allows you to easily run the your python code on multiple cores of your machine.

## Installation

pip install pybatch

or Download from

https://pypi.python.org/pypi/pybatch/0.1

## Usage

* Import the necessary files
```python
from pybatch.executor import Parallelize, JobExecutor, PipedJobExecutor, DEFAULT_PARTITION_KEY
from pybatch.partitioner import SimpleListPartitioner
from pybatch.result import ListResultManager
from pybatch.data_proxy import ListDataProxy
```
### Create a holder for your data. Extend DataProxy to represent different types of data.

```python
data = ListDataProxy(data=[i for i in range(100)])
```
### Create a holder for you results. Extend ResultManager to process the result as you wish. 

```python
result_manager = ListResultManager()
```
### Process the data on multiple cores

#### Using the JobExecutor API

* Create your data processing function. Use "DEFAULT_PARTITION_KEY" to get data from the kwargs. Example

```python
def test_worker(*args, **kwargs):
    data = kwargs[DEFAULT_PARTITION_KEY]
    # Actual processing
    return [i*i for i in data]

```

* Create a JobExecutor instance with your data processing function as worker and call execute on it.

```python
# You can extend DataPartitioner class create your custom partitioner.
result = PipedJobExecutor(worker=test_worker,
                            data_partitioner=SimpleListPartitioner(data_proxy=Data, processors=4),
                            result_manager=ListResultManager()).execute().show_results()
```

#### Using the "@Parallelize" Decorator

* Create your processing function and add decorate it with "@Parallelize". Use "DEFAULT_PARTITION_KEY" to get data from the kwargs

```python
# You can extend DataPartitioner class create your custom partitioner.
@Parallelize(executor_type=ExecutorCommType.pipe,
             result_manager=result_manager,
             data_partitioner=SimpleListPartitioner(data_proxy=data, processors=4))
def test_worker(*args, **kwargs):
    data = kwargs[DEFAULT_PARTITION_KEY]
    # Actual processing
    return [i*i for i in data]
```
#### Using "@Parallelize" with executor factory to create job executor once and parallelize multiple functions.

```python
def executor_factory():
    partitioner = SimpleListPartitioner(processors=4, data_proxy=data)
    return PipedJobExecutor(data_partitioner=partitioner, result_manager=result_manager)
    
@Parallelize(executor_factory=executor_factory)
def test_worker(*args, **kwargs):
    data = kwargs[DEFAULT_PARTITION_KEY]
    # Actual processing
    return [i*i for i in data]

@Parallelize(executor_factory=executor_factory)
def test_worker1(*args, **kwargs):
    data = kwargs[DEFAULT_PARTITION_KEY]
    # Actual processing
    return [i*i*i for i in data]
 
```

* Call the function and use the result

```python
for i in test_worker().show_results():
    print(i.result)
for i in test_worker1().show_results():
    print(i.result)
```

## Samples coming soon.
