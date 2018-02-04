# python-jolokia [![Build Status](https://travis-ci.org/wbrefvem/python-jolokia.svg?branch=master)](https://travis-ci.org/wbrefvem/python-jolokia)  [![Coverage Status](https://coveralls.io/repos/github/wbrefvem/python-jolokia/badge.svg?branch=master)](https://coveralls.io/github/wbrefvem/python-jolokia?branch=master) [![Maintainability](https://api.codeclimate.com/v1/badges/7922b69c7f2b37a88fe3/maintainability)](https://codeclimate.com/github/wbrefvem/python-jolokia/maintainability)
This is a python client library for [Jolokia](https://jolokia.org/).

### Motivation
Jolokia provides a JMX to HTTP bridge, which opens up many possibilities for managing JMX-enabled applications outside conventional enterprise Java workflows. At present, backend libraries are only available for Java and Perl, and there's also a browser-side JavaScript library. While Python is generally more convenient for dealing with HTTP resources than Java or Perl, a client library for Jolokia is optimal.

JMX is not a platform-agnostic tech. This means that management applications for Java EE apps are almost always written in Java, which is unfortunate, as it prevents a more flexible, polyglot architecture. Enter Jolokia. By bridging JMX to HTTP, Jolokia brings Java application management into the broader world of the web, so that they can be orchestrated and managed by tools outside the stodgy, if stable, world of enterprise Java.

### Goals
Create a Python client for Jolokia that makes JMX data available both through simple abstractions aimed at the non-Java developer as well as through a full-featured API that gives the seasoned Java developer the flexibility she craves.

### Requirements

* Python 2.7, 3.[4|5|6] (Python 2.6 should work but is neither routinely tested nor supported.)
* `python-jolokia` should be transparent to different versions of the Jolokia protocol.

### Installation
For regular usage, the recommended (but not required) installation method is pipenv:

```
pipenv install jolokia
```

For hacking on `python-jolokia`, [pipenv](https://docs.pipenv.org/) is required. Fork the repo, clone it, and install dev dependencies:

```
git clone https://github.com/<user|org>/python-jolokia.git
pipenv install --dev
```

### Usage

To get a single attribute of an MBean:

```python
from jolokia import JolokiaClient


jc = JolokiaClient('http://my-jolokia-enabled-server.com/jolokia')

resp = jc.get_attribute(mbean='java.lang:type=Memory', attribute='HeapMemoryUsage')

print(resp)

{
    'request': {
        'attribute': 'HeapMemoryUsage', 
        'mbean': 'java.lang:type=Memory', 
        'type': 'read'
    }, 
    'timestamp': 1496174821, 
    'value': {
        'used': 288902152, 
        'committed': 1310720000, 
        'max': 1310720000, 
        'init': 1367343104
    }, 
    'status': 200
}

```

Or to retrieve multiple attributes, pass a list as the ```attribute``` parameter:

```python
resp = jc.get_attribute(
    mbean='java.lang:type=Memory', 
    attribute=['HeapMemoryUsage', 'NonHeapMemoryUsage']
)

print(resp)

{
    'request': {
        'type': 'read', 
        'attribute': ['HeapMemoryUsage', 'NonHeapMemoryUsage'], 
        'mbean': 'java.lang:type=Memory'
    }, 
    'value': {
        'NonHeapMemoryUsage': {
            'init': 2555904, 
            'max': 1593835520, 
            'used': 77620176, 
            'committed': 87556096
        }, 
        'HeapMemoryUsage': {
            'init': 1367343104, 
            'max': 1310720000, 
            'used': 367638816, 
            'committed': 1310720000
        }
    }, 
    'timestamp': 1496175578, 
    'status': 200
}
```

Setting attributes works the same way, except that the ```value``` parameter is also required:

```python

resp = jc.set_attribute(
    mbean='java.lang:type=ClassLoading',
    attribute='Verbose',
    value=True
)

print(resp)

{
    'request': {
        'type': 'write', 
        'attribute': 'Verbose', 
        'mbean': 'java.lang:type=ClassLoading', 
        'value': True
    }, 
    'value': False, 
    'timestamp': 1496175995, 
    'status': 200
}

```

Note that the top-level ```value``` key in the response refers to the initial value, and we can run ```get_attribute``` to verify that the value is now set to our specified value:

```python
resp = jc.get_attribute(mbean='java.lang:type=ClassLoading', attribute='Verbose')

print(resp)

{
    'request': {
        'type': 'read', 
        'attribute': 'Verbose', 
        'mbean': 'java.lang:type=ClassLoading'
    }, 
    'value': True, 
    'timestamp': 1496176091, 
    'status': 200
}
``` 

### Contributing
Coming soon...