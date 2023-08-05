import sys
import os
import json
import platform
import sys

import deta
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

import click

from validator import validate

console = Console()

current_os = platform.system()
if current_os == "Windows":
    data_dir = os.path.join(os.getenv("LOCALAPPDATA"), "mini","detabase")
elif current_os == "Linux":
    data_dir = os.path.join(os.getenv("HOME"), ".config", "mini", "detabase")
else:
    console.print("We don't support your OS yet!", style="bold red")


@click.group()
@click.version_option("0.0.3")
def main():
    """CLI for detabase"""
    pass


# Make a command --verify which takes no arguments
@main.command()
def verify():
    """Verify the config file"""
    config_path, default_project = validate(data_dir)
    if default_project:
        console.print("Config file is valid!", style="bold green")
    else:
        console.print(f"Config file is invalid! Created config.json in {config_path}", style="bold red")

@main.command()
def showconfig():
    """Show the config file"""
    config_path, default_project = validate(data_dir)
    with open(config_path, "r") as f:
        config = json.load(f)

    conf = Table(title="About config.json",show_header=True, header_style="bold magenta", title_style="bold white")
    conf.add_column("Version", style="dim")
    conf.add_column("Default Project Key", style="dim")
    conf.add_row(config["version"], config["default_project_key"])
    console.print(conf)
    projects = Table(title="Projects", show_header=True, header_style="bold magenta", title_style="bold white")
    projects.add_column("Project Key", style="dim")
    projects.add_column("Project Name", style="dim")
    for project_key, project_name in config["projects"].items():
        projects.add_row(project_key, project_name)
    console.print(projects)

@main.command()
def delete():
    """Delete the config file"""
    config_path, status = validate(data_dir)
    os.remove(config_path)
    console.print("Deleted config file!", style="bold green")

@main.command()
def create():
    """Create a new project"""
    config_path, status = validate(data_dir)
    if status is False:
        console.print("Please set a default project first!", style="bold red")
        project_name = console.input("Enter the project name: ")
        project_key = console.input("Enter the project key: ")
        console.print("Setting it as default project...", style="bold green")
        with open(config_path, "r") as f:
            config = json.load(f)
        config["default_project_key"] = project_key
        config["projects"][project_key] = project_name
        with open(config_path, "w") as f:
            json.dump(config, f)
        console.print("Done!", style="bold green")

if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("basecli")
    main()