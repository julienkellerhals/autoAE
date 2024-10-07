defmodule AutoAe.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      AutoAeWeb.Telemetry,
      AutoAe.Repo,
      {Ecto.Migrator,
       repos: Application.fetch_env!(:auto_ae, :ecto_repos), skip: skip_migrations?()},
      {DNSCluster, query: Application.get_env(:auto_ae, :dns_cluster_query) || :ignore},
      {Phoenix.PubSub, name: AutoAe.PubSub},
      # Start the Finch HTTP client for sending emails
      {Finch, name: AutoAe.Finch},
      # Start a worker by calling: AutoAe.Worker.start_link(arg)
      # {AutoAe.Worker, arg},
      # Start to serve requests, typically the last entry
      AutoAeWeb.Endpoint
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: AutoAe.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  @impl true
  def config_change(changed, _new, removed) do
    AutoAeWeb.Endpoint.config_change(changed, removed)
    :ok
  end

  defp skip_migrations?() do
    # By default, sqlite migrations are run when using a release
    System.get_env("RELEASE_NAME") != nil
  end
end
