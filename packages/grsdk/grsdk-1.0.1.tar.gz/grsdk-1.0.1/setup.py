from setuptools import find_packages, setup

# with open("requirements.txt", "r", encoding="utf-8") as f:
#     install_requires = [x.strip() for x in f]

setup(
    name="grsdk",
    version="1.0.1",  
    packages=find_packages(where="grsdk"),
    # packages=find_packages(include=['grsdk']),
    python_requires=">=3.8, <4",
    install_requires=["boto3","pandas","gql[aiohttp]"],
    extras_require={
        "dev": ["wheel","setuptools","pipdeptree"]
    }
)