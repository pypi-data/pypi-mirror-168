#!/usr/bin/env bash

set -e -o pipefail -u

self_dir=$(cd "$(dirname "$0")" &>/dev/null; pwd -P)
source "$self_dir"/utils.sh

if git grep -In $'\t'; then
  die 'The above lines contain tab character (instead of spaces), please tidy up'
fi
