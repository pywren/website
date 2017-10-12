Title: Investigating alternative cloud backends for PyWren
Date: 2017-10-11
Tags: python
Category: benchmarks, s3
Slug: pywren_backends
Author: Allan Peng
Summary: We try out serverless offerings from other cloud providers to see how they compare with AWS Lambda

Recently at RISELab, we’ve been working on PyWren, a distributed computation framework that leverages serverless cloud functions to run python code at massive scale. Our existing infrastructure uses Amazon Web Services: S3 for storage and Lambda for compute. With the recent introduction of serverless cloud offerings from competing cloud providers, we asked ourselves if we could generalize PyWren to other cloud infrastructures and allow users to easily configure  PyWren to run on other cloud backends.


## What is Serverless?

Cloud providers have recently launched “serverless” cloud compute offerings, allowing consumers to offload computation to the cloud without having to worry about setting up any of the underlying servers or application environment, and promising to scale out function executions under the hood. The idea is simple: offer a small but scalable execution environment with minimal overhead, abstracting the complex infrastructure. 

Fundamentally, this “serverless cloud” is a consumer-facing concept. There still are servers, containers, and complex infrastructure. The cloud is still just someone else’s computer. The main distinction of the server-less cloud is one that users and consumers see. Because the internal details are often hidden away, we’ve found that implementations and performance different serverless offerings can often be drastically different, though the end product may look the same.

## How PyWren uses the cloud

![How it works](LINK HERE)

PyWren is a python library that uses serverless compute to implement a map that executes in parallel in the cloud. While native map executes sequentially on a single thread, PyWren executes each of the mapped function calls in parallel using a separate function invocation.

PyWren takes advantage of the fact that with serverless cloud functions, we can easily spin up a large number of workers without having to worry about or take care of the infrastructure underneath. With AWS Lambda for example, we can easily run embarrassingly parallel jobs - up to 3000 simultaneous workers - without having to provision clusters, decide on machine types, pricing, or pay for devops. But would other serverless offerings allow us to scale out in a similar way?


## The Players

The main players in this space are AWS Lambda, Google Cloud Functions, and Microsoft Azure Functions.. AWS jumped out first, releasing Lambda in 2014, followed by Google Cloud and Azure in 2016.

We wanted to investigate and understand the implementation details of each cloud under the hood, and see how much these implementations would allow us to scale out to handle PyWren’s workloads.

| | Lambda | Google  | Azure |
|----------|  :--- | :--- | :--- |
| Release  | 2014 | 2016 - beta | 2016 |
| Runtimes |  Python, Java, C# Node.js | Node.js | C#, F#, Node.js |
| Regions  |  Globally available across Asia, Europe, Americas | US |  Generally available in North America, Asia, West Europe |

## Implementation

Lambda and GCF have similar models. Function code is staged in a storage bucket (Google cloud storage, S3)**, and run in an isolated container when the function is invoked. In order to keep these invocations lightweight, AWS and Google restrict access to the execution environment to writes to ephemeral disk space in `/tmp`, and limit the size of the deployed code package. Concurrent executions run in isolation, and cannot coordinate with one another.

In contrast, Azure Functions is built on top of Azure App Service, Microsoft’s app hosting platform, and thus behaves similar to a typical web-app. Invocations are served by threads running in the same sandbox, not isolated from one another. Writes to the filesystem by one function invocation can be seen by all other threads. Additionally, different functions are not isolated from one another. The code for all functions on a single account is stored on the same file system, and can be accessed and called by other functions. Furthermore, Azure lets you write to persistent storage, In contrast to Lambda and GCF, where writes to the filesystem can only be seen by other invocations when containers are reused, writes to the Azure function environment are seen by all other threads and persist across all invocations.
Another notable feature of Azure is that users have direct access to the underlying file system through a cmd console on the deployment website. Using this, we were able to make extensive modifications to the Azure Functions environment, upgrading the system Python, and installing packages such as NumPy directly on the machine image. 

| | Lambda | Google  | Azure |
|----------|  :--- | :--- | :--- |
| Deployment package size (compressed) | 50MB | 100MB | N/A |
| Memory | 1.5GB | 2GB | 1.5GB /function instance |
| Disk space | 512MB | Counted against memory |  5TB
| OS |  Amazon Linux | Debian | Windows Server 2012 |
| Isolation | Isolated containers, sometimes reused | Isolated containers, sometimes reused | Threads run in the same function instance. |


## Scaling & Limits
The unit of scalability for Lambda and GCF is a single function execution. Upon each function invocation, a container is launched or assigned to run a single execution. AWS and Google limit the number of concurrent functions you can run, and will throttle any job that exceeds the limit of 1000.

When testing PyWren on Google Cloud, we were limited by GCF’s 100GB/100s limit on inbound socket traffic. Because PyWren downloads an Anaconda runtime(120MB) into each container, the socket limit prevents us from running more than ~80 concurrent tasks. As a result, we weren’t able to achieve the same scale with PyWren’s socket-busy workload on Google Cloud as we did on Lambda, which doesn’t limit socket traffic.

In contrast to the one-container-one-execution approach, the unit of scalability for Azure Functions is coarser. Azure scales at the granularity of  a“function instance”, a sandbox that serves up to 512 threads and 32 processes in the same environment. Under the hood, Azure monitors each function’s traffic, and will only scale out to more function instances when a function is consistently receiving a significant load.** This means that Azure isn’t a great fit for handling PyWren’s workload, which has low average traffic, but very sudden high bursts.The underlying infrastructure can’t anticipate a sudden burst of dropping into the job queue, and doesn’t have a chance to scale out to handle all of them. In our tests, we found when we tried invoking ~100 concurrent functions, they would all be scheduled to run on the same machine. Each of these threads would then try to fork a Python subprocess, which would overload the machine and cause most of the invocations to get throttled and error.

## Feature Table
| | Lambda | Google  | Azure |
|----------|  :--- | :--- | :--- |
| Deployment | Command line, web portal, Python SDK | Command line | Web portal, HTTP PUT |
| Invocation authentication | Yes | No | Yes |
| Asynchronous Invocation of Functions | Yes | No Yes |


## How pywren handles multiple backends
As we’ve worked to benchmark and understand sever-less cloud infrastructure, we’ve also refactored the pywren code base to be able to handle different cloud storage and compute backends without any noticeable changes for users.

We noted that the PyWren executor and futures APIs would stay the same no matter what cloud infrastructure we were running on. The only cloud-specific moving parts, essentially, were storage and function invocation - both of which could be swapped out silently in the backend, and set based on a user’s pywren_config.

To this end, we’ve abstracted all storage operations to a generic storage handler that calls service-specific APIs under the hood. In addition, we refactored much of the lambda code to be portable to different cloud environments - using python’s platform agnostic os module to replace hard-coded unix file paths, and using Linux-specific syscalls only when available.**

**https://github.com/pywren/pywren/pull/155/files

