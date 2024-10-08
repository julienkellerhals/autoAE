defmodule AutoAeWeb.ConfigurationControllerTest do
  use AutoAeWeb.ConnCase

  import AutoAe.BotsFixtures

  @create_attrs %{country: "some country", region: "some region", min_range: 42, max_range: 42, departure_airport_code: "some departure_airport_code", auto_slot: true, auto_terminal: true, auto_hub: true, min_frequency: 42, max_frequency: 42}
  @update_attrs %{country: "some updated country", region: "some updated region", min_range: 43, max_range: 43, departure_airport_code: "some updated departure_airport_code", auto_slot: false, auto_terminal: false, auto_hub: false, min_frequency: 43, max_frequency: 43}
  @invalid_attrs %{country: nil, region: nil, min_range: nil, max_range: nil, departure_airport_code: nil, auto_slot: nil, auto_terminal: nil, auto_hub: nil, min_frequency: nil, max_frequency: nil}

  describe "index" do
    test "lists all configurations", %{conn: conn} do
      conn = get(conn, ~p"/configurations")
      assert html_response(conn, 200) =~ "Listing Configurations"
    end
  end

  describe "new configuration" do
    test "renders form", %{conn: conn} do
      conn = get(conn, ~p"/configurations/new")
      assert html_response(conn, 200) =~ "New Configuration"
    end
  end

  describe "create configuration" do
    test "redirects to show when data is valid", %{conn: conn} do
      conn = post(conn, ~p"/configurations", configuration: @create_attrs)

      assert %{id: id} = redirected_params(conn)
      assert redirected_to(conn) == ~p"/configurations/#{id}"

      conn = get(conn, ~p"/configurations/#{id}")
      assert html_response(conn, 200) =~ "Configuration #{id}"
    end

    test "renders errors when data is invalid", %{conn: conn} do
      conn = post(conn, ~p"/configurations", configuration: @invalid_attrs)
      assert html_response(conn, 200) =~ "New Configuration"
    end
  end

  describe "edit configuration" do
    setup [:create_configuration]

    test "renders form for editing chosen configuration", %{conn: conn, configuration: configuration} do
      conn = get(conn, ~p"/configurations/#{configuration}/edit")
      assert html_response(conn, 200) =~ "Edit Configuration"
    end
  end

  describe "update configuration" do
    setup [:create_configuration]

    test "redirects when data is valid", %{conn: conn, configuration: configuration} do
      conn = put(conn, ~p"/configurations/#{configuration}", configuration: @update_attrs)
      assert redirected_to(conn) == ~p"/configurations/#{configuration}"

      conn = get(conn, ~p"/configurations/#{configuration}")
      assert html_response(conn, 200) =~ "some updated country"
    end

    test "renders errors when data is invalid", %{conn: conn, configuration: configuration} do
      conn = put(conn, ~p"/configurations/#{configuration}", configuration: @invalid_attrs)
      assert html_response(conn, 200) =~ "Edit Configuration"
    end
  end

  describe "delete configuration" do
    setup [:create_configuration]

    test "deletes chosen configuration", %{conn: conn, configuration: configuration} do
      conn = delete(conn, ~p"/configurations/#{configuration}")
      assert redirected_to(conn) == ~p"/configurations"

      assert_error_sent 404, fn ->
        get(conn, ~p"/configurations/#{configuration}")
      end
    end
  end

  defp create_configuration(_) do
    configuration = configuration_fixture()
    %{configuration: configuration}
  end
end
