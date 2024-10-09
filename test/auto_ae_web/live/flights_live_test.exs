defmodule AutoAeWeb.FlightsLiveTest do
  use AutoAeWeb.ConnCase

  import Phoenix.LiveViewTest
  import AutoAe.ConfigurationsFixtures

  @create_attrs %{airport: "some airport", flight_url: "some flight_url", flight_created: true, slots: 42, gates_available: true, freq_f: 120.5, freq_request_f: 42, freq_c: 120.5, freq_request_c: 42, freq_y: 120.5, freq_request_y: 42, avg_freq: 120.5, flight_criteria: true}
  @update_attrs %{airport: "some updated airport", flight_url: "some updated flight_url", flight_created: false, slots: 43, gates_available: false, freq_f: 456.7, freq_request_f: 43, freq_c: 456.7, freq_request_c: 43, freq_y: 456.7, freq_request_y: 43, avg_freq: 456.7, flight_criteria: false}
  @invalid_attrs %{airport: nil, flight_url: nil, flight_created: false, slots: nil, gates_available: false, freq_f: nil, freq_request_f: nil, freq_c: nil, freq_request_c: nil, freq_y: nil, freq_request_y: nil, avg_freq: nil, flight_criteria: false}

  defp create_flights(_) do
    flights = flights_fixture()
    %{flights: flights}
  end

  describe "Index" do
    setup [:create_flights]

    test "lists all flights", %{conn: conn, flights: flights} do
      {:ok, _index_live, html} = live(conn, ~p"/flights")

      assert html =~ "Listing Flights"
      assert html =~ flights.airport
    end

    test "saves new flights", %{conn: conn} do
      {:ok, index_live, _html} = live(conn, ~p"/flights")

      assert index_live |> element("a", "New Flights") |> render_click() =~
               "New Flights"

      assert_patch(index_live, ~p"/flights/new")

      assert index_live
             |> form("#flights-form", flights: @invalid_attrs)
             |> render_change() =~ "can&#39;t be blank"

      assert index_live
             |> form("#flights-form", flights: @create_attrs)
             |> render_submit()

      assert_patch(index_live, ~p"/flights")

      html = render(index_live)
      assert html =~ "Flights created successfully"
      assert html =~ "some airport"
    end

    test "updates flights in listing", %{conn: conn, flights: flights} do
      {:ok, index_live, _html} = live(conn, ~p"/flights")

      assert index_live |> element("#flights-#{flights.id} a", "Edit") |> render_click() =~
               "Edit Flights"

      assert_patch(index_live, ~p"/flights/#{flights}/edit")

      assert index_live
             |> form("#flights-form", flights: @invalid_attrs)
             |> render_change() =~ "can&#39;t be blank"

      assert index_live
             |> form("#flights-form", flights: @update_attrs)
             |> render_submit()

      assert_patch(index_live, ~p"/flights")

      html = render(index_live)
      assert html =~ "Flights updated successfully"
      assert html =~ "some updated airport"
    end

    test "deletes flights in listing", %{conn: conn, flights: flights} do
      {:ok, index_live, _html} = live(conn, ~p"/flights")

      assert index_live |> element("#flights-#{flights.id} a", "Delete") |> render_click()
      refute has_element?(index_live, "#flights-#{flights.id}")
    end
  end

  describe "Show" do
    setup [:create_flights]

    test "displays flights", %{conn: conn, flights: flights} do
      {:ok, _show_live, html} = live(conn, ~p"/flights/#{flights}")

      assert html =~ "Show Flights"
      assert html =~ flights.airport
    end

    test "updates flights within modal", %{conn: conn, flights: flights} do
      {:ok, show_live, _html} = live(conn, ~p"/flights/#{flights}")

      assert show_live |> element("a", "Edit") |> render_click() =~
               "Edit Flights"

      assert_patch(show_live, ~p"/flights/#{flights}/show/edit")

      assert show_live
             |> form("#flights-form", flights: @invalid_attrs)
             |> render_change() =~ "can&#39;t be blank"

      assert show_live
             |> form("#flights-form", flights: @update_attrs)
             |> render_submit()

      assert_patch(show_live, ~p"/flights/#{flights}")

      html = render(show_live)
      assert html =~ "Flights updated successfully"
      assert html =~ "some updated airport"
    end
  end
end
