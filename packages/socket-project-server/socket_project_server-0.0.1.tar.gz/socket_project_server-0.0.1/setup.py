from setuptools import setup, find_packages

setup(name="socket_project_server",
      version="0.0.1",
      description="Server app",
      author="Danila",
      author_email="kalganovdanila@gmailc.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
