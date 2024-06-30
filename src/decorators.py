from typing import Any, Callable


def log(filename: str = "decorators") -> Callable:
    """Декоратор, который логирует вызов функции и ее результат в файл."""

    def my_function(func: Callable[[Any], Any]) -> Callable[[Any], Callable]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with open(filename, "a", encoding="utf-8") as file:
                try:
                    res = func(*args, **kwargs)
                    data = res.to_dict(orient="list")
                    file.write(f"{str(data)}\n")
                except Exception as error:
                    file.write(f"{func.__name__} error: {error}\n")
                else:
                    file.write(f"{func.__name__} ok\n")
                    return res

        return wrapper

    return my_function
