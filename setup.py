from setuptools import setup

setup(name = "N-body Simulator",
      version = "1.0",
      description = "N-body simulations of the dynamical evolution of stellar clusters and galaxies.",
      author = "Troy P. Kling",
      author_email = "troykling1308@gmail.com",
      url = "https://gitlab.com/CoronalRain/Nbody",
	  py_modules = ["nbody"],
	  install_requires=[
		"numpy",
		"matplotlib",
		"docopt"
	  ],
     )