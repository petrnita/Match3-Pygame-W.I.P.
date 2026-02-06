from rich.console import Console

console = Console()

def log(message: str, headline: str='')
    if headline != '':
        console.rule(headline)
    console.log(message)
