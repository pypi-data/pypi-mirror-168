from typer import Typer


app = Typer()


@app.command()
def hi(name: str):
    print(f"Hi, {name}")


@app.command()
def bye(name: str):
    print(f"bye, {name}")
