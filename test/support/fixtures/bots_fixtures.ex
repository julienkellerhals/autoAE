defmodule AutoAE.BotsFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `AutoAE.Bots` context.
  """

  @doc """
  Generate a aircraft.
  """
  def aircraft_fixture(attrs \\ %{}) do
    {:ok, aircraft} =
      attrs
      |> Enum.into(%{
        aircraft: "some aircraft"
      })
      |> AutoAE.Bots.create_aircraft()

    aircraft
  end

  @doc """
  Generate a aircraft.
  """
  def aircraft_fixture(attrs \\ %{}) do
    {:ok, aircraft} =
      attrs
      |> Enum.into(%{
        aircraft: "some aircraft",
        min_runway: 42,
        range: 42
      })
      |> AutoAE.Bots.create_aircraft()

    aircraft
  end

  @doc """
  Generate a aircraft.
  """
  def aircraft_fixture(attrs \\ %{}) do
    {:ok, aircraft} =
      attrs
      |> Enum.into(%{
        aircraft: "some aircraft",
        min_runway: 42,
        range: 42
      })
      |> AutoAE.Bots.create_aircraft()

    aircraft
  end
end
