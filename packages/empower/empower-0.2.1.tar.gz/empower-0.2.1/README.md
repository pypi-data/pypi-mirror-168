# empower

Goodbye Inheritance!!!

## Install

```python
pip install empower
```

## Usage

You have a `Duck` class without any methods.

```python
# mod/__init__.py

class Duck:
    ...
```

You define a trait `Fly` for `Duck`
```python
# mod/fly.py

from empower import impl, Trait

from . import Duck

@impl(Duck)
class Fly(Trait):
    def fly(self):
        return "fly"
```

And you define another trait `Run` for `Duck`
```python
# mod/run.py

from empower import impl, Trait

from . import Duck


@impl(Duck)
class Run(Trait):
    def run(self):
        return "run"
```

Now you can add empower `Duck`
```python
# main.py

from mod import Duck
from empower import use

duck = Duck()

use("mod.fly")  # load fly trait
use("mod.run")  # load run trait

assert duck.fly() == "fly"
assert duck.run() == "run"
```