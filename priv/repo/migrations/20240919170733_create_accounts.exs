defmodule AutoAe.Repo.Migrations.CreateAccounts do
  use Ecto.Migration

  def change do
    create table(:accounts) do
      add :username, :string
      add :world, :string, null: true
      add :airline, :string, null: true
      add :session_id, :string, null: true
      add :user_id, references(:users, on_delete: :nothing)

      timestamps(type: :utc_datetime)
    end

    create index(:accounts, [:user_id])
  end
end
