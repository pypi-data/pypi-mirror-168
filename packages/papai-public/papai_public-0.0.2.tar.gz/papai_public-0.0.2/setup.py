from setuptools import setup

setup(name='papai_public',
      version='0.0.2',
      description="Public papAI minio writer/reader",
      author="Datategy",
      py_modules=['papai_minio'],
      package_dir={'': 'src'},
      install_requires=["pyarrow==9.0.0", "minio==7.1.9"]
)