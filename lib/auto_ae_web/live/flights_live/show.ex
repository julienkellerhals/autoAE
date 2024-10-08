defmodule AutoAeWeb.FlightsLive.Show do
  use AutoAeWeb, :live_view

  alias AutoAe.Configurations

  @impl true
  def mount(_params, _session, socket) do
    {:ok, socket}
  end

  @impl true
  def handle_params(
        %{"id" => id, "account_id" => account_id, "configuration_id" => configuration_id},
        _,
        socket
      ) do
    {:noreply,
     socket
     |> assign(:page_title, page_title(socket.assigns.live_action))
     |> assign(:flights, Configurations.get_flights!(id))
     |> assign(:account_id, account_id)
     |> assign(:configuration_id, configuration_id)}
  end

  defp page_title(:show), do: "Show Flights"
  defp page_title(:edit), do: "Edit Flights"
end
