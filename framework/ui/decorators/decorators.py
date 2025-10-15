import inspect
import logging
from functools import wraps

logger = logging.getLogger(__name__)


def action(message: str = None):
    def decorator(func):
        signature = inspect.signature(func)

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            bound = signature.bind(self, *args, **kwargs)
            bound.apply_defaults()

            context = dict(bound.arguments)
            context['element'] = self

            template = message or func.__name__.replace('_', ' ').capitalize()
            step_text = template.format(**context)

            logger.debug(f"Action: {step_text}")
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def step(message: str = None):
    def decorator(func):
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            bound_args = sig.bind(self, *args, **kwargs)
            bound_args.apply_defaults()
            arguments = bound_args.arguments
            arguments.pop('self', None)  # Remove 'self' from arguments

            step_text = message or func.__name__.replace('_', ' ').capitalize()

            try:
                step_text = step_text.format(**arguments)
            except KeyError as e:
                logger.warning(f"Missing key in step message: {e}")

            logger.info(step_text)
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
