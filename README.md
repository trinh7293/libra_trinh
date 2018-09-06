# libra

## Environment

- Using with conda

    + in default environment of conda, setup pipenv
    ```
    pip install --user pipenv
    ```
    + after that, cd to project directory
    + install environment of project by command
    ```
    pipenv install
    ```
    + [Pipenv Document](https://docs.pipenv.org/)

## Notes

```
admin/Whw6eyRy
```

- Celery

to run worker follow command below

```
celery -A libra worker -l info
```

