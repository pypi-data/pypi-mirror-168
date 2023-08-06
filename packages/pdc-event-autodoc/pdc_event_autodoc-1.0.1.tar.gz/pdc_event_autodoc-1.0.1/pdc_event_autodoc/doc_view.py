from pydantic import AnyHttpUrl

def get_asyncapi_html(
    *,
    asyncapi_url: AnyHttpUrl,
    title: str,
    asyncapi_js_url: str = "https://unpkg.com/@asyncapi/web-component@1.0.0-next.32/lib/asyncapi-web-component.js",
    asyncapi_css_url: str = "https://unpkg.com/@asyncapi/react-component@1.0.0-next.32/styles/default.min.css",
):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <script src="{asyncapi_js_url}" defer></script>
        <asyncapi-component
            schemaUrl="{asyncapi_url}"
            cssImportPath="{asyncapi_css_url}">
        </asyncapi-component>
    </body>
    </html>
    """
    return html