defmodule AutoAEWeb.AccountController do
  use AutoAEWeb, :controller

  alias AutoAE.Accounts
  alias AutoAE.Accounts.Account
  alias AutoAE.Accounts.AccountPassword

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
        System.cmd("python3", [
          "update_world.py",
          "--username",
          account_params["username"],
          "--password",
          account_params["password"],
          "--user_id",
          to_string(conn.assigns.current_user.id)
        ])

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
        System.cmd("python3", [
          "update_session_token.py",
          "-u",
          account.username,
          "-p",
          account_params["password"],
          "-w",
          account.world,
          "-a",
          account.airline,
          "--user_id",
          to_string(conn.assigns.current_user.id)
        ])

        Task.async(fn ->
          System.cmd("python3", [
            "update_aircraft.py",
            "--account_id",
            account_id,
            "--user_id",
            to_string(conn.assigns.current_user.id)
          ])
        end)

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
