defmodule AutoAe.BotsFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `AutoAe.Bots` context.
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
      |> AutoAe.Bots.create_aircraft()

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
      |> AutoAe.Bots.create_aircraft()

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
      |> AutoAe.Bots.create_aircraft()

    aircraft
  end

  @doc """
  Generate a configuration.
  """
  def configuration_fixture(attrs \\ %{}) do
    {:ok, configuration} =
      attrs
      |> Enum.into(%{
        auto_hub: true,
        auto_slot: true,
        auto_terminal: true,
        country: "some country",
        departure_airport_code: "some departure_airport_code",
        max_frequency: 42,
        max_range: 42,
        min_frequency: 42,
        min_range: 42,
        region: "some region"
      })
      |> AutoAe.Bots.create_configuration()

    configuration
  end
end
