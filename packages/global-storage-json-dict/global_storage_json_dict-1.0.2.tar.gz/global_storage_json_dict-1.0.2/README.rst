========================
global_storage_json_dict
========================

Description
===========

Добавляет возможность глобально управлять объектом dict сохраняя его в файл

Installation
============

(PyPi)

.. code-block:: bash

    pip install global_storage_json_dict

Usage
=====

example global storage

.. code-block:: python

    from global_storage_json_dict import Storage import
    def f(n):
        return (((n+1)*n) // 2) + 1
    for i in range(40, 100):
        if str(i) not in Storage:
            Storage[str(i)] = f(i)
        if i == 10:
            break

example factory

.. code-block:: python

    from global_storage_json_dict import FileJsonStorage
    storage = FileJsonStorage(file="store.json" auto_save=False)
    storage.get('a')  # Get value by key default None
    storage['a'] = 1  # Set value
    storage['b'] = 2
    'a' in storage
    storage.save()  # Save storage