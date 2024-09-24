defmodule AutoAE.BotsTest do
  use AutoAE.DataCase

  alias AutoAE.Bots

  describe "aircraft" do
    alias AutoAE.Bots.Aircraft

    import AutoAE.BotsFixtures

    @invalid_attrs %{aircraft: nil}

    test "list_aircraft/0 returns all aircraft" do
      aircraft = aircraft_fixture()
      assert Bots.list_aircraft() == [aircraft]
    end

    test "get_aircraft!/1 returns the aircraft with given id" do
      aircraft = aircraft_fixture()
      assert Bots.get_aircraft!(aircraft.id) == aircraft
    end

    test "create_aircraft/1 with valid data creates a aircraft" do
      valid_attrs = %{aircraft: "some aircraft"}

      assert {:ok, %Aircraft{} = aircraft} = Bots.create_aircraft(valid_attrs)
      assert aircraft.aircraft == "some aircraft"
    end

    test "create_aircraft/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Bots.create_aircraft(@invalid_attrs)
    end

    test "update_aircraft/2 with valid data updates the aircraft" do
      aircraft = aircraft_fixture()
      update_attrs = %{aircraft: "some updated aircraft"}

      assert {:ok, %Aircraft{} = aircraft} = Bots.update_aircraft(aircraft, update_attrs)
      assert aircraft.aircraft == "some updated aircraft"
    end

    test "update_aircraft/2 with invalid data returns error changeset" do
      aircraft = aircraft_fixture()
      assert {:error, %Ecto.Changeset{}} = Bots.update_aircraft(aircraft, @invalid_attrs)
      assert aircraft == Bots.get_aircraft!(aircraft.id)
    end

    test "delete_aircraft/1 deletes the aircraft" do
      aircraft = aircraft_fixture()
      assert {:ok, %Aircraft{}} = Bots.delete_aircraft(aircraft)
      assert_raise Ecto.NoResultsError, fn -> Bots.get_aircraft!(aircraft.id) end
    end

    test "change_aircraft/1 returns a aircraft changeset" do
      aircraft = aircraft_fixture()
      assert %Ecto.Changeset{} = Bots.change_aircraft(aircraft)
    end
  end

  describe "aircraft" do
    alias AutoAE.Bots.Aircraft

    import AutoAE.BotsFixtures

    @invalid_attrs %{range: nil, aircraft: nil, min_runway: nil}

    test "list_aircraft/0 returns all aircraft" do
      aircraft = aircraft_fixture()
      assert Bots.list_aircraft() == [aircraft]
    end

    test "get_aircraft!/1 returns the aircraft with given id" do
      aircraft = aircraft_fixture()
      assert Bots.get_aircraft!(aircraft.id) == aircraft
    end

    test "create_aircraft/1 with valid data creates a aircraft" do
      valid_attrs = %{range: 42, aircraft: "some aircraft", min_runway: 42}

      assert {:ok, %Aircraft{} = aircraft} = Bots.create_aircraft(valid_attrs)
      assert aircraft.range == 42
      assert aircraft.aircraft == "some aircraft"
      assert aircraft.min_runway == 42
    end

    test "create_aircraft/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Bots.create_aircraft(@invalid_attrs)
    end

    test "update_aircraft/2 with valid data updates the aircraft" do
      aircraft = aircraft_fixture()
      update_attrs = %{range: 43, aircraft: "some updated aircraft", min_runway: 43}

      assert {:ok, %Aircraft{} = aircraft} = Bots.update_aircraft(aircraft, update_attrs)
      assert aircraft.range == 43
      assert aircraft.aircraft == "some updated aircraft"
      assert aircraft.min_runway == 43
    end

    test "update_aircraft/2 with invalid data returns error changeset" do
      aircraft = aircraft_fixture()
      assert {:error, %Ecto.Changeset{}} = Bots.update_aircraft(aircraft, @invalid_attrs)
      assert aircraft == Bots.get_aircraft!(aircraft.id)
    end

    test "delete_aircraft/1 deletes the aircraft" do
      aircraft = aircraft_fixture()
      assert {:ok, %Aircraft{}} = Bots.delete_aircraft(aircraft)
      assert_raise Ecto.NoResultsError, fn -> Bots.get_aircraft!(aircraft.id) end
    end

    test "change_aircraft/1 returns a aircraft changeset" do
      aircraft = aircraft_fixture()
      assert %Ecto.Changeset{} = Bots.change_aircraft(aircraft)
    end
  end

  describe "aircraft" do
    alias AutoAE.Bots.Aircraft

    import AutoAE.BotsFixtures

    @invalid_attrs %{range: nil, aircraft: nil, min_runway: nil}

    test "list_aircraft/0 returns all aircraft" do
      aircraft = aircraft_fixture()
      assert Bots.list_aircraft() == [aircraft]
    end

    test "get_aircraft!/1 returns the aircraft with given id" do
      aircraft = aircraft_fixture()
      assert Bots.get_aircraft!(aircraft.id) == aircraft
    end

    test "create_aircraft/1 with valid data creates a aircraft" do
      valid_attrs = %{range: 42, aircraft: "some aircraft", min_runway: 42}

      assert {:ok, %Aircraft{} = aircraft} = Bots.create_aircraft(valid_attrs)
      assert aircraft.range == 42
      assert aircraft.aircraft == "some aircraft"
      assert aircraft.min_runway == 42
    end

    test "create_aircraft/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Bots.create_aircraft(@invalid_attrs)
    end

    test "update_aircraft/2 with valid data updates the aircraft" do
      aircraft = aircraft_fixture()
      update_attrs = %{range: 43, aircraft: "some updated aircraft", min_runway: 43}

      assert {:ok, %Aircraft{} = aircraft} = Bots.update_aircraft(aircraft, update_attrs)
      assert aircraft.range == 43
      assert aircraft.aircraft == "some updated aircraft"
      assert aircraft.min_runway == 43
    end

    test "update_aircraft/2 with invalid data returns error changeset" do
      aircraft = aircraft_fixture()
      assert {:error, %Ecto.Changeset{}} = Bots.update_aircraft(aircraft, @invalid_attrs)
      assert aircraft == Bots.get_aircraft!(aircraft.id)
    end

    test "delete_aircraft/1 deletes the aircraft" do
      aircraft = aircraft_fixture()
      assert {:ok, %Aircraft{}} = Bots.delete_aircraft(aircraft)
      assert_raise Ecto.NoResultsError, fn -> Bots.get_aircraft!(aircraft.id) end
    end

    test "change_aircraft/1 returns a aircraft changeset" do
      aircraft = aircraft_fixture()
      assert %Ecto.Changeset{} = Bots.change_aircraft(aircraft)
    end
  end

  describe "configurations" do
    alias AutoAE.Bots.Configuration

    import AutoAE.BotsFixtures

    @invalid_attrs %{country: nil, region: nil, min_range: nil, max_range: nil, departure_airport_code: nil, auto_slot: nil, auto_terminal: nil, auto_hub: nil, min_frequency: nil, max_frequency: nil}

    test "list_configurations/0 returns all configurations" do
      configuration = configuration_fixture()
      assert Bots.list_configurations() == [configuration]
    end

    test "get_configuration!/1 returns the configuration with given id" do
      configuration = configuration_fixture()
      assert Bots.get_configuration!(configuration.id) == configuration
    end

    test "create_configuration/1 with valid data creates a configuration" do
      valid_attrs = %{country: "some country", region: "some region", min_range: 42, max_range: 42, departure_airport_code: "some departure_airport_code", auto_slot: true, auto_terminal: true, auto_hub: true, min_frequency: 42, max_frequency: 42}

      assert {:ok, %Configuration{} = configuration} = Bots.create_configuration(valid_attrs)
      assert configuration.country == "some country"
      assert configuration.region == "some region"
      assert configuration.min_range == 42
      assert configuration.max_range == 42
      assert configuration.departure_airport_code == "some departure_airport_code"
      assert configuration.auto_slot == true
      assert configuration.auto_terminal == true
      assert configuration.auto_hub == true
      assert configuration.min_frequency == 42
      assert configuration.max_frequency == 42
    end

    test "create_configuration/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Bots.create_configuration(@invalid_attrs)
    end

    test "update_configuration/2 with valid data updates the configuration" do
      configuration = configuration_fixture()
      update_attrs = %{country: "some updated country", region: "some updated region", min_range: 43, max_range: 43, departure_airport_code: "some updated departure_airport_code", auto_slot: false, auto_terminal: false, auto_hub: false, min_frequency: 43, max_frequency: 43}

      assert {:ok, %Configuration{} = configuration} = Bots.update_configuration(configuration, update_attrs)
      assert configuration.country == "some updated country"
      assert configuration.region == "some updated region"
      assert configuration.min_range == 43
      assert configuration.max_range == 43
      assert configuration.departure_airport_code == "some updated departure_airport_code"
      assert configuration.auto_slot == false
      assert configuration.auto_terminal == false
      assert configuration.auto_hub == false
      assert configuration.min_frequency == 43
      assert configuration.max_frequency == 43
    end

    test "update_configuration/2 with invalid data returns error changeset" do
      configuration = configuration_fixture()
      assert {:error, %Ecto.Changeset{}} = Bots.update_configuration(configuration, @invalid_attrs)
      assert configuration == Bots.get_configuration!(configuration.id)
    end

    test "delete_configuration/1 deletes the configuration" do
      configuration = configuration_fixture()
      assert {:ok, %Configuration{}} = Bots.delete_configuration(configuration)
      assert_raise Ecto.NoResultsError, fn -> Bots.get_configuration!(configuration.id) end
    end

    test "change_configuration/1 returns a configuration changeset" do
      configuration = configuration_fixture()
      assert %Ecto.Changeset{} = Bots.change_configuration(configuration)
    end
  end
end
