defmodule AutoAe.Repo do
  use Ecto.Repo,
    otp_app: :auto_ae,
    adapter: Ecto.Adapters.Postgres
end
