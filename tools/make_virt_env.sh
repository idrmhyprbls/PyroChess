# Create, activate, and install PyroChess

POP=0

# Must be sourced, not run
if [[ ! "${BASH_SOURCE[0]}" != "${0}" ]] ; then
  echo "Error: Source this file!"
  exit
fi

# Check if inside folder
if [ -d ../../PyroChess/tools ] ; then
  POP+=1
  pushd .. 1> /dev/null
fi

# Create virtual env
virtualenv venv
. venv/bin/activate # deactivate
pip install --editable .

# Return to previous dir
if [ $POP -gt 0 ] ; then
  popd 1> /dev/null
fi
