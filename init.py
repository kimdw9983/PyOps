import subprocess, sys, re, signal, os

IS_WINDOWS = os.name == 'nt'

#TODO: make function
MV = "move" if IS_WINDOWS else "mv"
RM = "del" if IS_WINDOWS else "rm"

magenta = "\x1b[35;20m"
green = "\x1b[32;20m"
blue = "\x1b[34m"
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
reset = "\x1b[0m"

_print = __builtins__['print']
def fotmat(*args, **kwargs) :
  _print(*args, reset, **kwargs) 
__builtins__['print'] = fotmat

def signal_handler(sig, frame):
  print(f'\n\n{yellow}batch inturrupted, terminating...')
  sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def handle_error(e: Exception, message: str, command: str) -> None : 
  print(f"{red}[ERROR]\t{e}")
  print(f"{red}[ERROR]\tFailed to {message}. Failed command was {yellow}{command}")
  sys.exit(0)

def run_command(command: str, desc: str, supress_error: bool = False) -> tuple[str|None, str|None] :
  try :
    print(f"{magenta}TASK{reset}\t{desc}{reset}...", end=" ")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, errors = process.communicate()
    if process.returncode != 0 or errors:
      raise Exception(errors.decode("utf-8").rstrip())

    print(f"{green}SUCCESS")
    return output.decode("utf-8"), None
  except Exception as e:
    if supress_error : return None, output.decode("utf-8")
    print(f"{red}FAILED")
    handle_error(e, desc, command)

def find_regex(pattern: str, text: str) -> str | None :
  try:
    re.compile(pattern)
  except re.error:
    return print("invalid regex pattern")

  match = re.findall(pattern, text)
  if len(match) > 1 :
    return print("regex matches more than one, try change pattern.")
  return match[0] if match else None