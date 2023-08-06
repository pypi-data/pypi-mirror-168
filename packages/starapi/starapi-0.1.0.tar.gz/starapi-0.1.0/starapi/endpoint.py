import typing as t

import jinja2
from starlette.endpoints import HTTPEndpoint
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import BaseRoute, Mount, Route

from .api import Api


class OpenApiEndpoint(HTTPEndpoint):
    async def get(self, request):
        def updates(routes: t.List[BaseRoute], parent: str):
            for route in routes:
                if isinstance(route, Route):
                    Api.spec.update_definition(route.name, f"{parent}{route.path}", route.methods)

                if isinstance(route, Mount):
                    updates(route.routes, f"{parent}{route.path}")

        updates(request.app.routes, "")

        return JSONResponse(Api.spec.definition.dict(by_alias=True, exclude_none=True))


class SwaggerUiEndpoint(HTTPEndpoint):
    async def get(self, request):
        environment = jinja2.Environment()
        template = environment.from_string(
            """<!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <meta name="description" content="SwaggerUI" />
                <title>SwaggerUI</title>
                <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui.css" />
            </head>

            <body>
                <div id="swagger-ui"></div>
                <script src="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui-bundle.js" crossorigin></script>
                <script>
                    window.onload = () => {
                        window.ui = SwaggerUIBundle({
                            url: "{{ url }}",
                            dom_id: "#swagger-ui",
                        });
                    };
                </script>
            </body>

            </html>
        """
        )
        html = template.render(url=request.url_for("OpenApiEndpoint"))
        return HTMLResponse(html)


class RedocEndpoint(HTTPEndpoint):
    async def get(self, request):
        environment = jinja2.Environment()
        template = environment.from_string(
            """<!DOCTYPE html>
            <html>

            <head>
                <title>Redoc</title>
                <!-- needed for adaptive design -->
                <meta charset="utf-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">

                <!--
                Redoc doesn't change outer page styles
                -->
                <style>
                body {
                    margin: 0;
                    padding: 0;
                }
                </style>
            </head>

            <body>
                <redoc spec-url="{{ url }}"></redoc>
                <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"> </script>
            </body>
            
            </html>
        """
        )
        html = template.render(url=request.url_for("OpenApiEndpoint"))
        return HTMLResponse(html)
