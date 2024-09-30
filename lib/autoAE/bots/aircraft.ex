defmodule AutoAE.Bots.Aircraft do
  use Ecto.Schema
  import Ecto.Changeset

  schema "aircraft" do
    field :range, :integer
    field :aircraft, :string
    field :min_runway, :integer
    field :account_id, :id
    belongs_to :user, AutoAE.Accounts.User

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(aircraft, attrs) do
    aircraft
    |> cast(attrs, [:aircraft, :range, :min_runway])
    |> validate_required([:aircraft, :range, :min_runway])
  end
end
