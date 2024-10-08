defmodule AutoAe.Repo.Migrations.CreateFlights do
  use Ecto.Migration

  def change do
    create table(:flights) do
      add :airport, :string
      add :flight_url, :string
      add :slots, :integer
      add :gates_available, :boolean, default: false, null: false
      add :freq_f, :float, null: true
      add :flight_demand_f, :integer, null: true
      add :freq_c, :float, null: true
      add :flight_demand_c, :integer, null: true
      add :freq_y, :float, null: true
      add :flight_demand_y, :integer, null: true
      add :avg_freq, :float, null: true
      add :configuration_criteria, :boolean, default: nil, null: true
      add :flight_created, :boolean, default: false, null: false
      add :configuration_id, references(:configurations, on_delete: :nothing)

      timestamps(type: :utc_datetime)
    end

    create index(:flights, [:configuration_id])
  end
end
