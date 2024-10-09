# Find eligible builder and runner images on Docker Hub. We use Ubuntu/Debian
# instead of Alpine to avoid DNS resolution issues in production.
#
# https://hub.docker.com/r/hexpm/elixir/tags?page=1&name=ubuntu
# https://hub.docker.com/_/ubuntu?tab=tags
#
# This file is based on these images:
#
#   - https://hub.docker.com/r/hexpm/elixir/tags - for the build image
#   - https://hub.docker.com/_/debian?tab=tags&page=1&name=bullseye-20240904-slim - for the release image
#   - https://pkgs.org/ - resource for finding needed packages
#   - Ex: hexpm/elixir:1.17.2-erlang-26.2.5.3-debian-bullseye-20240904-slim
#
ARG ELIXIR_VERSION=1.17.2
ARG OTP_VERSION=26.2.5.3
ARG DEBIAN_VERSION=bullseye-20240904

ARG BUILDER_IMAGE="hexpm/elixir:${ELIXIR_VERSION}-erlang-${OTP_VERSION}-debian-${DEBIAN_VERSION}"
ARG RUNNER_IMAGE="debian:${DEBIAN_VERSION}"

FROM ${BUILDER_IMAGE} AS builder

# install build dependencies
RUN apt update -y && apt install -y build-essential git \
  && apt-get clean && rm -f /var/lib/apt/lists/*_*

# prepare build dir
WORKDIR /app

# install hex + rebar
RUN mix local.hex --force && \
  mix local.rebar --force

# set build ENV
ENV MIX_ENV="prod"

# install mix dependencies
COPY mix.exs mix.lock ./
RUN mix deps.get --only $MIX_ENV
RUN mkdir config

# copy compile-time config files before we compile dependencies
# to ensure any relevant config change will trigger the dependencies
# to be re-compiled.
COPY config/config.exs config/${MIX_ENV}.exs config/
RUN mix deps.compile

COPY priv priv

COPY lib lib

COPY assets assets

# compile assets
RUN mix assets.deploy

# Compile the release
RUN mix compile

# Changes to config/runtime.exs don't require recompiling the code
COPY config/runtime.exs config/

COPY rel rel
RUN mix release

# start a new build stage so that the final image will only contain
# the compiled release and other runtime necessities
FROM ${RUNNER_IMAGE}

RUN apt update -y && \
  apt install -y libstdc++6 openssl libncurses5 locales ca-certificates python3 curl \
  && apt clean && rm -f /var/lib/apt/lists/*_*

RUN cp /usr/bin/python3 /usr/bin/python
# Download the latest installer
ADD https://astral.sh/uv/install.sh /app/bin/uv-installer.sh

# Set the locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

RUN useradd -ms /bin/sh docker

WORKDIR "/app"
RUN chown docker /app
RUN chown docker /app/bin
RUN chown docker /app/bin/uv-installer.sh

USER docker

WORKDIR "/app/bin"

# Run the installer then remove it
# RUN sh /app/bin/uv-installer.sh
RUN sh /app/bin/uv-installer.sh && rm /app/bin/uv-installer.sh
# Ensure the installed binary is on the `PATH`
ENV PATH="/home/docker/.cargo/bin/:$PATH"

COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
RUN uv sync --frozen

COPY models models
COPY meta_data.py meta_data.py
COPY api.py api.py
COPY run_config.py run_config.py
COPY update_aircraft.py update_aircraft.py
COPY update_session_token.py update_session_token.py
COPY update_world.py update_world.py

WORKDIR "/app"

# set runner ENV
ENV MIX_ENV="prod"

# Only copy the final release from the build stage
COPY --from=builder --chown=docker:root /app/_build/${MIX_ENV}/rel/auto_ae ./


# If using an environment that doesn't automatically reap zombie processes, it is
# advised to add an init process such as tini via `apt-get install`
# above and adding an entrypoint. See https://github.com/krallin/tini for details
# ENTRYPOINT ["/tini", "--"]

CMD ["/app/bin/server"]
