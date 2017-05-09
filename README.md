# python-jolokia [![Build Status](https://travis-ci.org/wbrefvem/python-jolokia.svg?branch=master)](https://travis-ci.org/wbrefvem/python-jolokia)
This is a python client library for [Jolokia](https://jolokia.org/).

### Motivation
Jolokia provides a JMX to HTTP bridge, which opens up many possibilities for managing JMX-enabled applications outside conventional enterprise Java workflows. At present, backend libraries are only available for Java and Perl, and there's also a browser-side JavaScript library. While Python is generally more convenient for dealing with HTTP resources than Java or Perl, a client library for Jolokia is optimal.

### Note
The goal is to support Python 2.6+ and 3.2+, but at the moment only 3.5 and 3.6 are supported.