# Experiment Factory Robots

This container will allow you to run a robot test for various kinds of experiments. Currently supported are surveys and jspsych experiments. The container is available on Docker Hub, or you can build it here using the Dockerfile:

```
docker build -t vanessa/expfactory-robots .
```

## Setup

For the examples, we can clone the [test-task](https://www.github.com/expfactory-experiments/test-task) experiment and the [bis11-survey](https://www.github.com/expfactory-experiments/bis11-survey).

```
cd /tmp
git clone https://www.github.com/expfactory-experiments/test-task
git clone https://www.github.com/expfactory-experiments/bis11-survey
```

To test locally, you will need expfactory installed locally.

```
pip install expfactory

# Development
git clone https://www.github.com/expfactory/expfactory
cd expfactory
python setup.py install
```

and for Docker, you will need Docker.


## JsPsych Robot

Note that usage requires python 3, so if you cannot provide it, use the container.

The basic usage is to specify a list of one or more experiment folder paths, and then
optionally select a robot type (the default is jspsych):


```
python start.py --help
usage: start.py [-h] [--robot {survey,jspsych}] folders [folders ...]

expfactory: generate survey from config.json and question file

positional arguments:
  folders               experiments for robot testing

optional arguments:
  -h, --help            show this help message and exit
  --robot {survey,jspsych}, -r {survey,jspsych}
                        the survey robot to recruit!
  --browser {Firefox,Chrome}, -b {Firefox,Chrome}
                        browser driver to use for the robot
```

To run the robot for the test-task and use jspsych, we can simply do:

```
python start.py /tmp/test-task
```

This would be equivalent to:


```
python start.py --robot jspsych /tmp/test-task
```

the browser (chrome default) will open and you will see the experiment progress and
finish. The console will show GET and POST of resources, etc.

```
Recruiting jspsych robot!
[folder] /tmp/test-task
LOG STARTING TEST OF EXPERIMENT
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /jspsych.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /default_style.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /style.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jquery.min.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/math.min.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/jspsych.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/plugins/jspsych-text.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/poldrack_plugins/jspsych-poldrack-text.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/poldrack_plugins/jspsych-poldrack-instructions.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/poldrack_plugins/jspsych-attention-check.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/poldrack_plugins/jspsych-poldrack-single-stim.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/plugins/jspsych-survey-text.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/plugins/jspsych-call-function.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/poldrack_plugins/poldrack_utils.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /experiment.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:48] "GET /%3Cdiv%20class%20=%20%22shapebox%22%3E%3Cdiv%20id%20=%20%22cross%22%3E%3C/div%3E%3C/div%3E HTTP/1.1" 404 -
127.0.0.1 - - [17/Dec/2017 06:52:48] "GET /favicon.ico HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:58] "POST /save HTTP/1.1" 501 -
LOG FINISHING TEST OF EXPERIMENT
LOG [done] stopping web server...
```

## Survey Robot
The same can be done for a survey! Let's now test bis-11

```
python start.py --robot survey /tmp/bis11-survey
```


## Docker Usage

I am currently finish up the functions and writing tests... TBA!
