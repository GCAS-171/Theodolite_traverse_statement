'''

__init__.py помечает каталоги как каталоги пакетов Python. Обычная практика — оставлять __init__.py пустыми. Тем не менее во многих библиотеках, которые я читал, были непустые, а иногда длинные файлы __init__.py. Это заставило меня задуматься, что и почему можно добавить в __init__.py.

Во-первых, мы можем добавить в __init__.py импорт, когда хотим реорганизовать код, который вырос в несколько модулей, без критических изменений для существующих пользователей. Допустим, у нас есть один модуль (models.py), который содержит реализацию для DecisionTree и Bandit. Со временем этот единственный модуль превращается в пакет моделей с модулями для tree и bandit. Чтобы обеспечить согласованность API для существующих пользователей, в __init__.py в пакете моделей мы можем добавить следующее:

```python
from .tree import DecisionTree, RandomForest
from .bandit import Bandit, TSBandit
```

Это гарантирует, что существующие пользователи смогут продолжить импорт через from models import DecisionTree, а не from models.tree import DecisionTree. Для них API не меняется, а существующий код не ломается.

Это подводит к ещё одной причине добавить код в __init__.py, а именно — предоставить упрощённый API, чтобы пользователям не приходилось вникать в детали реализации:

app
│
├── __init__.py
├── dmodel_implementation.py
└── data_implementation.py

Вместо того чтобы заставлять пользователей решать, что импортировать из model_implementation и data_implementation, мы можем всё упростить, добавив в __init__.py такой код:

```python
from .model_implementation import SimpleModel
from .data_implementation import SimpleDataLoader
```

В нём говорится, что SimpleModel и SimpleDataLoader — единственные части приложения, с которыми должны работать пользователи, и это упрощает использование пакета приложения (например, from app import SimpleModel, SimpleDataLoader). И, если пользователи знают, что делают, и хотят импортировать напрямую из model_implementation, то это тоже возможно.

Так делается в Pandas, где __init__.py импортируются типы данных, считыватели (reader) и API изменения формы, а ещё так делается в Accelerate от Hugging Face.

Помимо упомянутого выше применения, мы также можем захотеть:

* инициализировать логгер в __init__.py основного пакета, чтобы использовать его в нескольких модулях;
* выполнить проверки совместимости [как в Pandas](https://pandas.pydata.org/pandas-docs/stable/development/extending.html][https://github.com/psf/requests/blob/main/src/requests/__init__.py]


'''