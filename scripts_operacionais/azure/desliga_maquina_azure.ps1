try{
    $azureAccountName = (get-item env:usuario).Value
    $senha = (get-item env:senha).Value
    $servidor = (get-item env:servidor).Value
    $idMaquina = (get-item env:id_maquina).Value

    $azurePassword = ConvertTo-SecureString $senha -AsPlainText -Force

    $psCred = New-Object System.Management.Automation.PSCredential($azureAccountName, $azurePassword)

    Login-AzureRmAccount -Credential $psCred
    Select-AzureRmSubscription -Subscriptionid $idMaquina

    Stop-AzureRmVM -ResourceGroupName RG-INTEGRACAO -Name $servidor -Force -ErrorAction SilentlyContinue
}
catch
{
    exit 1
}