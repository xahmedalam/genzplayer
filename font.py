import os

files = os.listdir("src/font")
fonts = []

for file in files:
    with open(f"src/font/{file}", "rb") as f:
        fonts.append(bytes.hex(f.read()))

with open("fonts.py", "w") as f:
    _fonts = []
    for font in fonts:
        _fonts.append(f'"{font}"')
    f.write(f"FONTS = [{','.join(_fonts)}]")
