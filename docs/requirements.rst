# Installation and Setup for Sphinx Documentation

1. Установите Sphinx:

```bash
pip install sphinx sphinx-autodoc-typehints
```

2. Перейдите в директорию docs и инициализируйте Sphinx:

```bash
cd docs
sphinx-quickstart
```

3. Добавьте пути к модулям в конфигурационный файл conf.py.

4. Для генерации документации выполните команду:

```bash
make html  # для создания HTML документации 
```

