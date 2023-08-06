======================
lyseum_hack_ege_client
======================

Description
===========

Добавляет возможность сохранять файлы из хранилища

Installation
============

(PyPi)

.. code-block:: bash

    pip install lyseum_hack_ege_client

Usage
=====

Получим все баркоды существующие в базе

.. code-block:: python

    from lyseum_hack_ege_client import Client
    codes = Client.all_barcodes()
    print(codes)
    >>>> ['1234567890123', '1234567890124']

Сохраним файлы документов по одному баркоду

.. code-block:: python

    from lyseum_hack_ege_client import Client
    files = Client.barcode('1234567890123')
    >>>> ["<YaSimpleFile filename='4.jpg' path='resource/detect/1234567890123/4.jpg'>"]
    for file in files:
        print(file.name)
        >>>> 4.jpg
        print(file.fullpath)
        >>>> resource/detect/1234567890123/4.jpg
        file.save()  # Здесь фактическое сохранение файла.


Другой способ сохранения файлов

.. code-block:: python

    from lyseum_hack_ege_client import Client
    files = Client.barcode('1234567890123')
    Client.save_files(files)  # Последовательно скачаются файлы

Сохранение всех картинок из директории all

.. code-block:: python

    from lyseum_hack_ege_client import Client
    files = Client.barcode('1234567890123')
    paths = Client.synchronize_all()
    print(paths)
    >>>> ['resource/all/1.jpg', 'resource/all/2.jpg', 'resource/all/3.jpg']