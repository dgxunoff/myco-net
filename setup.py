"""
Setup script for MycoShield package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mycoshield",
    version="1.0.0",
    author="Shaastra Biogen 2026 Team",
    description="Mycelium-Inspired Graph Neural Network for Zero-Day Cyberattack Detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "mycoshield-app=apps.streamlit_app:main",
            "mycoshield-rl=apps.rl_app:main",
            "mycoshield-multimodal=apps.multimodal_app:main",
            "mycoshield-enterprise=apps.enterprise_app:main",
            "mycoshield-blockchain=apps.blockchain_app:main",
        ],
    },
)