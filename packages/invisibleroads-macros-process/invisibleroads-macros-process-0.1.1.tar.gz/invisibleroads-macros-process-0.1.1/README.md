# Shortcut Functions for Process Operations

## Install

```bash
pip install invisibleroads-macros-process
```

## Use

```python
import logging
from invisibleroads_macros_process import LoggableProcess, StoppableProcess

logging.basicConfig(level=logging.DEBUG)

def f():
    print('whee')

process = LoggableProcess(name='MY-LOGGABLE', target=f, daemon=True)
process.start()

process = StoppableProcess(name='MY-STOPPABLE', target=f, daemon=True)
process.start()
process.stop()
```

## Test

```bash
git clone https://github.com/invisibleroads/invisibleroads-macros-process
cd invisibleroads-macros-process
pip install -e .[test]
pytest --cov=invisibleroads_macros_process --cov-report term-missing tests
```
