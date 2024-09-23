defmodule AutoAEWeb.AircraftHTML do
  use AutoAEWeb, :html

  embed_templates "aircraft_html/*"

  @doc """
  Renders a aircraft form.
  """
  attr :changeset, Ecto.Changeset, required: true
  attr :action, :string, required: true

  def aircraft_form(assigns)
end
