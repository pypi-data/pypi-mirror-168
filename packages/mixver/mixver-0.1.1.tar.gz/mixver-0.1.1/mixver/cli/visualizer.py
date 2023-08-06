from rich.console import Console
from rich.table import Table


def show_tags(tags: list[str], names, versions, paths):
    table = Table(title="Artifacts")

    table.add_column("Tag", justify="center", style="green")
    table.add_column("Name", justify="center", style="black")
    table.add_column("Version", justify="center", style="cyan")
    table.add_column("Path", justify="center", style="red")

    for i in range(len(tags)):
        table.add_row(tags[i], names[i], versions[i], paths[i])

    print("AA")
    console = Console()
    console.print(table)
