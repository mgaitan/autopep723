import httpx
from pyfiglet import Figlet
from rich.console import Console
from rich.rule import Rule


def get_geek_joke():
    try:
        response = httpx.get("https://geek-jokes.sameerkumar.website/api?format=json", timeout=5.0)
        response.raise_for_status()
        return response.json().get("joke", "No joke today! 🤷‍♂️")
    except Exception as e:
        return f"[Error fetching joke] {e}"


def main():
    console = Console()
    figlet = Figlet(font="slant")
    ascii_text = figlet.renderText("Shiphero Tools")

    # Create rules for top and bottom
    console.print(Rule(title="[cyan]🛠️ SHIPHERO TOOLS", style="bright_magenta"))

    # Print the ASCII banner centered
    console.print(ascii_text, justify="center")

    # Bottom line separator
    console.print(Rule(style="bright_magenta"))

    # Print the joke separately
    joke = get_geek_joke()
    console.print(f"🤓 {joke}", style="dim white", justify="center")


if __name__ == "__main__":
    main()
