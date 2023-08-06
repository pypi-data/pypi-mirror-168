from setuptools import setup, find_packages

setup(name="socket_project_client",
      version="0.0.1",
      description="Client app",
      author="Danila",
      author_email="kalganovdanila@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
