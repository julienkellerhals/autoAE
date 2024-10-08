defmodule AutoAeWeb.AccountController do
  use AutoAeWeb, :controller

  alias AutoAe.Accounts
  alias AutoAe.Accounts.Account
  alias AutoAe.Accounts.AccountPassword

  def index(conn, _params) do
    accounts = Accounts.list_accounts(conn.assigns.current_user.id)
    render(conn, :index, accounts: accounts)
  end

  def new(conn, _params) do
    changeset = Accounts.change_account(%Account{})
    render(conn, :new, changeset: changeset)
  end

  def create(conn, %{"account" => account_params}) do
    case Accounts.create_account(account_params) do
      {:ok, account} ->
        conn
        |> put_flash(:info, "Account created successfully.")
        |> redirect(to: ~p"/accounts/#{account}")

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, :new, changeset: changeset)
    end
  end

  def show(conn, %{"id" => id}) do
    account = Accounts.get_account!(id)
    render(conn, :show, account: account)
  end

  def edit(conn, %{"id" => id}) do
    account = Accounts.get_account!(id)
    changeset = Accounts.change_account(account)
    render(conn, :edit, account: account, changeset: changeset)
  end

  def update(conn, %{"id" => id, "account" => account_params}) do
    account = Accounts.get_account!(id)

    case Accounts.update_account(account, account_params) do
      {:ok, account} ->
        conn
        |> put_flash(:info, "Account updated successfully.")
        |> redirect(to: ~p"/accounts/#{account}")

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, :edit, account: account, changeset: changeset)
    end
  end

  def world(conn, _params) do
    changeset = Accounts.change_account_password(%AccountPassword{})

    render(conn, :world, changeset: changeset)
  end

  def run_world(conn, %{"account_password" => account_params}) do
    case Accounts.create_account_password(account_params) do
      {:ok} ->
        payload =
          %{
            username: account_params["username"],
            password: account_params["password"],
            user_id: to_string(conn.assigns.current_user.id)
          }

        {status, response} =
          ExAws.Lambda.invoke(
            "AutoAeScriptsStack-updateWorldB0013F59-s2GzEDmoStNs",
            payload,
            %{}
          )
          |> ExAws.request(region: System.get_env("AWS_REGION"))

        IO.inspect(status)
        IO.inspect(response)

        conn
        |> put_flash(
          :info,
          "Launched refresh job, please refresh after a few seconds to see the updated page."
        )
        |> redirect(to: ~p"/accounts/")

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, :world, changeset: changeset)
    end
  end

  def connect(conn, %{"account_id" => account_id}) do
    account = Accounts.get_account!(account_id)
    changeset = Accounts.change_account_password(%AccountPassword{})

    render(conn, :connect, account: account, changeset: changeset)
  end

  def run_connect(conn, %{"account_id" => account_id, "account_password" => account_params}) do
    account = Accounts.get_account!(account_id)

    case Accounts.create_account_password(account_params) do
      {:ok} ->
        payload =
          %{
            username: account.username,
            password: account_params["password"],
            world: account.world,
            airline: account.airline,
            user_id: to_string(conn.assigns.current_user.id)
          }

        {status, response} =
          ExAws.Lambda.invoke(
            "AutoAeScriptsStack-updateSessionToken92E1A2E7-gtN4PcN3n6KS",
            payload,
            %{}
          )
          |> ExAws.request(region: System.get_env("AWS_REGION"))

        IO.inspect(status)
        IO.inspect(response)

        payload =
          %{
            account_id: account_id,
            user_id: to_string(conn.assigns.current_user.id)
          }

        {status, response} =
          ExAws.Lambda.invoke(
            "AutoAeScriptsStack-updateAircraft9268BCB3-q0sUqisUtcBn",
            payload,
            %{}
          )
          |> ExAws.request(region: System.get_env("AWS_REGION"))

        IO.inspect(status)
        IO.inspect(response)

        conn
        |> put_flash(
          :info,
          "Launched refresh job, please refresh after a few seconds to see the updated page."
        )
        |> redirect(to: ~p"/accounts/")

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, :connect, account: account, changeset: changeset)
    end
  end

  def delete(conn, %{"id" => id}) do
    account = Accounts.get_account!(id)
    {:ok, _account} = Accounts.delete_account(account)

    conn
    |> put_flash(:info, "Account deleted successfully.")
    |> redirect(to: ~p"/accounts")
  end
end
