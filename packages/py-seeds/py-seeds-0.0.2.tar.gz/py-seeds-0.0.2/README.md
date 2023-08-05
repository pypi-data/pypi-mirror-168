# Seed function (random, torch, torch.cuda)
- seed_everything
- get_seed_state
- set_seed_state
## seed_everything
```python
from py_seeds import seed_everything

seed_everything(0)
```

## get_seed_state
```python
import torch

from py_seeds import get_seed_state


state = get_seed_state()

torch.save(state, 'seeds.pth')
```
## set_seed_state
```python
import torch

from py_seeds import set_seed_state


state = torch.load('seeds.pth')

set_seed_state(state)
```