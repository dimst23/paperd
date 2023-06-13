from jinja2 import Template
import pathlib
from typing import Any
from .exceptions.general import TemplateGenerationError
import uuid

class PresentationGenerator:
    def __init__(self, templates_path: str) -> None:
        self.__templates_path = templates_path
        super().__init__()

    def generate_slides(self, slides: list[dict[str, Any]]) -> dict[str, str]:
        j2_template = self.__get_j2_template("slide.tex.j2")

        rendered_template: dict[str, str] = {}
        for slide in slides:
            uuid_name = uuid.uuid5(uuid.NAMESPACE_OID, slide["title"])
            rendered_template[uuid_name] = j2_template.render(
                **slide, 
                uuid_name=uuid_name
            )

        return rendered_template
    
    def generate_main(self, slide_names: list[str], category_props: list[dict[str, str]]) -> str:
        j2_template = self.__get_j2_template("presentation.tex.j2")
        rendered_template = j2_template.render(slides=slide_names, labels=category_props)

        return rendered_template
    
    def __get_j2_template(self, template_name: str) -> Template:
        template_file_path = pathlib.Path(self.__templates_path)
        try:
            with open(
                template_file_path.joinpath(template_name), "r", encoding="utf-8"
            ) as render_file:
                template_contents = render_file.read()
        except (FileNotFoundError, PermissionError) as exc:
            raise TemplateGenerationError(
                f"The '{template_name}' template file could not be found."
            ) from exc
        j2_template = Template(template_contents)

        return j2_template
