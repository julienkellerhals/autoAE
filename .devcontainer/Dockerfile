ARG ELIXIR_VERSION=1.15.0
ARG OTP_VERSION=26.0.1
ARG DEBIAN_VERSION=bullseye-20230612-slim

ARG BUILDER_IMAGE="hexpm/elixir:${ELIXIR_VERSION}-erlang-${OTP_VERSION}-debian-${DEBIAN_VERSION}"
ARG RUNNER_IMAGE="debian:${DEBIAN_VERSION}"

FROM ${BUILDER_IMAGE} as builder

RUN apt update -y && apt install inotify-tools -y

RUN mix local.hex --force

RUN pipx install poetry && poetry install