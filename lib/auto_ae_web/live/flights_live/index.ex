defmodule AutoAeWeb.FlightsLive.Index do
  use AutoAeWeb, :live_view

  alias AutoAe.Configurations
  alias AutoAe.Configurations.Flights

  @impl true
  def mount(_params, _session, socket) do
    {:ok, stream(socket, :flights_collection, Configurations.list_flights())}
  end

  @impl true
  def handle_params(params, _url, socket) do
    {:noreply, apply_action(socket, socket.assigns.live_action, params)}
  end

  defp apply_action(socket, :edit, %{"id" => id}) do
    socket
    |> assign(:page_title, "Edit Flights")
    |> assign(:flights, Configurations.get_flights!(id))
  end

  defp apply_action(socket, :new, _params) do
    socket
    |> assign(:page_title, "New Flights")
    |> assign(:flights, %Flights{})
  end

  defp apply_action(socket, :index, _params) do
    socket
    |> assign(:page_title, "Listing Flights")
    |> assign(:flights, nil)
  end

  @impl true
  def handle_info({AutoAeWeb.FlightsLive.FormComponent, {:saved, flights}}, socket) do
    {:noreply, stream_insert(socket, :flights_collection, flights)}
  end

  @impl true
  def handle_event("delete", %{"id" => id}, socket) do
    flights = Configurations.get_flights!(id)
    {:ok, _} = Configurations.delete_flights(flights)

    {:noreply, stream_delete(socket, :flights_collection, flights)}
  end
end
