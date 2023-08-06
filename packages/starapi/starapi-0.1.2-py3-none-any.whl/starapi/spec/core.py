import typing as t

from pydantic import BaseModel

from . import construct


class Spec:
    def __init__(self) -> None:
        self.methods: t.List[construct.Method] = []
        self.definition = construct.Definition(paths={}, components=None)

    def add_openapi(self, version: str) -> None:
        self.definition.openapi = version

    def add_info(self, title: str, version: str) -> None:
        self.definition.info = construct.Info(title=title, version=version)

    def update_tag(self, name: str, description: str) -> None:
        if self.definition.tags is None:
            return None

        for tag in self.definition.tags:
            if name == tag.name:
                tag.description = description

    def add_endpoint(
        self,
        classname: str,
        methodname: str,
        tags: t.Optional[t.List[str]] = None,
        summary: t.Optional[str] = None,
        description: t.Optional[str] = None,
        parameters: t.List[construct.Parameter] = None,
        body: construct.RequestBody = None,
        response: t.Dict[str, construct.Response] = None,
    ) -> None:
        method = self._get_method(classname, methodname)
        self._add_tags(tags)
        if isinstance(method, construct.Method):
            endpoint = self._update_endpoint(method.endpoint, tags, summary, description, parameters, body, response)
            self._update_method(classname, methodname, endpoint)
            return None

        self._add_method(classname, methodname, tags, summary, description, parameters, body, response)

    def to_parameters(self, serializer: BaseModel, in_: str) -> t.List[construct.Parameter]:
        parameters: t.List[construct.Parameter] = []
        serializer = serializer.schema()
        required = serializer.get("required") or []
        for key, value in serializer["properties"].items():
            parameter = construct.Parameter(
                name=key, in_=in_, required=True if key in required else False, schema_=value
            )
            parameters.append(parameter)

        return parameters

    def to_body(self, serializer: BaseModel, description: str, content_type: str) -> construct.RequestBody:
        content = construct.Content(schema_={"$ref": f"#/components/schemas/{serializer.__name__}"})
        self._update_schema(serializer)
        return construct.RequestBody(description=description, content={content_type: content})

    def to_response(
        self, serializer: BaseModel, description: str, accept: str = "application/json"
    ) -> construct.Response:
        content = construct.Content(schema_={"$ref": f"#/components/schemas/{serializer.__name__}"})
        self._update_schema(serializer)
        return construct.Response(description=description, content={accept: content})

    def update_definition(self, classname: str, pathname: str, routing_methods: set = None) -> None:
        for method in self.methods:
            if routing_methods:
                if method.name.upper() in routing_methods and classname == method.classname:
                    self._update_paths(method, pathname)

                continue
            else:
                if classname == method.classname:
                    self._update_paths(method, pathname)

    def _get_method(self, classname: str, methodname: str) -> t.Union[construct.Method, None]:
        for method in self.methods:
            if classname == method.classname and methodname == method.name:
                return method

        return None

    def _add_method(
        self,
        classname: str,
        methodname: str,
        tags: t.Optional[t.List[str]],
        summary: t.Optional[str],
        description: t.Optional[str],
        parameters: t.List[construct.Parameter] = None,
        body: construct.RequestBody = None,
        response: t.Dict[str, construct.Response] = None,
    ) -> None:
        endpoint = construct.Endpoint(summary=summary, description=description)
        if tags:
            self._add_tags(tags)
            endpoint.tags = tags

        if parameters:
            endpoint.parameters = parameters

        if body:
            endpoint.requestBody = body

        if response:
            endpoint.responses = response

        method = construct.Method(name=methodname, classname=classname, endpoint=endpoint)
        self.methods.append(method)

    def _update_method(self, classname: str, methodname: str, endpoint: construct.Endpoint) -> None:
        for i, method in enumerate(self.methods):
            if classname == method.classname and methodname == method.name:
                method.endpoint = endpoint
                self.methods[i] = method

    def _update_schema(self, serializer: BaseModel) -> None:
        if serializer.schema().get("definitions"):
            self._update_nested_schema(serializer)
            return None

        self._update_schemas({serializer.__name__: serializer.schema()})

    def _update_nested_schema(self, serializer: BaseModel) -> None:
        schema = serializer.schema(ref_template="#/components/schemas/{model}")
        definitions = schema.pop("definitions")
        self._update_schemas({serializer.__name__: schema})
        for key, value in definitions.items():
            self._update_schemas({key: value})

    def _update_schemas(self, schema: dict) -> None:
        if self.definition.components is None:
            self.definition.components = construct.Schemas(schemas=schema)
            return None

        self.definition.components.schemas.update(schema)

    def _update_endpoint(
        self,
        endpoint: construct.Endpoint,
        tags: t.Optional[t.List[str]],
        summary: t.Optional[str],
        description: t.Optional[str],
        parameters: t.List[construct.Parameter] = None,
        body: t.Dict[str, construct.RequestBody] = None,
        response: t.Dict[str, construct.Response] = None,
    ) -> construct.Endpoint:
        if tags:
            endpoint.tags = tags

        if summary:
            endpoint.summary = summary

        if description:
            endpoint.description = description

        if parameters:
            if endpoint.parameters is None:
                endpoint.parameters = []

            endpoint.parameters += parameters

        if body:
            endpoint.requestBody = body

        if response:
            if endpoint.responses is None:
                endpoint.responses = {}

            endpoint.responses.update(response)

        return endpoint

    def _update_paths(self, method: construct.Method, pathname: str) -> None:
        path = construct.Path(name=pathname, method={method.name: method.endpoint})
        current_path_method = self.definition.paths.get(path.name)
        if current_path_method:
            current_path_method.update(path.method)
            self.definition.paths.update({path.name: current_path_method})
            return None

        self.definition.paths.update({path.name: path.method})

    def _add_tags(self, tags: t.List[str]) -> None:
        if tags is None:
            return None

        if self.definition.tags is None:
            self.definition.tags = [construct.Tag(name=tag) for tag in tags]
            return None

        current_tags: t.List[str] = [current_tag.name for current_tag in self.definition.tags]
        for tag in tags:
            if tag not in current_tags:
                self.definition.tags.append(construct.Tag(name=tag))
