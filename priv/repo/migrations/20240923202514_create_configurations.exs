defmodule AutoAE.Repo.Migrations.CreateConfigurations do
  use Ecto.Migration

  def change do
    create table(:configurations) do
      add :country, :string
      add :region, :string
      add :min_range, :integer
      add :max_range, :integer
      add :departure_airport_code, :string
      add :auto_slot, :boolean, default: false, null: false
      add :auto_terminal, :boolean, default: false, null: false
      add :auto_hub, :boolean, default: false, null: false
      add :min_frequency, :integer
      add :max_frequency, :integer
      add :account_id, references(:accounts, on_delete: :nothing)
      add :user_id, references(:users, on_delete: :nothing)
      add :aircraft_id, references(:aircraft, on_delete: :nothing)

      timestamps(type: :utc_datetime)
    end

    create index(:configurations, [:account_id])
    create index(:configurations, [:user_id])
    create index(:configurations, [:aircraft_id])
  end
end
