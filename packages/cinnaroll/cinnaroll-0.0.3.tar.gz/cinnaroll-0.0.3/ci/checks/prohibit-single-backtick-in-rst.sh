#!/usr/bin/env bash

set -e -o pipefail -u

self_dir=$(cd "$(dirname "$0")" &>/dev/null; pwd -P)
source "$self_dir"/utils.sh

if git grep -e ' `[^`]' --and --not -e 'https://' -- '*.rst'; then
  echo
  error 'Single backticks (`...`) are notoriously confusing in ReStructuredText: unlike in Markdown, they correspond to italics, not verbatim text.'
  die 'Use the somewhat more unambiguous *...* for italics, and double backticks (``...``) for verbatim text.'
fi
