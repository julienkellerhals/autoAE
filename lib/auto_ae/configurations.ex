defmodule AutoAe.Configurations do
  @moduledoc """
  The Configurations context.
  """

  import Ecto.Query, warn: false
  alias AutoAe.Repo

  alias AutoAe.Configurations.Flights

  @doc """
  Returns the list of flights belonging to the configuration.

  ## Examples

      iex> list_flights(1)
      [%Flights{}, ...]

  """
  def list_flights(configuration_id) do
    from(f in Flights,
      where: f.configuration_id == ^configuration_id and f.flight_created == false,
      order_by: f.id
    )
    |> Repo.all()
  end

  @doc """
  Returns the list of all available flights belonging to the configuration.

  ## Examples

      iex> list_available_flights(1)
      [%Flights{}, ...]

  """
  def list_available_flights(configuration_id) do
    Flights
    |> where([f], f.configuration_id == ^configuration_id)
    |> where([f], f.flight_created == false)
    |> where([f], is_nil(f.configuration_criteria) or f.configuration_criteria == true)
    |> order_by([f], f.id)
    |> Repo.all()
  end

  @doc """
  Gets a single flights.

  Raises `Ecto.NoResultsError` if the Flights does not exist.

  ## Examples

      iex> get_flights!(123)
      %Flights{}

      iex> get_flights!(456)
      ** (Ecto.NoResultsError)

  """
  def get_flights!(id), do: Repo.get!(Flights, id)

  @doc """
  Creates a flights.

  ## Examples

      iex> create_flights(%{field: value})
      {:ok, %Flights{}}

      iex> create_flights(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_flights(attrs \\ %{}) do
    %Flights{}
    |> Flights.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a flights.

  ## Examples

      iex> update_flights(flights, %{field: new_value})
      {:ok, %Flights{}}

      iex> update_flights(flights, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_flights(%Flights{} = flights, attrs) do
    flights
    |> Flights.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a flights.

  ## Examples

      iex> delete_flights(flights)
      {:ok, %Flights{}}

      iex> delete_flights(flights)
      {:error, %Ecto.Changeset{}}

  """
  def delete_flights(%Flights{} = flights) do
    Repo.delete(flights)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking flights changes.

  ## Examples

      iex> change_flights(flights)
      %Ecto.Changeset{data: %Flights{}}

  """
  def change_flights(%Flights{} = flights, attrs \\ %{}) do
    Flights.changeset(flights, attrs)
  end
end
