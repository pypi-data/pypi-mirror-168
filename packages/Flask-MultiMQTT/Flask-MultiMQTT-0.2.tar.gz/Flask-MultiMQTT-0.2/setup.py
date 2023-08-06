from setuptools import setup

setup(
    name="Flask-MultiMQTT",
    version='0.2',
    url="https://git.sr.ht/~martijnbraam/Flask-MultiMQTT",
    license="MIT",
    author="Martijn Braam",
    author_email="martijn@brixit.nl",
    description="Flask middleware for MQTT with threading support",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=["flask_multimqtt"],
    install_requires=["Flask", "paho-mqtt"],
)
