import ast
import functools
import json
import typing as t

from pydantic import BaseModel
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import JSONResponse

from .spec.core import Spec


class Api:
    spec = Spec()

    @classmethod
    def query(cls, serializer: BaseModel, tags: t.List[str] = None):
        def decorator(func):
            summary, description = cls._get_document(func.__doc__)
            classname, methodname = cls._get_name(func.__qualname__)
            parameters = cls.spec.to_parameters(serializer, "query")
            cls.spec.add_endpoint(classname, methodname, tags, summary, description, parameters=parameters)

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                request: Request = cls._get_request(args)
                args = args + (serializer(**request.query_params),)
                return await func(*args, **kwargs)

            return wrapper

        return decorator

    @classmethod
    def path(cls, serializer: BaseModel, tags: t.List[str] = None):
        def decorator(func):
            summary, description = cls._get_document(func.__doc__)
            classname, methodname = cls._get_name(func.__qualname__)
            parameters = cls.spec.to_parameters(serializer, "path")
            cls.spec.add_endpoint(classname, methodname, tags, summary, description, parameters=parameters)

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                request: Request = cls._get_request(args)
                args = args + (serializer(**request.path_params),)
                return await func(*args, **kwargs)

            return wrapper

        return decorator

    @classmethod
    def header(cls, serializer: BaseModel, tags: t.List[str] = None):
        def decorator(func):
            summary, description = cls._get_document(func.__doc__)
            classname, methodname = cls._get_name(func.__qualname__)
            parameters = cls.spec.to_parameters(serializer, "header")
            cls.spec.add_endpoint(classname, methodname, tags, summary, description, parameters=parameters)

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                request: Request = cls._get_request(args)
                args = args + (serializer(**request.headers),)
                return await func(*args, **kwargs)

            return wrapper

        return decorator

    @classmethod
    def body(
        cls,
        serializer: BaseModel,
        description: str = "",
        content_type: str = "application/json",
        tags: t.List[str] = None,
    ):
        def decorator(func):
            summary, description_ = cls._get_document(func.__doc__)
            classname, methodname = cls._get_name(func.__qualname__)
            body = cls.spec.to_body(serializer, description, content_type)
            cls.spec.add_endpoint(classname, methodname, tags, summary, description_, body=body)

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                request: Request = cls._get_request(args)
                if content_type == "application/json":
                    data = await request.json()
                elif content_type == "multipart/form-data":
                    form = await request.form()
                    data = form._dict
                else:
                    body = await request.body()
                    data = ast.literal_eval(body.decode("utf-8"))

                args = args + (serializer(**data),)
                return await func(*args, **kwargs)

            return wrapper

        return decorator

    @classmethod
    def response(
        cls,
        serializer: BaseModel,
        status_code: int = 200,
        description: str = "",
        headers: t.Optional[t.Dict[str, str]] = None,
        media_type: t.Optional[str] = None,
        background: t.Optional[BackgroundTask] = None,
    ):
        def decorator(func):
            summary, description_ = cls._get_document(func.__doc__)
            classname, methodname = cls._get_name(func.__qualname__)
            response = cls.spec.to_response(serializer, description)
            cls.spec.add_endpoint(
                classname, methodname, None, summary, description_, response={str(status_code): response}
            )

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                response = await func(*args, **kwargs)
                if isinstance(response, BaseModel):
                    return JSONResponse(json.loads(response.json()), status_code, headers, media_type, background)

                return response

            return wrapper

        return decorator

    @classmethod
    def _get_name(cls, qualname: str) -> t.Tuple[str, str]:
        assert "." in qualname, "Can't apply to function based view."
        return tuple(qualname.split("."))

    @classmethod
    def _get_document(cls, document: str) -> t.Tuple[str, str]:
        if document is None:
            return None, None

        if "\n" in document:
            docs = document.split("\n")
            docs = [doc.strip() for doc in docs]
            return docs[0], "".join(f"{b}\n" for b in docs[1:-1])

        return document, None

    @classmethod
    def _get_request(cls, args: tuple) -> t.Union[Request, None]:
        for arg in args:
            if isinstance(arg, Request):
                return arg

        raise ValueError("Request object not found.")
