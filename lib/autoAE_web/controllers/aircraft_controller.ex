defmodule AutoAEWeb.AircraftController do
  use AutoAEWeb, :controller

  alias AutoAE.Bots
  alias AutoAE.Bots.Aircraft

  def index(conn, _params) do
    aircraft = Bots.list_aircraft()
    render(conn, :index, aircraft_collection: aircraft)
  end

  def new(conn, _params) do
    changeset = Bots.change_aircraft(%Aircraft{})
    render(conn, :new, changeset: changeset)
  end

  def create(conn, %{"aircraft" => aircraft_params}) do
    case Bots.create_aircraft(aircraft_params) do
      {:ok, aircraft} ->
        conn
        |> put_flash(:info, "Aircraft created successfully.")
        |> redirect(to: ~p"/aircraft/#{aircraft}")

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, :new, changeset: changeset)
    end
  end

  def show(conn, %{"id" => id}) do
    aircraft = Bots.get_aircraft!(id)
    render(conn, :show, aircraft: aircraft)
  end

  def edit(conn, %{"id" => id}) do
    aircraft = Bots.get_aircraft!(id)
    changeset = Bots.change_aircraft(aircraft)
    render(conn, :edit, aircraft: aircraft, changeset: changeset)
  end

  def update(conn, %{"id" => id, "aircraft" => aircraft_params}) do
    aircraft = Bots.get_aircraft!(id)

    case Bots.update_aircraft(aircraft, aircraft_params) do
      {:ok, aircraft} ->
        conn
        |> put_flash(:info, "Aircraft updated successfully.")
        |> redirect(to: ~p"/aircraft/#{aircraft}")

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, :edit, aircraft: aircraft, changeset: changeset)
    end
  end

  def delete(conn, %{"id" => id}) do
    aircraft = Bots.get_aircraft!(id)
    {:ok, _aircraft} = Bots.delete_aircraft(aircraft)

    conn
    |> put_flash(:info, "Aircraft deleted successfully.")
    |> redirect(to: ~p"/aircraft")
  end
end
