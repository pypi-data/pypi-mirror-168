# Gistats
*Gistats* is a small library for generating **Statistics** on **Gists** using dictionaries<br>
based on [@sciencepal chess.com statistics](https://github.com/sciencepal/chess-com-box-py)

# Installation
```python
# Unstable
pip install git+https://github.com/ZSendokame/Gistats.git

# Stable
pip install Gistats 
```

# How to use
```py
import os
import gistats

def get_size():
    size = 0

    for element in os.scandir('./gistats'):
        size += os.stat(element).st_size

    return size

statistics = {
    'Total size': {'value': str(get_size()), 'emoji': '💾'},
    'Gistats Version': {'value': '1.0.0', 'emoji': '✔'}
}
gist = gistats.Login('name', 'gist-token', 'gist-id')

# Separator is the character that will separate Statistic name from its value.
# Until is the maximum of characters on the string, so it gets at the same column.
gist.update(statistics, separator=':', until=30)  # Return Status Code.
# https://gist.github.com/ZSendokame/4637229c389a70083784eac6d4adc1f4
```