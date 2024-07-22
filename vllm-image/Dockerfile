ARG ROOT_CONTAINER=ubuntu:24.04

FROM $ROOT_CONTAINER AS foundation

# Fix the UID conflict with user ubuntu when jovyan needs to be created later. 
# See https://bugs.launchpad.net/cloud-images/+bug/2005129
RUN touch /var/mail/ubuntu && chown ubuntu /var/mail/ubuntu && userdel -r ubuntu

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Avoid prompt for user input for installation of dependencies
ENV DEBIAN_FRONTEND=noninteractive

ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID} \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8 \
    TZ=Asia/Hong_Kong
ENV PATH="${CONDA_DIR}/bin:${PATH}" \
    HOME="/home/${NB_USER}"

USER root
FROM foundation AS base

RUN apt-get update --yes && \
    # Patch newly discovered vulnerabilities in apt-get packages
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    # To extract micromamba
    bzip2 \
    ca-certificates \
    locales \
    sudo \
    # used as an entrypoint that reaps zombie processes.
    # See https://github.com/krallin/tini#why-tini
    tini \
    wget \
    less \
    curl \
    patch \
    && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    echo "C.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


# A script to correct permissions after running certain commands
COPY fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions

# Enable prompt color in the skeleton .bashrc before creating the default NB_USER
# hadolint ignore=SC2016
RUN sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc && \
   # Add call to conda init script see https://stackoverflow.com/a/58081608/4413446
   echo 'eval "$(conda shell.bash hook)"' >> /etc/skel/.bashrc && \
   # fix https://github.com/jupyter/docker-stacks/issues/815
   cat /etc/skel/.bashrc >> /etc/bash.bashrc

# Create NB_USER with name jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers && \
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers && \
    useradd -l -m -s /bin/bash -N -u "${NB_UID}" "${NB_USER}" && \
    mkdir -p "${CONDA_DIR}" && \
    chown "${NB_USER}:${NB_GID}" "${CONDA_DIR}" && \
    chmod g+w /etc/passwd && \
    fix-permissions "${HOME}" && \
    fix-permissions "${CONDA_DIR}"

USER ${NB_UID}

# Pin python version here, or set it to "default"
ARG PYTHON_VERSION=3.11

# Download and install Micromamba, and initialize Conda prefix.
#   <https://github.com/mamba-org/mamba#micromamba>
# Install Python, Mamba and jupyter_core
COPY --chown="${NB_UID}:${NB_GID}" initial-condarc "${CONDA_DIR}/.condarc"
WORKDIR /tmp
RUN set -x && \
    arch=$(uname -m) && \
    if [ "${arch}" = "x86_64" ]; then \
        # Should be simpler, see <https://github.com/mamba-org/mamba/issues/1437>
        arch="64"; \
    fi &&  \
    wget --progress=dot:giga -O /tmp/micromamba.tar.bz2 \
        "https://micromamba.snakepit.net/api/micromamba/linux-${arch}/latest" && \
    tar -xvjf /tmp/micromamba.tar.bz2 --strip-components=1 bin/micromamba && \
    rm /tmp/micromamba.tar.bz2 && \
    PYTHON_SPECIFIER="python=${PYTHON_VERSION}" && \
    if [[ "${PYTHON_VERSION}" == "default" ]]; then PYTHON_SPECIFIER="python"; fi && \
    # Install the packages
    ./micromamba install \
        --root-prefix="${CONDA_DIR}" \
        --prefix="${CONDA_DIR}" \
        --yes \
        "${PYTHON_SPECIFIER}" \
        'mamba' \
        'jupyter_core' && \
    rm micromamba && \
    # Pin major.minor version of python
    mamba list python | grep '^python ' | tr -s ' ' | cut -d ' ' -f 1,2 >> "${CONDA_DIR}/conda-meta/pinned" && \
    # mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# CUDA
RUN mamba install --quiet --yes \
    'cuda' \
    && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}"

RUN \
    pip install --quiet --no-cache-dir \
    'vllm==0.5.2' \
    && \
    fix-permissions "${CONDA_DIR}"

# ----------------------------------------------------------

FROM foundation AS prod

COPY --from=base /etc/ /etc/
COPY --from=base /usr/ /usr/
COPY --from=base /var/ /var/
COPY --from=base /home/ /home/
COPY --from=base /opt/ /opt/

USER ${NB_UID}
WORKDIR ${HOME}

# Copy local files as late as possible to avoid cache busting
COPY start.sh /usr/local/bin/

# Configure container startup
ENTRYPOINT ["tini", "-g", "--", "start.sh", "python", "-m", "vllm.entrypoints.openai.api_server"]

ENV VLLM_PORT=8000 \
    API_KEY=""
EXPOSE ${VLLM_PORT}

# To avoid fatal internal server error that kills the engine
RUN VLLM_PATH=$(pip show vllm | grep Location | cut -d' ' -f2) || { echo "vllm location not found" >&2; exit 1; } && \
    API_SERVER_PATH="$VLLM_PATH/vllm/entrypoints/openai/api_server.py" && \
    patch $API_SERVER_PATH - <<EOF
--- entrypoints/openai/api_server.py.orig	2024-07-23 02:22:08.321456687 +0800
+++ entrypoints/openai/api_server.py	2024-07-23 02:17:28.121324937 +0800
@@ -150,6 +150,8 @@
 
 @router.post("/v1/embeddings")
 async def create_embedding(request: EmbeddingRequest, raw_request: Request):
+    if not engine.engine.model_config.embedding_mode:
+        return JSONResponse(content={"detail": "This action is forbidden for the current model."}, status_code=403)
     generator = await openai_serving_embedding.create_embedding(
         request, raw_request)
     if isinstance(generator, ErrorResponse):
EOF
