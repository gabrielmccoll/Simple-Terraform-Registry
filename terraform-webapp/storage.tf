resource "azurerm_storage_account" "tfreg-wa-sa" {
  name                     = "${var.name}sa"
  resource_group_name      = azurerm_resource_group.tfreg-wa-rg.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  allow_blob_public_access = false
  tags                     = var.tags
}

resource "azurerm_storage_container" "tfreg-wa-sac" {
  storage_account_name = azurerm_storage_account.tfreg-wa-sa.name
  name                 = var.name

}

resource "azurerm_role_assignment" "funccode_sa_ev" { #giving permissions to the webapp to read the contents of the storage account
  scope                = azurerm_storage_account.tfreg-wa-sa.id
  role_definition_name = "Storage Blob Data Reader"
  principal_id         = azurerm_app_service.tfreg-wa-as.identity[0].principal_id
}



