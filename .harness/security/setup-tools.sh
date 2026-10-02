#!/bin/sh
# Explicit network-enabled setup; verification never invokes this script.
set -eu
destination=${1:?supply a disposable binary directory}
mkdir -p "${destination}"
case "$(uname -sm)" in
'Darwin arm64')
  arch=arm64
  hash=b40ab0ae55c505963e365f271a8d3846efbc170aa17f2607f13df610a9aeb6a5
  ;;
'Darwin x86_64')
  arch=x64
  hash=dfe101a4db2255fc85120ac7f3d25e4342c3c20cf749f2c20a18081af1952709
  ;;
*)
  printf 'Security setup supports macOS only\n' >&2
  exit 1
  ;;
esac
curl --fail --location --silent --show-error --max-time 90 \
  "https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_darwin_${arch}.tar.gz" \
  -o "${destination}/gitleaks.tar.gz"
printf '%s  %s\n' "${hash}" "${destination}/gitleaks.tar.gz" | shasum -a 256 -c -
tar -xzf "${destination}/gitleaks.tar.gz" -C "${destination}" gitleaks
"${destination}/gitleaks" version
