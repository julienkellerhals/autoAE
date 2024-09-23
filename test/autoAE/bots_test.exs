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
end
