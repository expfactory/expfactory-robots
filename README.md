# Experiment Factory Robots

This container will allow you to run a robot test for various kinds of experiments. Currently supported are surveys and jspsych experiments. The container is available on Docker Hub, or you can build it here using the Dockerfile:

```
docker build -t vanessa/expfactory-robots .
```

## Setup

For both examples, ew can clone the [test-task](https://www.github.com/expfactory-experiments/test-task) experiment.

```
cd /tmp && git clone https://www.github.com/expfactory-experiments/test-task
```

and then proceed with a local or Docker container test.

## Local Usage
If you use the functions locally (on your host) you will need to install expfactory.

```
pip install expfactory
```

or from the Github repository:

```
git clone https://www.github.com/expfactory/expfactory
cd expfactory
python setup.py install
```

Note that usage requires python 3, so if you cannot provide it, use the container.

## Docker Usage

I am currently finish up the functions and writing tests... TBA!
