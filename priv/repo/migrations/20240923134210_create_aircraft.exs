defmodule AutoAE.Repo.Migrations.CreateAircraft do
  use Ecto.Migration

  def change do
    create table(:aircraft) do
      add :aircraft, :string
      add :range, :integer
      add :min_runway, :integer
      add :account_id, references(:accounts, on_delete: :nothing)
      add :user_id, references(:users, on_delete: :nothing)

      timestamps(type: :utc_datetime)
    end

    create index(:aircraft, [:account_id])
    create index(:aircraft, [:user_id])
  end
end
