Title: getting started
Slug: gettingstarted
Authors: pywren
Summary: Getting started with pywren
status: hidden


To get started, make sure you have an AWS account, and install PyWren. 

### Obtaining an Amazon Web Services account

First make sure you are signed up for [Amazon Web Services](https://aws.amazon.com/). We recomment then installing the AWS command-line utilities via
```console
pip install awscli
```

and following [their configuration instructions](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html )

### Install PyWren
You can do the installation from either PyPI (recommended):

```console
$ pip install pywren
```

or from the [git repository](https://github.com/pywren/pywren/). This
installs the pywren library as well as the `pywren` command-line tool. 

### Interactive PyWren setup

As of `v0.2` PyWren now has an interactive setup script, which you can
run via `pywren-setup`, which will prompt you for various configuration
options. It is recommended to hit enter and simply accept the defaults. 


```console
$ pywren-setup

This is the PyWren interactive setup script
Your AWS configuration appears to be set up, and your account ID is 71825125821
This interactive script will set up your initial PyWren configuration.
If this is your first time using PyWren then accepting the defaults should be fine.
What is your default aws region? [us-west-2]:
Location for config file:  [~/.pywren_config]:
PyWren requires an s3 bucket to store intermediate data. What s3 bucket would you like to use? [jonas-pywren-604]:
Bucket does not currently exist, would you like to create it? [Y/n]: Y
PyWren prefixes every object it puts in S3 with a particular prefix.
PyWren s3 prefix:  [pywren.jobs]:
Would you like to configure advanced PyWren properties? [y/N]:
PyWren standalone mode uses dedicated AWS instances to run PyWren tasks. This is more flexible, but more expensive with fewer simultaneous workers.
Would you like to enable PyWren standalone mode? [y/N]:
Creating config /Users/jonas/.pywren_config
new default file created in ~/.pywren_config
lambda role is pywren_exec_role_1
Creating bucket jonas-pywren-604.
Creating role.
Deploying lambda.
Pausing for 5 seconds for changes to propagate.
Pausing for 5 seconds for changes to propagate. 
Successfully created function. 
Pausing for 10 sec for changes to propoagate.
function returned: Hello world
```


## Manual setup
The manual setup is only recommended for advanced users. 

Before you get started, make sure you have your AWS credentials set up 
properly for use via Boto, the python AWS library. 

```console
$ pywren get_aws_account_id
Your AWS account ID is 942315755674
```

Run the following from the prompt:

```console
$ pywren create_config 
$ pywren create_role
$ pywren create_bucket
$ pywren deploy_lambda
```

1. This will create a default configuration file and place it in `~/.pywren_config`. 
2. Create the default IAM role to run the lambda process as `pywren_exec_role`
3. Deploy the lambda function to AWS using your account as `pywren1`. 
4. Create a bucket in your default AZ named `pywren-bucket`
4. Place all intermediate data in `pywren-bucket/pywren.jobs`. 

### Testing

You should now be able to run a test function . You should see the following:

```console
$ pywren test_function

function returned: Hello world
```

### Next steps
Check out [the examples](https://github.com/pywren/examples)


## Debugging (When things go wrong)

Pywren will print logging info to console by setting the environment
varible as follows:

```
PYWREN_LOGLEVEL=INFO
```

Logs are written to AWS Cloudwatch. To print the latest cloudwatch from the commandline use:
```
pywren print_latest_logs
```

To inspect the logs through the AWS GUI get the URL for the current worker
via 
```
pywren log_url
```

## Permissions and IAM 

PyWren needs various permissions for the automatic setup script to work. 
Please see an example of an AWS policy with the necessary permissions [in the PyWren source](https://github.com/pywren/pywren/blob/master/tests/default_pywren_user_permissions.json ) 
