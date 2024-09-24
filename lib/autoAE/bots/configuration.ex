defmodule AutoAE.Bots.Configuration do
  use Ecto.Schema
  import Ecto.Changeset

  schema "configurations" do
    field :country, :string
    field :region, :string
    field :min_range, :integer
    field :max_range, :integer
    field :departure_airport_code, :string
    field :auto_slot, :boolean, default: false
    field :auto_terminal, :boolean, default: false
    field :auto_hub, :boolean, default: false
    field :min_frequency, :integer
    field :max_frequency, :integer
    field :account_id, :id
    field :user_id, :id
    belongs_to :aircraft, AutoAE.Bots.Aircraft

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(configuration, attrs) do
    configuration
    |> cast(attrs, [
      :country,
      :region,
      :min_range,
      :max_range,
      :departure_airport_code,
      :auto_slot,
      :auto_terminal,
      :auto_hub,
      :min_frequency,
      :max_frequency,
      :aircraft_id
    ])
    |> validate_required([:departure_airport_code])
  end
end
