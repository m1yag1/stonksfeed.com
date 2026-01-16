FROM mcr.microsoft.com/vscode/devcontainers/base:bullseye

ARG USERNAME=vscode

# Set these in devcontainer.json
ARG TERRAFORM_VERSION
ARG TERRAGRUNT_VERSION
ARG POETRY_VERSION
ARG DOCKER_VERSION
ARG USER_UID

ENV POETRY_VERSION=${POETRY_VERSION}

# Set timezone
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install packages
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends awscli build-essential ca-certificates curl git gnupg2 jq libffi-dev make openssh-client python3-dev python3-pip python3-venv vim zsh \
    && apt-get autoremove -y && apt-get clean -y

RUN echo "$(dpkg --print-architecture)"

# Install Terraform
RUN curl -Lo terraform.zip https://releases.hashicorp.com/terraform/"${TERRAFORM_VERSION}"/terraform_"${TERRAFORM_VERSION}"_linux_"$(dpkg --print-architecture)".zip \
    && unzip terraform.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform.zip

# Install Terragrunt
RUN curl -Lo terragrunt https://github.com/gruntwork-io/terragrunt/releases/download/v"${TERRAGRUNT_VERSION}"/terragrunt_linux_"$(dpkg --print-architecture)" \
    && chmod +x terragrunt \
    && mv terragrunt /usr/local/bin/

# install docker
# Add Docker's official GPG key
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add the Docker repository to Apt sources
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update packages again and install Docker
RUN apt-get update && apt-get install -y --no-install-recommends \
    docker-ce=${DOCKER_VERSION} \
    containerd.io \
    && rm -rf /var/lib/apt/lists/*

# SET user
# RUN echo "docker:x:1000:0:docker user:/home/docker:/bin/bash" >> /etc/passwd
RUN usermod -aG docker vscode

# Install SAM App
# RUN curl -Lo aws-sam-cli.zip https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-arm64.zip \
#     && unzip aws-sam-cli.zip -d sam-install \
#     && ./sam-install/install \
#     && rm aws-sam-cli.zip

RUN pip3 install poetry

# Setup aliases and autocomplete
RUN echo "\n\
complete -C /usr/bin/aws_completer aws\n\
complete -C /usr/local/bin/terraform terraform\n\
complete -C /usr/local/bin/terraform terragrunt\n\
alias tf='terraform'\n\
alias tg='terragrunt'\n\
alias python='python3'\n\
alias ll='la -la'" >> /home/"${USERNAME}"/.zshrc
