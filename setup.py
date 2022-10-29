from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='random_img_api',
    version='1.0',
    description='Random Image API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/BrandenXia/Random_Img_API",
    py_modules=find_packages(),
    install_requires=[
        'pydenticon',
        'rich_click',
        'requests',
        "Pillow",
        "gunicorn",
        "uvicorn",
        "fastapi",
        "rich"
    ],
    entry_points='''
        [console_scripts]
        img_api=random_img_api.img_api_cli:cli
    ''',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
    ],
)