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
  def list_aircraft do
    Repo.all(Aircraft)
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
end
