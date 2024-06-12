# Test Playwright Framework

<details>
<summary>Версия Python</summary>
 - python 3.11+
</details>

<details> <summary>Установка окружения</summary>

* <details> <summary> Установка с помощью pip</summary>

  * Перейти в папку с проектом
    ```bash
    cd ../project_dir
    ```
  * Перейти создать локальное окружение:
    ```bash
    python -m venv venv
    ```
  * Запустить локальное окружение:
    ```bash
    venv\Scripts\activate.bat
    ```
  * Установить зависимости:
      ```bash
      pip install -r req.txt
      ```

* <details> <summary> Установка с помощью poetry.</summary>
  
  * [Как установить poetry](https://python-poetry.org/docs/#installation)
  * Перейти в папку с проектом
    ```bash
    cd ../project_dir
    ```
  * Установить зависимости:
    ```bash
    poetry install -vv --no-root --no-cache --no-interaction
    ```
</details>
</details>
</details>

<details>
<summary>Команды запуска тестов</summary>

##### Запустить все тесты:
```bash
pytest -v
```
```bash
poetry run pytest -v
```

##### Запустить все тесты без багов:
```bash
pytest -v -m "not bug"
```
```bash
poetry run pytest -v -m "not bug"
```

##### Запустить api тесты:
```bash
pytest -v -m "api"
```
```bash
poetry run pytest -v -m "api"
```

##### Запустить api тесты без багов:
```bash
pytest -v -m "api and not bug"
```
```bash
poetry run pytest -v -m "api and not bug"
```

##### Запустить web тесты:
```bash
pytest -v -m "web"
```
```bash
poetry run pytest -v -m "web"
```

##### Запустить web тесты без багов:
```bash
pytest -v -m "web and not bug"
```
```bash
poetry run pytest -v -m "web and not bug"
```
</details>