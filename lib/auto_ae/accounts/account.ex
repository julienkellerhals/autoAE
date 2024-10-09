defmodule AutoAe.Accounts.Account do
  use Ecto.Schema
  import Ecto.Changeset

  schema "accounts" do
    field :session_id, :string
    field :username, :string
    field :world, :string
    field :airline, :string
    belongs_to :user, AutoAe.Accounts.User

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(account, attrs) do
    account
    |> cast(attrs, [:username, :world, :airline, :session_id])
    # |> validate_required([:username, :world, :airline, :session_id])
    |> validate_required([:username])
  end
end
