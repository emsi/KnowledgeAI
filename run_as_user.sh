#!/bin/bash

set -Eeuo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)

# set default values
CUDA_VERSION="11.7.1-cudnn8-runtime-ubuntu22.04"
TF_VERSION="${TF_VERSION:-"2.10"}"

# source existing env values
. "${script_dir}"/.env 2>/dev/null || true

# refresh repo
echo "$(cd "${script_dir}"; git pull)" >> /dev/null

# set variables for  uid/gid and prefix project name with username
cat > "${script_dir}/.env" << EOF
CUDA_VERSION="${CUDA_VERSION}"
TF_VERSION="${TF_VERSION}"

COMPOSE_USER_ID=$(id -u)
COMPOSE_GROUP_ID=$(id -g)
EOF

# create appropriate sudoers.sh script
cat > "${script_dir}/sudoers.sh" << EOF
#!/bin/bash

echo "$(whoami) ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/sudoers
chown 0:0 /etc/sudoers.d/sudoers

mkdir -p "${HOME}/.ssh"
chown -R $(id -u):$(id -g) "${HOME}"
EOF
chmod +x sudoers.sh


if [ "$(which docker-compose)" ]; then
	compose='docker-compose'
else
	compose='docker compose'
fi

$compose restart

$compose logs -f
