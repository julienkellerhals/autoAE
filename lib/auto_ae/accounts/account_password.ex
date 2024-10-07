defmodule AutoAe.Accounts.AccountPassword do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key false
  embedded_schema do
    field :username, :string
    field :password, :string
  end

  @doc false
  def changeset(account, attrs) do
    account
    |> cast(attrs, [:username, :password])
    |> validate_required([:password])
    |> validate_length(:username, min: 6)
    |> validate_length(:password, min: 6)
  end
end
