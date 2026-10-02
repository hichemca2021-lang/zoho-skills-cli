"""zoho-skills-cli: install Zoho CRM pre-sales skills into a project.

Usage (no local install needed, via uv):

    uvx --from git+https://github.com/<org>/zoho-skills-cli.git zoho-skills init my-project
    uvx --from git+https://github.com/<org>/zoho-skills-cli.git zoho-skills init --here
"""

from __future__ import annotations

import shutil
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

SKILLS_SRC = Path(__file__).parent / "skills"

# Each skill's SKILL.md `name:` frontmatter is the slash-command the agent
# recognizes once installed (e.g. invoked as /crm-data-model-customizer).
# Order reflects the suggested engagement flow: discover -> design -> plan -> demo.
SKILLS = [
    {
        "dir": "crm-discovery-interviewer",
        "command": "/crm-discovery-interviewer",
        "label": "Discovery Interview",
        "blurb": "Interview a CRM-naive prospect and produce a structured customer brief",
    },
    {
        "dir": "design-prospect",
        "command": "/design-prospect",
        "label": "Design Prospect (guided intake)",
        "blurb": "Guided front door into CRM Design for an engineer who hasn't gathered discovery material yet",
    },
    {
        "dir": "crm-data-model-customizer",
        "command": "/crm-data-model-customizer",
        "label": "CRM Data Model Customizer",
        "blurb": "Design a traceable, validated Zoho CRM data model package for a prospect",
    },
    {
        "dir": "customization-implementation-planner",
        "command": "/customization-implementation-planner",
        "label": "Implementation Plan Generator",
        "blurb": "Turn a validated design package into a credential-free, API-executable build plan",
    },
    {
        "dir": "demo-package",
        "command": "/demo-package",
        "label": "Demo Pulse",
        "blurb": "Turn an org + customer pain case into a truthful, screen-by-screen demo script",
    },
]

BANNER = r"""
 _____     _            ____  _    _ _ _
|__   |___| |__   ___  / ___|| | _(_) | |___
  /  /| / _ \ '_ \ / _ \\___ \| |/ / | | / __|
 / /__|   (_) | | | (_) |__) |   <| | | \__ \
/_____|__ \___/|_| |_|\___/____/|_|\_\_|_|___/
"""


def _print_banner() -> None:
    text = Text(BANNER, style="bold cyan")
    console.print(text)
    console.print(
        Text("Zoho CRM Pre-Sales Skills Toolkit", style="bold yellow", justify="center")
    )
    console.print()


def _copy_skills(target_skills_dir: Path, overwrite: bool) -> list[str]:
    installed = []
    target_skills_dir.mkdir(parents=True, exist_ok=True)
    for skill in SKILLS:
        src = SKILLS_SRC / skill["dir"]
        dest = target_skills_dir / skill["dir"]
        if dest.exists():
            if not overwrite:
                console.print(
                    f"  [yellow]skip[/yellow] {skill['dir']} already exists (use --force to overwrite)"
                )
                continue
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        installed.append(skill["dir"])
    return installed


def _print_setup_panel(project_name: str, working_path: Path, target_path: Path) -> None:
    body = Text()
    body.append("Project       ", style="bold")
    body.append(f"{project_name}\n")
    body.append("Working Path  ", style="bold")
    body.append(f"{working_path}\n")
    body.append("Target Path   ", style="bold")
    body.append(f"{target_path}")
    console.print(Panel(body, title="Zoho Skills Project Setup", border_style="cyan"))


def _print_next_steps(project_name: str, is_here: bool) -> None:
    lines = []
    if not is_here:
        lines.append(f"1. Go to the project folder: [bold]cd {project_name}[/bold]")
        step = 2
    else:
        step = 1
    lines.append(
        f"{step}. Start Claude (or your coding agent) in this project directory; "
        "skills were installed to [bold].claude/skills[/bold]"
    )
    step += 1
    lines.append(f"{step}. Start using the skills:")
    for skill in SKILLS:
        lines.append(f"   [cyan]{skill['command']}[/cyan] — {skill['blurb']}")

    console.print(Panel("\n".join(lines), title="Next Steps", border_style="green"))

    workflow = Text()
    workflow.append("Typical flow: ", style="bold")
    workflow.append(
        "run /crm-discovery-interviewer (or /design-prospect if you already have discovery "
        "material) to produce a customer brief, hand it to /crm-data-model-customizer to "
        "produce a validated design package, hand that to "
        "/customization-implementation-planner for a credential-free API build plan, then "
        "hand the built org to /demo-package (with a connected Zoho CRM MCP server) to "
        "generate the demo plan and spoken transcript."
    )
    console.print(Panel(workflow, title="Suggested Workflow", border_style="blue"))


app = typer.Typer(
    name="zoho-skills",
    help="Install Zoho CRM pre-sales skills (CRM Data Model Customizer, Demo Pulse) into a project.",
    add_completion=False,
)


@app.command()
def init(
    project_name: str = typer.Argument(
        None, help="Name of the new project directory to create."
    ),
    here: bool = typer.Option(
        False, "--here", help="Install skills into the current directory instead of a new one."
    ),
    force: bool = typer.Option(
        False, "--force", help="Overwrite skills that are already installed."
    ),
) -> None:
    """Create (or use) a project directory and install the skills into .claude/skills."""
    _print_banner()

    if not here and not project_name:
        console.print("[red]Error:[/red] provide a project name, or pass --here to use the current directory.")
        raise typer.Exit(code=1)

    if here:
        target_root = Path.cwd()
        project_name = target_root.name
    else:
        target_root = Path.cwd() / project_name
        if target_root.exists() and any(target_root.iterdir()):
            console.print(f"[red]Error:[/red] directory '{project_name}' already exists and is not empty.")
            raise typer.Exit(code=1)
        target_root.mkdir(parents=True, exist_ok=True)

    skills_dir = target_root / ".claude" / "skills"
    _print_setup_panel(project_name, Path.cwd(), target_root)

    console.print()
    installed = _copy_skills(skills_dir, overwrite=force)
    for name in installed:
        console.print(f"  [green]✓[/green] installed {name}")
    console.print()

    _print_next_steps(project_name, is_here=here)


@app.command()
def check() -> None:
    """List the skills this toolkit installs."""
    _print_banner()
    for skill in SKILLS:
        console.print(f"  [cyan]{skill['command']}[/cyan] — {skill['label']}: {skill['blurb']}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
