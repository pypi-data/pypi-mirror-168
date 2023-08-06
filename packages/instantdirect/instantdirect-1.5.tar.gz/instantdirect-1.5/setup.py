import setuptools

setuptools.setup(
    name='instantdirect',
    version='1.5',
    packages=setuptools.find_packages(),
    license='GPL-3.0',
    author='jack',
    author_email='kinginjack@gmail.com',
    description='an automation software ',
    install_requires=['selenium', 'colorama', 'datetime', 'cryptography', 'webdriver-manager', 'termcolor', 'tinydb','pyperclip'],
    python_requires='>=3.8'
)
