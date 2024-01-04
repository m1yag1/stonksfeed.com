FROM mcr.microsoft.com/vscode/devcontainers/base:bullseye

ARG USERNAME=vscode

# Set these in devcontainer.json
ARG OPA_VERSION
ARG TERRAFORM_VERSION
ARG TERRAGRUNT_VERSION
ARG POETRY_VERSION

ENV POETRY_VERSION=${POETRY_VERSION}

# Set timezone
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install packages
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends awscli build-essential ca-certificates curl git gnupg2 jq libffi-dev make openssh-client python3-dev python3-pip vim zsh \
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

# Install Checkov
RUN pip3 install --upgrade requests setuptools \
    && pip3 install --upgrade botocore checkov poetry

# Install OPA
RUN curl -Lo opa https://github.com/open-policy-agent/opa/releases/download/v"${OPA_VERSION}"/opa_linux_"$(dpkg --print-architecture)" \
    && chmod +x opa \
    && mv opa /usr/local/bin/


# Setup aliases and autocomplete
RUN echo "\n\
complete -C /usr/bin/aws_completer aws\n\
complete -C /usr/local/bin/terraform terraform\n\
complete -C /usr/local/bin/terraform terragrunt\n\
alias tf='terraform'\n\
alias tg='terragrunt'\n\
alias ll='la -la'" >> /home/"${USERNAME}"/.zshrc
