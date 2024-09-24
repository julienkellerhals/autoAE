defmodule AutoAEWeb.ConfigurationController do
  use AutoAEWeb, :controller

  alias AutoAE.Bots
  alias AutoAE.Bots.Configuration

  def index(conn, _params) do
    configurations = Bots.list_configurations()
    render(conn, :index, configurations: configurations)
  end

  def new(conn, _params) do
    changeset = Bots.change_configuration(%Configuration{})
    aircraft = Bots.list_aircraft()
    render(conn, :new, changeset: changeset, aircraft: aircraft)
  end

  def create(conn, %{"configuration" => configuration_params}) do
    IO.inspect(configuration_params)

    case Bots.create_configuration(configuration_params) do
      {:ok, configuration} ->
        conn
        |> put_flash(:info, "Configuration created successfully.")
        |> redirect(to: ~p"/configurations/#{configuration}")

      {:error, %Ecto.Changeset{} = changeset} ->
        aircraft = Bots.list_aircraft()
        render(conn, :new, changeset: changeset, aircraft: aircraft)
    end
  end

  def show(conn, %{"id" => id}) do
    configuration = Bots.get_configuration!(id)
    render(conn, :show, configuration: configuration)
  end

  def edit(conn, %{"id" => id}) do
    configuration = Bots.get_configuration!(id)
    changeset = Bots.change_configuration(configuration)
    render(conn, :edit, configuration: configuration, changeset: changeset)
  end

  def update(conn, %{"id" => id, "configuration" => configuration_params}) do
    configuration = Bots.get_configuration!(id)

    case Bots.update_configuration(configuration, configuration_params) do
      {:ok, configuration} ->
        conn
        |> put_flash(:info, "Configuration updated successfully.")
        |> redirect(to: ~p"/configurations/#{configuration}")

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, :edit, configuration: configuration, changeset: changeset)
    end
  end

  def delete(conn, %{"id" => id}) do
    configuration = Bots.get_configuration!(id)
    {:ok, _configuration} = Bots.delete_configuration(configuration)

    conn
    |> put_flash(:info, "Configuration deleted successfully.")
    |> redirect(to: ~p"/configurations")
  end
end
