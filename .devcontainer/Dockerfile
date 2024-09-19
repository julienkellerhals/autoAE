ARG ELIXIR_VERSION=1.17.2
ARG OTP_VERSION=26.2.5.3
ARG DEBIAN_VERSION=bookworm-20240904

ARG BUILDER_IMAGE="hexpm/elixir:${ELIXIR_VERSION}-erlang-${OTP_VERSION}-debian-${DEBIAN_VERSION}"
ARG RUNNER_IMAGE="debian:${DEBIAN_VERSION}"

FROM ${BUILDER_IMAGE} as builder

RUN apt update -y && apt install inotify-tools python3 -y
RUN cp /usr/bin/python3 /usr/bin/python

RUN mix local.hex --force
