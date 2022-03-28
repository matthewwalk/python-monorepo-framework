import os

# load environment variable
def defaulter(envName, defaultValue):
    try:
        input = os.environ[envName]
    except:
        return defaultValue
    return defaultValue if len(input) == 0 else input