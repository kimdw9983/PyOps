from pyops.init import *

if "patch" == sys.argv[1] :
  versioning  = sys.argv[2:]
  check_commit(versioning)

  run_command("poetry build --format wheel", "building dist")
  latest = get_latest_file("/dist/*.whl")
  run_command(f"pip install --upgrade dist/{latest}", "install upgrade")