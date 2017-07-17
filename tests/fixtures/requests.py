VALID_EXEC = {
    'type': 'exec',
    'mbean': 'java.lang:type=Threading',
    'operation': 'dumpAllThreads',
    'arguments': [True, True]
}

VALID_SEARCH = {
    'type': 'search',
    'mbean': 'java.lang:*'
}
