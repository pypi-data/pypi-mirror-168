from typer import Typer
from rich import print

from .animals import Cow, Cat, Dog


# Creating app instance
app = Typer()


# Command for a cow
@app.command()
def cow(sound: str):
    new_cow = Cow()
    if new_cow.validate_sound(sound):
        print(f"{new_cow.generate_image(sound)}")
    else:
        print(f"[bold red]{new_cow.species_name} does not say '{sound}'!")


# Command for a cat
@app.command()
def cat(sound: str):
    new_cat = Cat()
    if new_cat.validate_sound(sound):
        print(f"{new_cat.generate_image(sound)}")
    else:
        print(f"[bold red]{new_cat.species_name} does not say '{sound}'!")


# Command for a dog
@app.command()
def dog(sound: str):
    new_dog = Dog()
    if new_dog.validate_sound(sound):
        print(f"{new_dog.generate_image(sound)}")
    else:
        print(f"[bold red]{new_dog.species_name} does not say '{sound}'!")

app()