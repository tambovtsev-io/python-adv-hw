# HW01 CLI Tools
Вам нужно реализовать CLI приложения, кроме кода, вам необходимо в качестве артефактов приложить текстовый файл, как вы проверяли работоспособность вашего кода (просто копия команд и выводов из терминала)

## Task 1.1
Написать упрощенный вариант утилиты `nl` -- скрипт, который выдает в `stdout` пронумерованные строки из файла.
Если файл не передан, то скрипт читает строки из `stdin`.

Он должен работать так же, как `nl -b a`.

### Outputs
Замечание: я добавил CLI в путь через `pyproject.toml` и `uv pip install -e .`

```
>>> nl --help
NAME
    nl - Write each FILE to standard output, with line numbers added.

SYNOPSIS
    nl <flags>

DESCRIPTION
    Write each FILE to standard output, with line numbers added.

FLAGS
    -f, --filename=FILENAME
        Type: Optional[Optional]
        Default: None
        Optional path to input file. If None, reads from stdin
```

```
>>> nl inputs/zen_of_python.txt
     1  Beautiful is better than ugly.
     2  Explicit is better than implicit.
     3  Simple is better than complex.
     4  Complex is better than complicated.
     5  Flat is better than nested.
     6  Sparse is better than dense.
     7  Readability counts.
     8  Special cases aren't special enough to break the rules.
     9  Although practicality beats purity.
    10  Errors should never pass silently.
    11  Unless explicitly silenced.
    12  In the face of ambiguity, refuse the temptation to guess.
    13  There should be one-- and preferably only one --obvious way to do it.
    14  Although that way may not be obvious at first unless you're Dutch.
    15  Now is better than never.
    16  Although never is often better than *right* now.
    17  If the implementation is hard to explain, it's a bad idea.
    18  If the implementation is easy to explain, it may be a good idea.
    19  Namespaces are one honking great idea -- let's do more of those!
```

```
>>> nl
hello
     1  hello
world
     2  world
copy paste lines: Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
     3  copy paste lines: Beautiful is better than ugly.
     4  Explicit is better than implicit.
     5  Simple is better than complex.
```


## Task 1.2
Написать упрощенный вариант утилиты `tail` -- скрипт, выводящий в `stdout` последние 10 строк каждого из переданных файлов.

- если передано больше одного файла, то перед обработкой очередного файла необходимо вывести его имя. Подробности смотрите в оригинальной утилите `tail`, ваш скрипт должен повторять форматирование.
- если не передано ни одного файла, то нужно вывести последние 17 строк из `stdin`.

```
>>> tail --help
NAME
    tail - Print the last 10 lines of each FILE to standard output.

SYNOPSIS
    tail [FILENAMES]...

DESCRIPTION
    Print the last 10 lines of each FILE to standard output.

POSITIONAL ARGUMENTS
    FILENAMES
        Type: str
```

```
>>> tail inputs/zen_of_python.txt
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

```
>>> tail
tail
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!

### Separation comment -- wasn't present in the original output ###
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

```
>>> tail inputs/zen_of_python.txt inputs/lorem.txt
==> inputs/zen_of_python.txt <==
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!

==> inputs/lorem.txt <==
nec tincidunt. Dapibus nunc porttitor aenean quis class tortor. Suscipit dui eu
diam varius a. Vulputate molestie pellentesque aenean lacus enim non.

Rhoncus sapien facilisi tellus maecenas vestibulum magnis tristique ornare. Ante
duis imperdiet diam nec feugiat primis condimentum. Sem orci leo lobortis
hendrerit consequat interdum ultrices aptent quam. Efficitur tempor ante;
cubilia natoque commodo adipiscing ipsum mi. Habitant rhoncus natoque fames
facilisis himenaeos tempor sapien. Fusce laoreet mus euismod fusce himenaeos
maecenas sociosqu. Ullamcorper molestie himenaeos a cubilia pharetra leo.
Potenti arcu felis felis non elementum vivamus orci.
```

Combo:
```
>>> tail inputs/zen_of_python.txt | nl
     1  Errors should never pass silently.
     2  Unless explicitly silenced.
     3  In the face of ambiguity, refuse the temptation to guess.
     4  There should be one-- and preferably only one --obvious way to do it.
     5  Although that way may not be obvious at first unless you're Dutch.
     6  Now is better than never.
     7  Although never is often better than *right* now.
     8  If the implementation is hard to explain, it's a bad idea.
     9  If the implementation is easy to explain, it may be a good idea.
    10  Namespaces are one honking great idea -- let's do more of those!
```

## Task 1.3
Написать скрипт, работающий так же, как утилита `wc`, вызванная без дополнительных опций.
Т.е. для каждого переданного файла утилита выводит статистику (3 числа) и имя файла.

При этом
- если передано больше одного файла, то в самом конце утилита выводит суммарную статистику (total),
- если ни одного файла не передано, то утилита считывает весь вход и печатает для него статистику без имени.

### Outputs

```
>>> wc --help
NAME
    wc - Print newline, word, and byte counts for each FILE, and a total line if more than one FILE is specified.

SYNOPSIS
    wc [FILENAMES]...

DESCRIPTION
    Print newline, word, and byte counts for each FILE, and a total line if more than one FILE is specified.

POSITIONAL ARGUMENTS
    FILENAMES
        Type: str
```

```
>>> wc inputs/zen_of_python.txt
  19  137  823 inputs/zen_of_python.txt
```

```
>>> wc inputs/lorem.txt inputs/zen_of_python.txt
  39  340 2523 inputs/lorem.txt
  19  137  823 inputs/zen_of_python.txt
  58  477 3346 total
```
