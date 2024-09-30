defmodule AutoAE.Repo do
  use Ecto.Repo,
    otp_app: :autoAE,
    adapter: Ecto.Adapters.Postgres
end
