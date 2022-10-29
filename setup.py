from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='random_img_api',
    version='1.1.0',
    author='Branden Xia',
    description='Random Image API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/BrandenXia/Random_Img_API",
    packages=['random_img_api', 'random_img_api.src', 'random_img_api.src.get_img'],
    include_package_data=True,
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