defmodule AutoAe.Configurations.Flights do
  use Ecto.Schema
  import Ecto.Changeset

  schema "flights" do
    field :airport, :string
    field :flight_url, :string
    field :slots, :integer
    field :gates_available, :boolean, default: false
    field :freq_f, :float
    field :flight_demand_f, :integer
    field :freq_c, :float
    field :flight_demand_c, :integer
    field :freq_y, :float
    field :flight_demand_y, :integer
    field :avg_freq, :float
    field :configuration_criteria, :boolean, default: false
    field :flight_created, :boolean, default: false
    field :configuration_id, :id

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(flights, attrs) do
    flights
    |> cast(attrs, [
      :airport,
      :flight_url,
      :flight_created
    ])
    |> validate_required([
      :airport,
      :flight_url,
      :flight_created
    ])
  end
end
