from pyops.init import *

if "patch" == sys.argv[1] :
  versioning  = sys.argv[1]

  if versioning not in ("no_version", "no_change") :
    title = check_commit()
    output, error = run_command(f"poetry version {versioning}", "versioning")
    version = find_regex(r'to (\d+\.\d+\.\d+)', output)
    print(f"{blue}INFO{reset}\tUpdated version to {yellow}{version}")
    run_command('git add .', f'{blue}git add .')
    run_command(f'git commit -am "{title}"', f'{blue}git commit -am "{title}"')
    run_command(f"git tag v{version}", f'git version tag')
  else : 
    print(f"{blue}INFO{reset}\tVersioning is disabled, ignoring.")

  run_command("poetry build --format wheel", "building dist")
  latest = get_latest_file("/dist/*.whl")
  run_command(f"pip install --upgrade dist/{latest}", "install upgrade")