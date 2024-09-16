defmodule AutoAE.Repo do
  use Ecto.Repo,
    otp_app: :autoAE,
    adapter: Ecto.Adapters.SQLite3
end
