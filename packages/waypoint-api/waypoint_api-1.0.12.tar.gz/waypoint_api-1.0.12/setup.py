import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

packages = [
    'waypoint_api', 
    'waypoint_api.endpoints',
]

# data_files = [
#     ('waypoint_api/endpoints', [
#         # 'waypoint_api/endpoints/h5.json', 
#         # 'waypoint_api/endpoints/hi.json'
#         ]
#     )
# ]


setuptools.setup(
    name="waypoint_api", # Replace with your own username
    version="1.0.12",
    author="Fliqqr",
    author_email="author@example.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fliqqr/waypoint",
    packages=packages,
    # data_files=data_files,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'aiohttp'
    ],
    python_requires='>=3.10',
)