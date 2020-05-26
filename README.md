# aaa_aws_audit
Alex A. Anikin 


Module for fast get information from AWS accounts entire Organization or 
flat list of accounts from text-file using using AssumeRole mechanizm. 

Main features:
- module encapsulation, just write a code and pass function name using command line 
- command line support
- multithreading support
- retriving account list from your AWS Organization
- authentication using stored credentials or using AWS access keys from command line
- encapsulated logic for output and report saving 
- easy to add own reports without module logic changes  
- exapmles and out of the box extension modules

Tools: Python3, boto3, threading, mock 
