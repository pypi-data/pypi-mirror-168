from importlib import import_module

import typer

from .converter import Converter

app = typer.Typer()


@app.command()
def main(model_path, format: str = typer.Option("hcl")):
    module_path, class_name = model_path.split(":", 2)
    module = import_module(module_path)
    model = getattr(module, class_name)
    converter = Converter(format=format)
    print(converter.convert(model))


if __name__ == "__main__":
    app()
