Title: pywren -- run your python code on thousands of cores
skiptitle: True
Slug: home
Authors: Eric Jonas
Summary: Pywren uses AWS Lambda to effortlessly run your existing python code on thousands of machines in the cloud 
save_as: index.html
status: hidden
template: home

## Overview
```python
  def my_function(b):
    x = np.random.normal(0, b, 1024)
    A = np.random.normal(0, b, (1024, 1024))
    return np.dot(A, x)

  pwex = pywren.default_executor()
  res = pwex.map(my_function, np.linspace(0.1, 100, 1000))
```

## Scaling Examples
<div class="row">
    <div class="col-sm-4 col-md-4">
        <div class="thumbnail">
        <img src="images/flops_scaling.flops.small.png" alt="...">
        <div class="caption">
        <h5> 40 TFLOPS on Lambda <a href="https://github.com/pywren/examples/tree/benchmark_flops">[more]</a> </h5>
        </div>
        </div>
    </div>
        <div class="col-sm-4 col-md-4">
        <div class="thumbnail">
        <img src="images/s3_scaling.s3_agg_tput.png" alt="...">
        <div class="caption">
        <h5> 80 GB/sec read and 60 GB/s write to S3 <a href="https://github.com/pywren/examples/tree/master/benchmark_s3">[more]</a> </h5>
        </div>
        </div>
    </div>


  <!-- </div> -->
  
</div>


## Getting started

First, make sure you have an account
with [Amazon Web Services](https://aws.amazon.com/). Then download and
install pywren via PIP
as
[outlined in the getting started materials]({filename}gettingstarted.md) Then
enjoy running your code on thousands of cores simultaneously!

## Technology 

Key technologies leveraged include:

* [AWS Lambda](https://aws.amazon.com/lambda/) for fast, containerized, stateless compute
* [AWS S3](https://aws.amazon.com/s3/) for event coordination
* [Continuum's Anaconda python distribution](https://www.continuum.io/downloads) for up-to-date python packages
* [cloudpickle](https://github.com/cloudpipe/cloudpickle) for shipping functions back and forth

The overall goal is to [mimic the Python 3.x futures interface](http://pythonhosted.org/futures/) as
much as make sense. 

Key Limitations:

* low limit of simultaneous workers (maybe 3k if you reserve ahead)
* finite amount of time per worker (300 seconds), but [see support for stand-alone workers!]
* non-trivial function invocation overhead, sometimes 15 sec! 

## Publications

> *"Occupy the Cloud: Distributed computing for the 99%"* [arXiv 1702.0402](https://arxiv.org/abs/1702.04024) 
> [Eric Jonas](http://ericjonas.com), [Shivaram Venkataraman](http://shivaram.org/), 
> [Ion Stoica](https://people.eecs.berkeley.edu/~istoica/), [Benjamin Recht](https://people.eecs.berkeley.edu/~brecht/)

## Recent news

