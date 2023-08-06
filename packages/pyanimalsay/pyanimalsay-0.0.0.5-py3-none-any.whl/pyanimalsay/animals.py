# Class for representing animal species
class Animal:

    def __init__(self,  species_name: str, sound: str):
        self.species_name = species_name
        self.sound = sound

    def validate_sound(self, sound: str) -> bool:
        chars = list(set(self.sound))
        given_chars = list(set(sound.upper()))
        for c1, c2 in zip(chars, given_chars):
            if c1 != c2:
                return False
        return True


# Class for representing a cow
class Cow(Animal):

    def __init__(self):
        super().__init__('Cow', 'MO')

    @staticmethod
    def generate_image(sound: str) -> str:
        return rf'''[green]
      {'-' * len(sound)}
    < [bold]{sound}[/] >
      {'-' * len(sound)}
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
        [/]'''


# Class for representing a cat
class Cat(Animal):

    def __init__(self):
        super().__init__('Cat', 'MEOW')

    @staticmethod
    def generate_image(sound: str) -> str:
        return rf'''[blue]
      {'-' * len(sound)}
    < [bold]{sound}[/] >
      {'-' * len(sound)}
       \
        \   |\/| ---- _
           =(oo)=_____ \
            c___ (______/
        [/]'''


# Class for representing a dog
class Dog(Animal):

    def __init__(self):
        super().__init__('Dog', 'WOOF')

    @staticmethod
    def generate_image(sound: str) -> str:
        return rf'''[yellow]
      {'-' * len(sound)}
    < [bold]{sound}[/] >
      {'-' * len(sound)}
       \    _   _
        \  /(. .)\    )
             (*)____/|
             /       |
            /   |--\ |
           (_)(_)  (_)
    [/]'''
