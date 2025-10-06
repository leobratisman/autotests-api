from typing import ParamSpec, TypeVar, Callable
from functools import wraps

from clients.base_schema import ApiResponse



P = ParamSpec("P")
R = TypeVar("R")
# TODO: add response
def handle_error(func: Callable[P, R], response) -> Callable[P, R]:
    @wraps(func)
    def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self.logger.error(f"Failed to {func.__name__}: {e}")
            return ApiResponse(
                status_code=getattr(response, "status_code", None), 
                error=str(e),
                raw_response=response.text
            )
    return wrapper