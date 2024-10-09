defmodule AutoAeWeb.FlightsLive.Index do
  use AutoAeWeb, :live_view

  alias AutoAe.Configurations
  alias AutoAe.Configurations.Flights

  @impl true
  def mount(%{"configuration_id" => configuration_id}, _session, socket) do
    {:ok,
     socket
     |> stream(:flights_collection, Configurations.list_flights(configuration_id))}
  end

  @impl true
  def handle_params(params, _url, socket) do
    {:noreply, apply_action(socket, socket.assigns.live_action, params)}
  end

  defp apply_action(socket, :edit, %{
         "id" => id,
         "account_id" => account_id,
         "configuration_id" => configuration_id
       }) do
    socket
    |> assign(:page_title, "Edit Flights")
    |> assign(:flights, Configurations.get_flights!(id))
    |> assign(:account_id, account_id)
    |> assign(:configuration_id, configuration_id)
  end

  defp apply_action(socket, :new, %{
         "account_id" => account_id,
         "configuration_id" => configuration_id
       }) do
    socket
    |> assign(:page_title, "New Flights")
    |> assign(:flights, %Flights{})
    |> assign(:account_id, account_id)
    |> assign(:configuration_id, configuration_id)
  end

  defp apply_action(socket, :index, %{
         "account_id" => account_id,
         "configuration_id" => configuration_id
       }) do
    socket
    |> assign(:page_title, "Listing Flights")
    |> assign(:flights, nil)
    |> assign(:account_id, account_id)
    |> assign(:configuration_id, configuration_id)
  end

  @impl true
  def handle_info({AutoAeWeb.FlightsLive.FormComponent, {:saved, flights}}, socket) do
    {:noreply, stream_insert(socket, :flights_collection, flights)}
  end

  @impl true
  def handle_info({:update, flight}, socket) do
    {:noreply, stream_insert(socket, :flights_collection, flight)}
  end

  @impl true
  def handle_event(
        "run",
        %{"account_id" => account_id, "configuration_id" => configuration_id},
        socket
      ) do
    Task.async(fn -> run_configuration(account_id, configuration_id) end)

    {:noreply,
     socket
     |> put_flash(:info, "Running flight creation. Refreshing page stops script.")
     |> push_patch(to: ~p"/accounts/#{account_id}/configurations/#{configuration_id}/flights/")}
  end

  @impl true
  def handle_event("delete", %{"id" => id}, socket) do
    flights = Configurations.get_flights!(id)
    {:ok, _} = Configurations.delete_flights(flights)

    {:noreply, stream_delete(socket, :flights_collection, flights)}
  end

  defp run_configuration(_account_id, configuration_id) do
    flights = Configurations.list_available_flights(configuration_id)

    for flight <- flights do
      payload = %{
        flight_id: flight.id
      }

      {status, response} =
        ExAws.Lambda.invoke(
          "AutoAeScriptsStack-runConfiguration96A0EB2F-7r0fHL1rmB1C",
          payload,
          %{}
        )
        |> ExAws.request(region: System.get_env("AWS_REGION"))

      IO.inspect(status)
      IO.inspect(response)

      # send(self(), {:update, Configurations.get_flights!(flight.id)})
    end

    # {:noreply,
    #  socket
    #  |> put_flash(:info, "Flights updated successfully")
    #  |> push_patch(to: ~p"/accounts/#{account_id}/configurations/#{configuration_id}/flights/")}
  end
end
