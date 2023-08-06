#!/usr/bin/env bash

set -e -o pipefail -u

self_dir=$(cd "$(dirname "$0")" &>/dev/null; pwd -P)
source "$self_dir"/utils.sh

if git grep -E '^#!/usr/bin/env python(2)?$' .; then
  die "Ambiguous python shebang, please declare shebangs that point to python3:  #!/usr/bin/env python3"
fi
