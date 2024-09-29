defmodule AutoAEWeb.AircraftController do
  use AutoAEWeb, :controller

  alias AutoAE.Bots
  alias AutoAE.Bots.Aircraft

  def index(conn, %{"account_id" => account_id}) do
    aircraft = Bots.list_aircraft()
    render(conn, :index, account_id: account_id, aircraft_collection: aircraft)
  end

  def new(conn, %{"account_id" => account_id}) do
    changeset = Bots.change_aircraft(%Aircraft{})
    render(conn, :new, account_id: account_id, changeset: changeset)
  end

  def create(conn, %{"account_id" => account_id, "aircraft" => aircraft_params}) do
    case Bots.create_aircraft(aircraft_params) do
      {:ok, aircraft} ->
        conn
        |> put_flash(:info, "Aircraft created successfully.")
        |> redirect(to: ~p"/accounts/#{account_id}/aircraft/#{aircraft}")

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, :new, account_id: account_id, changeset: changeset)
    end
  end

  def show(conn, %{"account_id" => account_id, "id" => id}) do
    aircraft = Bots.get_aircraft!(id)
    render(conn, :show, account_id: account_id, aircraft: aircraft)
  end

  def edit(conn, %{"account_id" => account_id, "id" => id}) do
    aircraft = Bots.get_aircraft!(id)
    changeset = Bots.change_aircraft(aircraft)
    render(conn, :edit, account_id: account_id, aircraft: aircraft, changeset: changeset)
  end

  def update(conn, %{"account_id" => account_id, "id" => id, "aircraft" => aircraft_params}) do
    aircraft = Bots.get_aircraft!(id)

    case Bots.update_aircraft(aircraft, aircraft_params) do
      {:ok, aircraft} ->
        conn
        |> put_flash(:info, "Aircraft updated successfully.")
        |> redirect(to: ~p"/accounts/#{account_id}/aircraft/#{aircraft}")

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, :edit, account_id: account_id, aircraft: aircraft, changeset: changeset)
    end
  end

  def delete(conn, %{"account_id" => account_id, "id" => id}) do
    aircraft = Bots.get_aircraft!(id)
    {:ok, _aircraft} = Bots.delete_aircraft(aircraft)

    conn
    |> put_flash(:info, "Aircraft deleted successfully.")
    |> redirect(to: ~p"/accounts/#{account_id}/aircraft")
  end
end
