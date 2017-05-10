# python-jolokia [![Build Status](https://travis-ci.org/wbrefvem/python-jolokia.svg?branch=master)](https://travis-ci.org/wbrefvem/python-jolokia)
This is a python client library for [Jolokia](https://jolokia.org/).

### Motivation
Jolokia provides a JMX to HTTP bridge, which opens up many possibilities for managing JMX-enabled applications outside conventional enterprise Java workflows. At present, backend libraries are only available for Java and Perl, and there's also a browser-side JavaScript library. While Python is generally more convenient for dealing with HTTP resources than Java or Perl, a client library for Jolokia is optimal.

JMX is not a platform-agnostic tech. This means that management applications for Java EE apps are almost always written in Java, which is unfortunate, as it prevents a more flexible, polyglot architecture. Enter Jolokia. By bridging JMX to HTTP, Jolokia brings Java application management into the broader world of the web, so that they can be orchestrated and managed by tools outside the stodgy, if stable, world of enterprise Java.

### Goals
Create a Python client for Jolokia that makes JMX data available both through simple abstractions aimed at the non-Java developer as well as through a full-featured API that gives the seasoned Java developer the flexibility she craves.

### Note
The goal is to support Python 2.6+ and 3.2+, but at the moment only 3.5 and 3.6 are supported.