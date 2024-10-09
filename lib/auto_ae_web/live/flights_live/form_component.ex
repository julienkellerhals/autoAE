defmodule AutoAeWeb.FlightsLive.FormComponent do
  use AutoAeWeb, :live_component

  alias AutoAe.Configurations

  @impl true
  def render(assigns) do
    ~H"""
    <div>
      <.header>
        <%= @title %>
        <:subtitle>Use this form to manage flights records in your database.</:subtitle>
      </.header>

      <.simple_form
        for={@form}
        id="flights-form"
        phx-target={@myself}
        phx-change="validate"
        phx-submit="save"
      >
        <.input field={@form[:airport]} type="text" label="Airport" />
        <.input field={@form[:flight_url]} type="text" label="Flight url" />
        <.input field={@form[:flight_created]} type="checkbox" label="Flight created" />
        <.input field={@form[:slots]} type="number" label="Slots" />
        <.input field={@form[:gates_available]} type="checkbox" label="Gates available" />
        <.input field={@form[:freq_f]} type="number" label="Freq f" step="any" />
        <.input field={@form[:flight_demand_f]} type="number" label="Flight demand f" />
        <.input field={@form[:freq_c]} type="number" label="Freq c" step="any" />
        <.input field={@form[:flight_demand_c]} type="number" label="Flight demand c" />
        <.input field={@form[:freq_y]} type="number" label="Freq y" step="any" />
        <.input field={@form[:flight_demand_y]} type="number" label="Flight demand y" />
        <.input field={@form[:avg_freq]} type="number" label="Avg freq" step="any" />
        <.input field={@form[:configuration_criteria]} type="checkbox" label="Flight criteria" />
        <:actions>
          <.button phx-disable-with="Saving...">Save Flights</.button>
        </:actions>
      </.simple_form>
    </div>
    """
  end

  @impl true
  def update(%{flights: flights} = assigns, socket) do
    {:ok,
     socket
     |> assign(assigns)
     |> assign_new(:form, fn ->
       to_form(Configurations.change_flights(flights))
     end)}
  end

  @impl true
  def handle_event("validate", %{"flights" => flights_params}, socket) do
    changeset = Configurations.change_flights(socket.assigns.flights, flights_params)
    {:noreply, assign(socket, form: to_form(changeset, action: :validate))}
  end

  def handle_event("save", %{"flights" => flights_params}, socket) do
    save_flights(socket, socket.assigns.action, flights_params)
  end

  defp save_flights(socket, :edit, flights_params) do
    case Configurations.update_flights(socket.assigns.flights, flights_params) do
      {:ok, flights} ->
        notify_parent({:saved, flights})

        {:noreply,
         socket
         |> put_flash(:info, "Flights updated successfully")
         |> push_patch(to: socket.assigns.patch)}

      {:error, %Ecto.Changeset{} = changeset} ->
        {:noreply, assign(socket, form: to_form(changeset))}
    end
  end

  defp save_flights(socket, :new, flights_params) do
    case Configurations.create_flights(flights_params) do
      {:ok, flights} ->
        notify_parent({:saved, flights})

        {:noreply,
         socket
         |> put_flash(:info, "Flights created successfully")
         |> push_patch(to: socket.assigns.patch)}

      {:error, %Ecto.Changeset{} = changeset} ->
        {:noreply, assign(socket, form: to_form(changeset))}
    end
  end

  defp notify_parent(msg), do: send(self(), {__MODULE__, msg})
end
