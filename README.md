# pybatch
Framework  to simplify multi-core processing in python.

## Installation

pip install pybatch

or Download from

https://pypi.python.org/pypi/pybatch/0.1

## Usage

### Create a holder for your data. Extend DataProxy to represent different types of data.

```python
from pybatch.data_proxy import ListDataProxy

data = ListDataProxy(data=[i for i in range(100)])
```

### Create a Partitioner for your data. You can extend DataPartitioner class to create your custom partitioner.

```python
from pybatch.partitioner import SimpleListPartitioner

partitioner = SimpleListPartitioner(data_proxy=Data, processors=4)
```

### Create a holder for the results. Extend ResultManager to process the result as you wish.

```python
from pybatch.result import ListResultManager

result_manager = ListResultManager()
```
### Process the data on multiple cores

#### Using the JobExecutor API

* Create your data processing function. Use "DEFAULT_PARTITION_KEY" to get data from the kwargs. Example

```python
from pybatch.executor import DEFAULT_PARTITION_KEY

def test_worker(*args, **kwargs):
    data = kwargs[DEFAULT_PARTITION_KEY]
    # Actual processing
    return [i*i for i in data]

```

* Create a JobExecutor instance with your data processing function as worker and call execute on it.

```python
from pybatch.executor import PipedJobExecutor

result = PipedJobExecutor(worker=test_worker, data_partitioner=partitioner,
                            result_manager=result_manager).execute().show_results()
```

#### Using the "@Parallelize" Decorator

* Create your processing function and decorate it with "@Parallelize". Use "DEFAULT_PARTITION_KEY" to get data from the kwargs

```python
from pybatch.executor import Parallelize, ExecutorCommType, DEFAULT_PARTITION_KEY

@Parallelize(executor_type=ExecutorCommType.pipe, data_partitioner=partitioner, result_manager=result_manager)
def test_worker(*args, **kwargs):
    data = kwargs[DEFAULT_PARTITION_KEY]
    # Actual processing
    return [i*i for i in data]
```
#### Using "@Parallelize" with executor factory to create job executor once and parallelize multiple functions.


* Create a function that returns a JobExecutor and decorate the worker functions with it.

```python
def executor_factory():
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

* Or create an ExecutorFactory class that returns a JobExecutor and decorate the worker functions with it.

```python
from pybatch.executor import ExecutorFactory

class MyExecutorFactory(ExecutorFactory):

    def __init__(self, arg1, arg2):
        pass

    def executor(self):
        partitioner = SimpleListPartitioner(processors=4, data_proxy=data)
        return PipedJobExecutor(data_partitioner=partitioner, result_manager=result_manager)


@Parallelize(executor_factory=MyExecutorFactory)
def test_worker(*args, **kwargs):
    data = kwargs[DEFAULT_PARTITION_KEY]
    # Actual processing
    return [i*i for i in data]

@Parallelize(executor_factory=MyExecutorFactory)
def test_worker1(*args, **kwargs):
    data = kwargs[DEFAULT_PARTITION_KEY]
    # Actual processing
    return [i*i*i for i in data]

```

* Call the worker function and use the result

```python
for i in test_worker().show_results():
    print(i.result)
for i in test_worker1().show_results():
    print(i.result)
```

## Samples coming soon.
