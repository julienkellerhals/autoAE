defmodule AutoAe.Configurations.Flights do
  use Ecto.Schema
  import Ecto.Changeset

  schema "flights" do
    field :airport, :string
    field :flight_url, :string
    field :flight_created, :boolean, default: false
    field :slots, :integer
    field :gates_available, :boolean, default: false
    field :freq_f, :float
    field :freq_request_f, :integer
    field :freq_c, :float
    field :freq_request_c, :integer
    field :freq_y, :float
    field :freq_request_y, :integer
    field :avg_freq, :float
    field :flight_criteria, :boolean, default: false
    field :configuration_id, :id

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(flights, attrs) do
    flights
    |> cast(attrs, [:airport, :flight_url, :flight_created, :slots, :gates_available, :freq_f, :freq_request_f, :freq_c, :freq_request_c, :freq_y, :freq_request_y, :avg_freq, :flight_criteria])
    |> validate_required([:airport, :flight_url, :flight_created, :slots, :gates_available, :freq_f, :freq_request_f, :freq_c, :freq_request_c, :freq_y, :freq_request_y, :avg_freq, :flight_criteria])
  end
end
