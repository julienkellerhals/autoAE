defmodule AutoAe.ConfigurationsFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `AutoAe.Configurations` context.
  """

  @doc """
  Generate a flights.
  """
  def flights_fixture(attrs \\ %{}) do
    {:ok, flights} =
      attrs
      |> Enum.into(%{
        airport: "some airport",
        avg_freq: 120.5,
        flight_created: true,
        flight_criteria: true,
        flight_url: "some flight_url",
        freq_c: 120.5,
        freq_f: 120.5,
        freq_request_c: 42,
        freq_request_f: 42,
        freq_request_y: 42,
        freq_y: 120.5,
        gates_available: true,
        slots: 42
      })
      |> AutoAe.Configurations.create_flights()

    flights
  end
end
