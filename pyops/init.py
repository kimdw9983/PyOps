import subprocess, sys, re, signal, os, glob

IS_WINDOWS = os.name == 'nt'

#TODO: make this function
MV = "move" if IS_WINDOWS else "mv"
RM = "del" if IS_WINDOWS else "rm"

args = sys.argv

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
    if supress_error : 
      print(f"{yellow}SUPRESSED")
      return None, output.decode("utf-8")
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

def check_commit(versioning: str) -> None :
  if versioning in ("no_change", "no_version") :
    return print(f"{blue}INFO{reset}\tVersioning is disabled, ignoring.")

  output, _ = run_command("git status", "git commit check")
  commit = find_regex(r"Changes not staged for commit:", output)
  if commit :
    print(f"{blue}INFO\uncommited change found. you need to commit first to version.")
    print(f"{blue}INFO\tplease check your changes or enter commit title below, press {yellow}ctrl + c{blue} to escape")
    
    title = input(f"{yellow}INPUT\t{reset}")
    run_command('git add .', f'{blue}git add .')
    run_command(f'git commit -am "{title}"', f'{blue}git commit -am "{title}"')

def get_latest_file(pattern: str="", directory: str="") -> str | None :
  if not pattern and not directory :
    print(f"{red}[ERROR]\t{yellow}get_latest_file() {red}requires pattern or directory")
    sys.exit(0)

  files = glob.glob(directory or os.getcwd() + pattern)
  latest = max(files, key=os.path.getctime).split("\\")[-1].replace("\\", "/")
  return latest