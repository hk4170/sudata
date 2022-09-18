from setuptools import setup
setup(
    name = 'sudata',
    py_modules = [
        'mysql.py',
        'sqlite.py',
        'csvloader.py',
        'excel.py'
    ],
    scripts =['sudata']  
)