defmodule AutoAeWeb.ConfigurationController do
  use AutoAeWeb, :controller

  alias AutoAe.Bots
  alias AutoAe.Bots.Configuration
  alias AutoAe.Configurations

  def index(conn, %{"account_id" => account_id}) do
    configurations = Bots.list_configurations(conn.assigns.current_user.id, account_id)
    render(conn, :index, account_id: account_id, configurations: configurations)
  end

  def new(conn, %{"account_id" => account_id}) do
    changeset = Bots.change_configuration(%Configuration{})
    aircraft = Bots.list_aircraft(conn.assigns.current_user.id, account_id)
    render(conn, :new, account_id: account_id, changeset: changeset, aircraft: aircraft)
  end

  def create(conn, %{"account_id" => account_id, "configuration" => configuration_params}) do
    configuration_params
    |> Map.put("user_id", conn.assigns.current_user.id)
    |> Map.put("account_id", account_id)
    |> Bots.create_configuration()
    |> case do
      {:ok, configuration} ->
        payload =
          %{
            configuration_id: configuration.id
          }

        {status, response} =
          ExAws.Lambda.invoke(
            "AutoAeScriptsStack-updateFlightsC2110FE0-HbcRQDnpcNAH",
            payload,
            %{}
          )
          |> ExAws.request(region: System.get_env("AWS_REGION"))

        IO.inspect(status)
        IO.inspect(response)

        conn
        |> put_flash(:info, "Configuration created successfully and flight list created.")
        |> redirect(to: ~p"/accounts/#{account_id}/configurations/#{configuration}")

      {:error, %Ecto.Changeset{} = changeset} ->
        aircraft = Bots.list_aircraft(conn.assigns.current_user.id, account_id)
        render(conn, :new, account_id: account_id, changeset: changeset, aircraft: aircraft)
    end
  end

  def show(conn, %{"account_id" => account_id, "id" => id}) do
    configuration = Bots.get_configuration!(id)
    render(conn, :show, account_id: account_id, configuration: configuration)
  end

  def edit(conn, %{"account_id" => account_id, "id" => id}) do
    configuration = Bots.get_configuration!(id)
    changeset = Bots.change_configuration(configuration)

    render(conn, :edit,
      account_id: account_id,
      configuration: configuration,
      changeset: changeset
    )
  end

  def update(conn, %{
        "account_id" => account_id,
        "id" => id,
        "configuration" => configuration_params
      }) do
    configuration = Bots.get_configuration!(id)

    case Bots.update_configuration(configuration, configuration_params) do
      {:ok, configuration} ->
        conn
        |> put_flash(:info, "Configuration updated successfully.")
        |> redirect(to: ~p"/accounts/#{account_id}/configurations/#{configuration}")

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, :edit,
          account_id: account_id,
          configuration: configuration,
          changeset: changeset
        )
    end
  end

  def delete(conn, %{"account_id" => account_id, "id" => id}) do
    configuration = Bots.get_configuration!(id)
    {:ok, _configuration} = Bots.delete_configuration(configuration)

    conn
    |> put_flash(:info, "Configuration deleted successfully.")
    |> redirect(to: ~p"/accounts/#{account_id}/configurations")
  end

  def run(conn, %{"account_id" => account_id, "configuration_id" => configuration_id}) do
    Task.start(fn ->
      flights = Configurations.list_available_flights(configuration_id)

      for flight <- flights do
        IO.inspect(flight)

        payload = %{
          flight_id: flight.id
        }

        # Invoke AWS Lambda function
        {status, response} =
          ExAws.Lambda.invoke(
            "AutoAeScriptsStack-runConfiguration96A0EB2F-7r0fHL1rmB1C",
            payload,
            %{}
          )
          |> ExAws.request(region: System.get_env("AWS_REGION"))

        IO.inspect(status)
        IO.inspect(response)
      end
    end)

    # Respond to the user immediately
    conn
    |> put_flash(:info, "Running flight creation in the background.")
    |> redirect(to: ~p"/accounts/#{account_id}/configurations/#{configuration_id}/flights/")
  end
end
