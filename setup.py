from setuptools import setup, find_packages

setup(
    name='random_img_api',
    version='1.1',
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
        img_api=img_api:cli
    ''',
)