from setuptools import find_packages, setup

setup(
    name="samppl",
    version="0.0.0",
    author="Daniel Dodd",
    author_email="d.dodd1@lancaster.ac.uk",
    packages=find_packages(".", exclude=["tests"]),
    license="LICENSE",
    description="A simple probabilistic programming langauage in JAX.",
    keywords=["ppl jax bayesian machine-learning statistics probabilistic-programming"],
)
