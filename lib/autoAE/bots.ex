defmodule AutoAE.Bots do
  @moduledoc """
  The Bots context.
  """

  import Ecto.Query, warn: false
  alias AutoAE.Repo

  alias AutoAE.Bots.Aircraft

  @doc """
  Returns the list of aircraft.

  ## Examples

      iex> list_aircraft()
      [%Aircraft{}, ...]

  """
  def list_aircraft(user_id, account_id) do
    from(a in Aircraft, where: a.user_id == ^user_id and a.account_id == ^account_id)
    |> Repo.all()
  end

  @doc """
  Gets a single aircraft.

  Raises `Ecto.NoResultsError` if the Aircraft does not exist.

  ## Examples

      iex> get_aircraft!(123)
      %Aircraft{}

      iex> get_aircraft!(456)
      ** (Ecto.NoResultsError)

  """
  def get_aircraft!(id), do: Repo.get!(Aircraft, id)

  @doc """
  Creates a aircraft.

  ## Examples

      iex> create_aircraft(%{field: value})
      {:ok, %Aircraft{}}

      iex> create_aircraft(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_aircraft(attrs \\ %{}) do
    %Aircraft{}
    |> Aircraft.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a aircraft.

  ## Examples

      iex> update_aircraft(aircraft, %{field: new_value})
      {:ok, %Aircraft{}}

      iex> update_aircraft(aircraft, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_aircraft(%Aircraft{} = aircraft, attrs) do
    aircraft
    |> Aircraft.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a aircraft.

  ## Examples

      iex> delete_aircraft(aircraft)
      {:ok, %Aircraft{}}

      iex> delete_aircraft(aircraft)
      {:error, %Ecto.Changeset{}}

  """
  def delete_aircraft(%Aircraft{} = aircraft) do
    Repo.delete(aircraft)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking aircraft changes.

  ## Examples

      iex> change_aircraft(aircraft)
      %Ecto.Changeset{data: %Aircraft{}}

  """
  def change_aircraft(%Aircraft{} = aircraft, attrs \\ %{}) do
    Aircraft.changeset(aircraft, attrs)
  end

  alias AutoAE.Bots.Configuration

  @doc """
  Returns the list of configurations.

  ## Examples

      iex> list_configurations()
      [%Configuration{}, ...]

  """
  def list_configurations(user_id, account_id) do
    query =
      from a in Configuration, where: a.user_id == ^user_id, where: a.account_id == ^account_id

    query
    |> Repo.all()
  end

  @doc """
  Gets a single configuration.

  Raises `Ecto.NoResultsError` if the Configuration does not exist.

  ## Examples

      iex> get_configuration!(123)
      %Configuration{}

      iex> get_configuration!(456)
      ** (Ecto.NoResultsError)

  """
  def get_configuration!(id), do: Repo.get!(Configuration, id)

  @doc """
  Creates a configuration.

  ## Examples

      iex> create_configuration(%{field: value})
      {:ok, %Configuration{}}

      iex> create_configuration(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_configuration(attrs \\ %{}) do
    %Configuration{}
    |> Configuration.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a configuration.

  ## Examples

      iex> update_configuration(configuration, %{field: new_value})
      {:ok, %Configuration{}}

      iex> update_configuration(configuration, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_configuration(%Configuration{} = configuration, attrs) do
    configuration
    |> Configuration.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a configuration.

  ## Examples

      iex> delete_configuration(configuration)
      {:ok, %Configuration{}}

      iex> delete_configuration(configuration)
      {:error, %Ecto.Changeset{}}

  """
  def delete_configuration(%Configuration{} = configuration) do
    Repo.delete(configuration)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking configuration changes.

  ## Examples

      iex> change_configuration(configuration)
      %Ecto.Changeset{data: %Configuration{}}

  """
  def change_configuration(%Configuration{} = configuration, attrs \\ %{}) do
    Configuration.changeset(configuration, attrs)
  end
end
