from distutils.core import setup

setup(
    name="handzone",
    packages=["handzone"],
    version="0.0.6",
    license="MIT",
    description="Hand Utils",
    author="cavalleria",
    author_email="cavallyb@gmail.com",
    url="https://github.com/cavalleria/handzone.git",
    install_requires=["opencv-python", "numpy", "scipy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
