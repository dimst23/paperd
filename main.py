from program.src import PresentationGenerator
import pathlib
from typing import Any
import json
import os
import uuid
import shutil

def read_json_file(path: str):
    try:
        with open(pathlib.Path(path), "r", encoding="utf-8") as settings_file:
            contents_dict: dict[str, Any] = json.load(settings_file)
    except (FileNotFoundError, PermissionError) as exc:
        raise FileExistsError(
            f"The '{path}' file could not be read or found."
        ) from exc
    return contents_dict

def parse_config(config_path: str, config_key: str) -> list[dict[str, str]]:
    json_settings = read_json_file(config_path)
    return json_settings[config_key]

def uuid_name_calculator(name: str):
    return str(uuid.uuid5(uuid.NAMESPACE_OID, name))


if __name__ == '__main__':
    templates_path = "program/templates"
    slides_path = "input/slides.json"
    settings_path = "program/settings/settings.json"

    output_path = "output"
    output_slides_path = "output/slides"
    output_assets_path = "output/assets"

    slides_list = parse_config(slides_path, "content")
    category_settings = parse_config(settings_path, "category_tags")
    directory_settings = parse_config(settings_path, "output_directories")

    pr_generator = PresentationGenerator.PresentationGenerator(templates_path)
    generated_slides = pr_generator.generate_slides(slides_list)
    generated_main = pr_generator.generate_main(list(generated_slides.keys()), category_settings)

    for uuid_name, slide_content in generated_slides.items():
        slides_output = pathlib.Path(output_slides_path)
        if not os.path.exists(slides_output):
            os.makedirs(slides_output)
        with open(
            pathlib.Path(output_slides_path).joinpath(f"slide-{uuid_name}.tex"),
            "w",
            encoding="utf-8",
        ) as render_file:
            render_file.write(slide_content)

    with open(
        pathlib.Path(output_path).joinpath("main.tex"),
        "w",
        encoding="utf-8",
    ) as render_file:
        render_file.write(generated_main)
    
    for output_dir in directory_settings:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    # Copy all assets to output
    for slide in slides_list:
        assets_output = pathlib.Path(output_assets_path).joinpath("figures", uuid_name_calculator(slide["title"]))
        if not os.path.exists(assets_output):
            os.makedirs(assets_output)
        for figure in slide["figures"]:
            shutil.copyfile(pathlib.Path(f"./input/figures/{figure}"), assets_output.joinpath(figure))
    
    # Create the output folder structure to include assets, slides and the tex files. Move all figure there too.