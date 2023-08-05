from pathlib import PurePath, PurePosixPath
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    NoReturn,
    Optional,
    TypeVar,
    Union,
    cast,
)

import yaml
from orjson import OPT_INDENT_2, OPT_OMIT_MICROSECONDS, OPT_SERIALIZE_NUMPY, dumps
from pydantic import BaseModel, SecretStr
from pydantic_openapi_schema.v3_1_0.open_api import OpenAPI
from starlette.responses import Response as StarletteResponse
from starlette.status import HTTP_204_NO_CONTENT, HTTP_304_NOT_MODIFIED

from starlite.enums import MediaType, OpenAPIMediaType
from starlite.exceptions import ImproperlyConfiguredException

T = TypeVar("T")

if TYPE_CHECKING:
    from starlite.datastructures import BackgroundTask, BackgroundTasks
    from starlite.template import TemplateEngineProtocol
    from starlite.types import ResponseCookies


class Response(StarletteResponse, Generic[T]):
    def __init__(
        self,
        content: T,
        *,
        status_code: int,
        media_type: Union["MediaType", "OpenAPIMediaType", str],
        background: Optional[Union["BackgroundTask", "BackgroundTasks"]] = None,
        headers: Optional[Dict[str, Any]] = None,
        cookies: Optional["ResponseCookies"] = None,
    ):
        """The response class is used to return an HTTP response.

        Args:
            content: A value for the response body that will be rendered into bytes string.
            status_code: A value for the response HTTP status code.
            media_type: A value for the response 'Content-Type' header.
            background: A [BackgroundTask][starlite.datastructures.BackgroundTask] instance or
                [BackgroundTasks][starlite.datastructures.BackgroundTasks] to execute after the response is finished.
                Defaults to None.
            headers: A string keyed dictionary of response headers. Header keys are insensitive.
            cookies: A list of [Cookie][starlite.datastructures.Cookie] instances to be set under the response 'Set-Cookie' header.
        """
        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers or {},
            media_type=media_type,
            background=cast("BackgroundTask", background),
        )
        self.cookies = cookies or []

    @staticmethod
    def serializer(value: Any) -> Union[Dict[str, Any], str]:
        """Serializer hook for orjson to handle pydantic models.

        This method can be overridden to extend json serialization.

        Args:
            value: The value to be serialized

        Returns:
            A string keyed dictionary of json compatible values
        """
        if isinstance(value, BaseModel):
            return value.dict()
        if isinstance(value, SecretStr):
            return value.get_secret_value()
        if isinstance(value, (PurePath, PurePosixPath)):
            return str(value)
        raise TypeError  # pragma: no cover

    def render(self, content: Any) -> bytes:
        """
        Handles the rendering of content T into a bytes string.
        Args:
            content: An arbitrary value of type T

        Returns:
            An encoded bytes string
        """
        try:
            if (
                content is None
                or content is NoReturn
                and (self.status_code < 100 or self.status_code in {HTTP_204_NO_CONTENT, HTTP_304_NOT_MODIFIED})
            ):
                return b""
            if self.media_type == MediaType.JSON:
                return dumps(content, default=self.serializer, option=OPT_SERIALIZE_NUMPY | OPT_OMIT_MICROSECONDS)
            if isinstance(content, OpenAPI):
                content_dict = content.dict(by_alias=True, exclude_none=True)
                if self.media_type == OpenAPIMediaType.OPENAPI_YAML:
                    encoded = yaml.dump(content_dict, default_flow_style=False).encode("utf-8")
                    return cast("bytes", encoded)
                return dumps(content_dict, option=OPT_INDENT_2 | OPT_OMIT_MICROSECONDS)
            return super().render(content)
        except (AttributeError, ValueError, TypeError) as e:
            raise ImproperlyConfiguredException("Unable to serialize response content") from e


class TemplateResponse(Response):
    def __init__(
        self,
        template_name: str,
        template_engine: "TemplateEngineProtocol",
        status_code: int,
        context: Optional[Dict[str, Any]] = None,
        background: Optional[Union["BackgroundTask", "BackgroundTasks"]] = None,
        headers: Optional[Dict[str, Any]] = None,
        cookies: Optional["ResponseCookies"] = None,
    ):
        """Handles the rendering of a given template into a bytes string.

        Args:
            template_name: Path-like name for the template to be rendered, e.g. "index.html".
            template_engine: The template engine class to use to render the response.
            status_code: A value for the response HTTP status code.
            context: A dictionary of key/value pairs to be passed to the temple engine's render method. Defaults to None.
            background: A [BackgroundTask][starlite.datastructures.BackgroundTask] instance or
                [BackgroundTasks][starlite.datastructures.BackgroundTasks] to execute after the response is finished.
                Defaults to None.
            headers: A string keyed dictionary of response headers. Header keys are insensitive.
            cookies: A list of [Cookie][starlite.datastructures.Cookie] instances to be set under the response 'Set-Cookie' header.
        """
        context = context or {}
        template = template_engine.get_template(template_name)
        content = template.render(**context or {})
        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type=MediaType.HTML,
            background=background,
            cookies=cookies,
        )
