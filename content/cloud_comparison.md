Title: Investigating alternative cloud backends for PyWren
Date: 2017-10-11
Tags: python
Category: benchmarks, s3
Slug: pywren_backends
Author: Allan Peng
Summary: We try out serverless offerings from other cloud providers to see how they compare with AWS Lambda

Recently at [RISELab](https://rise.cs.berkeley.edu/), we’ve been working on [PyWren](http://pywren.io), a distributed computation framework that leverages serverless cloud functions to run python code at massive scale. Our existing infrastructure uses Amazon Web Services: [S3](https://aws.amazon.com/s3/) for storage and [Lambda](https://aws.amazon.com/lambda/) for compute. With the recent introduction of serverless cloud offerings from competing cloud providers, we asked ourselves if we could generalize PyWren to other cloud infrastructures and allow users to easily configure  PyWren to run on other cloud backends.
<style>
table, th, td {
    border: 1px solid black;
}
th, td{
padding: 10px;
}
</style>

## What is Serverless?

Cloud providers have recently launched “serverless” cloud compute offerings, allowing consumers to offload computation to the cloud without having to worry about setting up any of the underlying servers or application environment, and promising to scale out function executions under the hood. The idea is simple: offer a small but scalable execution environment with minimal overhead, abstracting the complex infrastructure. 

Fundamentally, this “serverless cloud” is a consumer-facing concept. There still are servers, containers, and complex infrastructure. The cloud is still just someone else’s computer. The main distinction of the server-less cloud is one that users and consumers see. Because the internal details are often hidden away, we’ve found that implementations and performance different serverless offerings can often be drastically different, though the end product may look the same.

## How PyWren uses the cloud

<a href="/images/meta.png"><img src="/images/how_it_works.png" alt="How it works"style="max-width:100%"></a>

PyWren is a python library that uses serverless compute to implement a map that executes in parallel in the cloud. While native map executes sequentially on a single thread, PyWren executes each of the mapped function calls in parallel using a separate function invocation.

PyWren takes advantage of the fact that with serverless cloud functions, we can easily spin up a large number of workers without having to worry about or take care of the infrastructure underneath. With AWS Lambda for example, we can easily run embarrassingly parallel jobs - up to 3000 simultaneous workers - without having to provision clusters, decide on machine types, pricing, or pay for devops. But would other serverless offerings allow us to scale out in a similar way?


## The Players

The main players in this space are AWS Lambda, [Google Cloud Functions](https://cloud.google.com/functions/), and [Microsoft Azure Functions](https://azure.microsoft.com/en-us/services/functions/). AWS jumped out first, releasing Lambda in 2014, followed by Google Cloud and Azure in 2016.

We wanted to investigate and understand the implementation details of each cloud under the hood, and see how much these implementations would allow us to scale out to handle PyWren’s workloads.

<table style="width:100%">
  <tr>
    <th></th>
    <th>AWS Lambda</th>
    <th>Google Cloud Functions</th> 
    <th>Azure Functions</th>
  </tr>
  <tr>
    <td>Release</td>
    <td>2014</td>
    <td>2016 (in beta)</td> 
    <td>2016</td>
  </tr>
  <tr>
    <td>Runtimes</td>
    <td>Python, Node.js, Java, C#</td> 
    <td>Node.js</td>
    <td>C#, F#, Node.js, Python</td>
  </tr>
  <tr>
    <td>Regions</td>
    <td>Globally available across Americas, Asia, Europe</td>
    <td> US</td>
    <td>Americas, Asia, Europe</td>
  </tr>
</table>

## Implementation

Lambda and GCF have similar models. Function code is staged in a storage bucket ([Google Cloud Storage](https://cloud.google.com/storage/), S3) and run in an isolated container when the function is invoked. In order to keep these invocations lightweight, AWS and Google restrict access to the execution environment to writes to ephemeral disk space in `/tmp`, and limit the size of the deployed code package. Concurrent executions run in isolation, and cannot coordinate with one another.

In contrast, Azure Functions is built on top of [Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/web-sites-create-web-jobs), Microsoft’s app hosting platform, and thus behaves similar to a typical web-app. Invocations are served by threads running in the same sandbox, not isolated from one another. Writes to the filesystem by one function invocation can be seen by all other threads. Additionally, different functions are not isolated from one another. The code for all functions on a single account is stored on the same file system, and can be accessed and called by other functions.

Azure also lets you write to persistent storage, In contrast to Lambda and GCF, where writes to the filesystem can only be seen by other invocations when containers are reused, writes to the Azure function environment are seen by all other threads and persist across all invocations.

Another notable feature of Azure is that users have direct access to the underlying file system through a [cmd console on the deployment website](https://blogs.msdn.microsoft.com/benjaminperkins/2014/03/24/using-kudu-with-windows-azure-web-sites/). Using this, we were able to make extensive modifications to the Azure Functions environment, upgrading the system Python, and installing packages such as NumPy directly on the machine image. 


<table style="width:100%">
  <tr>
    <th></th>
    <th>AWS Lambda</th>
    <th>Google Cloud Functions</th> 
    <th>Azure Functions</th>
  </tr>
  <tr>
    <td>Max Deployment Size (Compressed)</td>
    <td>50MB </td>
    <td>100MB</td> 
    <td>N/A</td>
  </tr>
  <tr>
    <td>Max run time</td>
    <td>300s </td>
    <td>540s</td> 
    <td>600s</td>
  </tr>
  <tr>
    <td>Memory</td>
    <td>1.5GB</td>
    <td>2GB</td> 
    <td>1.5GB/Function Instance</td>
  </tr>
  <tr>
    <td>Disk Space</td>
    <td>512 MB</td> 
    <td>Counted against Memroy Limit</td>
    <td>5TB</td>
  </tr>
  <tr>
    <td>OS</td>
    <td>Amazon Linux</td>
    <td>Debian</td>
    <td> Windows Server 2012</td>
  </tr>
  <tr>
    <td>Job Isolation</td>
    <td>Isolated containers, sometimes reused</td>
    <td>Isolated containers, sometimes reused</td>
    <td>Concurrent threads run in the same function instance</td>
  </tr>
</table>

## Scaling & Limits
The unit of scalability for Lambda and GCF is a single function execution. Upon each function invocation, a container is launched or assigned to run a single execution. AWS and Google limit the number of concurrent functions you can run, and will throttle any job that exceeds the limit of 1000.

When testing PyWren on Google Cloud, we were limited by GCF’s 100GB/100s limit on inbound socket traffic. Because PyWren downloads an Anaconda runtime(120MB) into each container, the socket limit prevents us from running more than ~80 concurrent tasks. As a result, we weren’t able to achieve the same scale with PyWren’s socket-busy workload on Google Cloud as we did on Lambda, which doesn’t limit socket traffic.

In contrast to the one-container-one-execution approach, the unit of scalability for Azure Functions is coarser. Azure scales at the granularity of  a“function instance”, a sandbox that serves up to 512 threads and 32 processes in the same environment. Under the hood, Azure monitors each function’s traffic, and will only scale out to more function instances when a function is consistently receiving a significant load. This means that Azure isn’t a great fit for handling PyWren’s workload, which has low average traffic, but very sudden high bursts.The underlying infrastructure can’t anticipate a sudden burst of dropping into the job queue, and doesn’t have a chance to scale out to handle all of them. In our tests, we found when we tried invoking ~100 concurrent functions, they would all be scheduled to run on the same machine. Each of these threads would then try to fork a Python subprocess, which would overload the machine and cause most of the invocations to get throttled and error.

## Feature Table
<table style="width:100%">
  <tr>
    <th></th>
    <th>AWS Lambda</th>
    <th>Google Cloud Functions</th> 
    <th>Azure Functions</th>
  </tr>
  <tr>
    <td>Deployment options</td>
    <td>Web portal, Command line, boto SDK</td>
    <td>Comamnd line</td> 
    <td>Web portal, HTTP PUT endpoint</td>
  </tr>
  <tr>
    <td>Invocation Authentication</td>
    <td>Yes</td>
    <td>No</td> 
    <td>Yes</td>
  </tr>
  <tr>
    <td>Asynchronous Invocation</td>
    <td>Yes</td>
    <td>None.  Synchronous HTTP POST</td> 
    <td>Yes</td>
  </tr>
</table>

## How PyWren handles multiple backends
Though we're worked to reconcile the implementation differences across serverless providers with the workloads of PyWren, the use of alternate backends is still not ready for deployment.

As we’ve worked to benchmark and understand sever-less cloud infrastructure, we have refactored the PyWren code base to anticipate the use of different cloud storage and compute backends without any noticeable changes for users.

We noted that the user facing APIs, `executor` and `futures` should stay the same no matter what cloud infrastructure we were running on. The only moving parts, essentially, were storage and function invocation - both of which could be swapped out silently in the backend. To use a different compute backend, a user would only need to modify their `pywren_config` and nothing else.

We've also restructured the code under the hood to be less AWS-specific. We abstracted all storage operations to a [generic storage handler](https://github.com/pywren/pywren/pull/119) that calls service-specific APIs under the hood. In addition, we [refactored](https://github.com/pywren/pywren/pull/155/files) much of the lambda code to be portable to different cloud environments - using python’s platform agnostic `os` module to replace hard-coded unix file paths, and using Linux-specific syscalls only when available.

The serverless landscape is new and exciting. Providers are continuously pushing new features, raising limits, adding new options for users, and we're still working to understand the capabilities and trends in this space. We welcome any comments or corrections, in case of any inaccuracies in this post. Feel free to reach out via our [github](https://github.com/pywren/pywren/issues).
