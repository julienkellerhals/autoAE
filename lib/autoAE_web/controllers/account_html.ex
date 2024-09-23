defmodule AutoAEWeb.AccountHTML do
  use AutoAEWeb, :html

  embed_templates "account_html/*"

  @doc """
  Renders a account form.
  """
  attr :changeset, Ecto.Changeset, required: true
  attr :action, :string, required: true

  def account_form(assigns)
end
