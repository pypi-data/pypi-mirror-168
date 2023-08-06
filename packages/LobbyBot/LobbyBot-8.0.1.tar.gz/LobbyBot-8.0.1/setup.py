import setuptools

name = 'LobbyBot'


setuptools.setup(
    name=name,
    version="8.0.1",
    author="Pirxcy",
    description="24/7 Fortnite Lobbybot With Admin Controls",
    long_description="24/7 Fortnite Lobbybot With Admin Controls",
    long_description_content_type="text/markdown",
    url="https://github.com/PirxcyFinal/pirxcybotv4",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'sanic==21.6.2',
        'fortnitepy',
        'aiohttp',
        'crayons',
        'psutil',
        'PirxcyPinger'
    ],
)
