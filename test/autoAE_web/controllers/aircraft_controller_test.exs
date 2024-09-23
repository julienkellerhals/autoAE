defmodule AutoAEWeb.AircraftControllerTest do
  use AutoAEWeb.ConnCase

  import AutoAE.BotsFixtures

  @create_attrs %{range: 42, aircraft: "some aircraft", min_runway: 42}
  @update_attrs %{range: 43, aircraft: "some updated aircraft", min_runway: 43}
  @invalid_attrs %{range: nil, aircraft: nil, min_runway: nil}

  describe "index" do
    test "lists all aircraft", %{conn: conn} do
      conn = get(conn, ~p"/aircraft")
      assert html_response(conn, 200) =~ "Listing Aircraft"
    end
  end

  describe "new aircraft" do
    test "renders form", %{conn: conn} do
      conn = get(conn, ~p"/aircraft/new")
      assert html_response(conn, 200) =~ "New Aircraft"
    end
  end

  describe "create aircraft" do
    test "redirects to show when data is valid", %{conn: conn} do
      conn = post(conn, ~p"/aircraft", aircraft: @create_attrs)

      assert %{id: id} = redirected_params(conn)
      assert redirected_to(conn) == ~p"/aircraft/#{id}"

      conn = get(conn, ~p"/aircraft/#{id}")
      assert html_response(conn, 200) =~ "Aircraft #{id}"
    end

    test "renders errors when data is invalid", %{conn: conn} do
      conn = post(conn, ~p"/aircraft", aircraft: @invalid_attrs)
      assert html_response(conn, 200) =~ "New Aircraft"
    end
  end

  describe "edit aircraft" do
    setup [:create_aircraft]

    test "renders form for editing chosen aircraft", %{conn: conn, aircraft: aircraft} do
      conn = get(conn, ~p"/aircraft/#{aircraft}/edit")
      assert html_response(conn, 200) =~ "Edit Aircraft"
    end
  end

  describe "update aircraft" do
    setup [:create_aircraft]

    test "redirects when data is valid", %{conn: conn, aircraft: aircraft} do
      conn = put(conn, ~p"/aircraft/#{aircraft}", aircraft: @update_attrs)
      assert redirected_to(conn) == ~p"/aircraft/#{aircraft}"

      conn = get(conn, ~p"/aircraft/#{aircraft}")
      assert html_response(conn, 200) =~ "some updated aircraft"
    end

    test "renders errors when data is invalid", %{conn: conn, aircraft: aircraft} do
      conn = put(conn, ~p"/aircraft/#{aircraft}", aircraft: @invalid_attrs)
      assert html_response(conn, 200) =~ "Edit Aircraft"
    end
  end

  describe "delete aircraft" do
    setup [:create_aircraft]

    test "deletes chosen aircraft", %{conn: conn, aircraft: aircraft} do
      conn = delete(conn, ~p"/aircraft/#{aircraft}")
      assert redirected_to(conn) == ~p"/aircraft"

      assert_error_sent 404, fn ->
        get(conn, ~p"/aircraft/#{aircraft}")
      end
    end
  end

  defp create_aircraft(_) do
    aircraft = aircraft_fixture()
    %{aircraft: aircraft}
  end
end
