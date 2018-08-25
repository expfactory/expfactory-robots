# Experiment Factory Robots

This set of scripts (and provided container) allow you to run a robot test for various kinds of experiments. Currently supported are:

 - [surveys]()
 - [jspsych experiments]()
 - [labjs]()

Local (non container) use will be discussed first, followed by Docker.

[![asciicast](https://asciinema.org/a/153497.png)](https://asciinema.org/a/153497?speed=3)

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

and for Singularity, you will need to [install Singularity](https://singularityware.github.io/install-linux).


## LabJS Robot

**under development**

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

The output is similar to jspsych, except we are progressing through a survey.

```
python start.py --robot survey /tmp/bis11-survey
Recruiting survey robot!
[folder] /tmp/bis11-survey
LOG STARTING TEST OF SURVEY
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /css/material.blue-red.min.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /css/surveys.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /css/jquery-ui-1.10.4.custom.min.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /css/style.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /js/jquery-2.1.1.min.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /js/material.min.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /js/jquery-ui-1.10.4.custom.min.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /js/jquery.wizard.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /js/jquery.form-3.50.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /js/jquery.validate-1.12.0.min.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /css/images/ui-bg_flat_75_ffffff_40x100.png HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /css/images/ui-bg_highlight-soft_75_cccccc_1x100.png HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /favicon.ico HTTP/1.1" 200 -
LOG Testing page 1
LOG Testing page 2
LOG Testing page 3
LOG Testing page 4
LOG Testing page 5
LOG FINISHING TEST OF SURVEY
LOG [done] stopping web server...
```

## Singularity Usage
Singularity is ideal for this use case because of the seamless nature between the container and host. We have a pre-built image for your use:

```
singularity pull shub://expfactory/expfactory-robots
```

or if you want to build it yourself, the first thing you would want to do is again clone the repository:

```
git clone https://www.github.com/expfactory/expfactory-robots
cd expfactory-robots
```

and then build.

```
sudo singularity build expfactory-robots.simg Singularity
```

Then to run the image, you will basically want to bind the *parent* folder where your task is to `/data` in the container, and specify the path to the experiment *relative to `data`*

```
singularity run --bind /tmp:/data expfactory-robots.simg /data/test-task
```


## Docker Usage
Note that this isn't fully tested and working, because of issues with the display and drivers. I have a feeling it would be a good idea to start with one of the [selenium bases](https://github.com/SeleniumHQ/docker-selenium), but I haven't tried it yet. Please submit a pull request if you are able to get it working. My notes will be included here. To build the image:

```
docker build -t vanessa/expfactory-robots .
```

To run it, I again mapped the folder one level above your experiment (so we can validate the experiment folder name itself!) to `/data` in the container, and I also made sure to specify the port, because Docker doesn't have a seamless connection to the host like Singularity.

```
docker run -v /tmp:/data -p 3030:3030 -v /dev/shm:/dev/shm vanessa/expfactory-robots /data/test-task
```

I didn't get beyond this point - I had various errors with the Gecko Driver an went back to using Singularity!
