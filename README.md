# Визуализатор графа зависимостей Maven Этап 2 (Вариант 21)

На данном этапе реализован минимальный прототип для получения информации о прямых зависимостях Maven-пакетов. Приложение позволяет анализировать указанный пользователем пакет и выводить список его прямых зависимостей.

## Использование

Пример команды для анализа пакета через Maven-репозиторий:

```bash
python3 main.py \
  --package org.springframework:spring-context \
  --repo https://repo.maven.apache.org/maven2/ \
  --repo-mode url \
  --version 6.1.3 \
  --output graph.png
```
 ## Аргументы
| Аргумент      | Описание                                                                       |
| ------------- | ------------------------------------------------------------------------------ |
| `--package`   | Имя анализируемого пакета (`groupId:artifactId`) |
| `--repo`      | URL Maven-репозитория                   |
| `--repo-mode` | Режим работы: реализован только `url`                                                |
| `--version`   | Версия пакета                                          |
| `--output`    | Имя файла для сохранения результата                                            |

## Пример вывода

```bash
Загрузка POM-файла...
Парсинг зависимостей...

Прямые зависимости выбранного пакета:
org.springframework:spring-aop:6.1.3 (scope=compile)
org.springframework:spring-beans:6.1.3 (scope=compile)
org.springframework:spring-core:6.1.3 (scope=compile)
org.springframework:spring-expression:6.1.3 (scope=compile)
io.micrometer:micrometer-observation:1.12.2 (scope=compile)
```