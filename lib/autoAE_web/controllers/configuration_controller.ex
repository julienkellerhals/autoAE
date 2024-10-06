defmodule AutoAEWeb.ConfigurationController do
  use AutoAEWeb, :controller

  alias AutoAE.Bots
  alias AutoAE.Bots.Configuration

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
        conn
        |> put_flash(:info, "Configuration created successfully.")
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
    payload =
      %{
        account_id: account_id,
        configuration_id: configuration_id
        # user_id: to_string(conn.assigns.current_user.id)
      }

    {status, response} =
      ExAws.Lambda.invoke(
        "AutoAeScriptsStack-runConfiguration96A0EB2F-7r0fHL1rmB1C",
        payload,
        %{}
      )
      |> ExAws.request(region: System.get_env("AWS_REGION"))

    IO.inspect(status)
    IO.inspect(response)

    conn
    |> put_flash(:info, "Running selected configuration")
    |> redirect(to: ~p"/accounts/#{account_id}/configurations")
  end
end
