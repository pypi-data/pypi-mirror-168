import os

def run_command(cmd):
    """
    run cmd and return the result
    
    parameters:
        cmd: str
            command 
    
    """
    return os.popen(cmd).read()