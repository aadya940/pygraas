"""List of unsafe python functions taken from 
https://xcg.tech.gov.sg/packages/dangerousfunctions/
"""

unsafe_functions = [
    "subprocess.Popen",
    "os.system",
    "os.popen",
    "subprocess.check_output",
    "builtins.eval",
    "builtins.exec",
]
