defmodule AutoAe.ConfigurationsTest do
  use AutoAe.DataCase

  alias AutoAe.Configurations

  describe "flights" do
    alias AutoAe.Configurations.Flights

    import AutoAe.ConfigurationsFixtures

    @invalid_attrs %{airport: nil, flight_url: nil, flight_created: nil, slots: nil, gates_available: nil, freq_f: nil, freq_request_f: nil, freq_c: nil, freq_request_c: nil, freq_y: nil, freq_request_y: nil, avg_freq: nil, flight_criteria: nil}

    test "list_flights/0 returns all flights" do
      flights = flights_fixture()
      assert Configurations.list_flights() == [flights]
    end

    test "get_flights!/1 returns the flights with given id" do
      flights = flights_fixture()
      assert Configurations.get_flights!(flights.id) == flights
    end

    test "create_flights/1 with valid data creates a flights" do
      valid_attrs = %{airport: "some airport", flight_url: "some flight_url", flight_created: true, slots: 42, gates_available: true, freq_f: 120.5, freq_request_f: 42, freq_c: 120.5, freq_request_c: 42, freq_y: 120.5, freq_request_y: 42, avg_freq: 120.5, flight_criteria: true}

      assert {:ok, %Flights{} = flights} = Configurations.create_flights(valid_attrs)
      assert flights.airport == "some airport"
      assert flights.flight_url == "some flight_url"
      assert flights.flight_created == true
      assert flights.slots == 42
      assert flights.gates_available == true
      assert flights.freq_f == 120.5
      assert flights.freq_request_f == 42
      assert flights.freq_c == 120.5
      assert flights.freq_request_c == 42
      assert flights.freq_y == 120.5
      assert flights.freq_request_y == 42
      assert flights.avg_freq == 120.5
      assert flights.flight_criteria == true
    end

    test "create_flights/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Configurations.create_flights(@invalid_attrs)
    end

    test "update_flights/2 with valid data updates the flights" do
      flights = flights_fixture()
      update_attrs = %{airport: "some updated airport", flight_url: "some updated flight_url", flight_created: false, slots: 43, gates_available: false, freq_f: 456.7, freq_request_f: 43, freq_c: 456.7, freq_request_c: 43, freq_y: 456.7, freq_request_y: 43, avg_freq: 456.7, flight_criteria: false}

      assert {:ok, %Flights{} = flights} = Configurations.update_flights(flights, update_attrs)
      assert flights.airport == "some updated airport"
      assert flights.flight_url == "some updated flight_url"
      assert flights.flight_created == false
      assert flights.slots == 43
      assert flights.gates_available == false
      assert flights.freq_f == 456.7
      assert flights.freq_request_f == 43
      assert flights.freq_c == 456.7
      assert flights.freq_request_c == 43
      assert flights.freq_y == 456.7
      assert flights.freq_request_y == 43
      assert flights.avg_freq == 456.7
      assert flights.flight_criteria == false
    end

    test "update_flights/2 with invalid data returns error changeset" do
      flights = flights_fixture()
      assert {:error, %Ecto.Changeset{}} = Configurations.update_flights(flights, @invalid_attrs)
      assert flights == Configurations.get_flights!(flights.id)
    end

    test "delete_flights/1 deletes the flights" do
      flights = flights_fixture()
      assert {:ok, %Flights{}} = Configurations.delete_flights(flights)
      assert_raise Ecto.NoResultsError, fn -> Configurations.get_flights!(flights.id) end
    end

    test "change_flights/1 returns a flights changeset" do
      flights = flights_fixture()
      assert %Ecto.Changeset{} = Configurations.change_flights(flights)
    end
  end
end
