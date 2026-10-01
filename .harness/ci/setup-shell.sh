#!/bin/sh
# Official binaries, pinned release URLs and reviewed release asset digests.
set -eu
destination=${1:?supply a disposable binary directory}
mkdir -p "${destination}"
case "$(uname -sm)" in
'Darwin arm64')
  shell_arch=aarch64
  shfmt_arch=arm64
  shell_hash=339b930feb1ea764467013cc1f72d09cd6b869ebf1013296ba9055ab2ffbd26f
  shfmt_hash=d903802e0ce3ecbc82b98512f55ba370b0d37a93f3f78de394f5b657052b33dd
  ;;
'Darwin x86_64')
  shell_arch=x86_64
  shfmt_arch=amd64
  shell_hash=c2c15e08df0e8fbc374c335b230a7ee958c313fa5714817a59aa59f1aa594f51
  shfmt_hash=c31548693de6584e6164b7ed5fbb7b4a083f2d937ca94b4e0ddf59aa461a85e4
  ;;
*)
  printf 'CI shell setup supports macOS arm64/x86_64 only\n' >&2
  exit 1
  ;;
esac
curl --fail --location --silent --show-error --max-time 90 \
  "https://github.com/koalaman/shellcheck/releases/download/v0.11.0/shellcheck-v0.11.0.darwin.${shell_arch}.tar.gz" \
  -o "${destination}/shellcheck.tar.gz"
printf '%s  %s\n' "${shell_hash}" "${destination}/shellcheck.tar.gz" | shasum -a 256 -c -
tar -xzf "${destination}/shellcheck.tar.gz" -C "${destination}" \
  shellcheck-v0.11.0/shellcheck
mv "${destination}/shellcheck-v0.11.0/shellcheck" "${destination}/shellcheck"
curl --fail --location --silent --show-error --max-time 90 \
  "https://github.com/mvdan/sh/releases/download/v3.12.0/shfmt_v3.12.0_darwin_${shfmt_arch}" \
  -o "${destination}/shfmt"
printf '%s  %s\n' "${shfmt_hash}" "${destination}/shfmt" | shasum -a 256 -c -
chmod +x "${destination}/shellcheck" "${destination}/shfmt"
"${destination}/shellcheck" --version
"${destination}/shfmt" --version
