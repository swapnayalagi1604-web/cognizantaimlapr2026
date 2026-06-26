resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'teststorage${uniqueString(resourceGroup().id)}'
  location: resourceGroup().location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}
