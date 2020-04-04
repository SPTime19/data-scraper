
# Set-ExecutionPolicy Unrestricted
param([Int32]$pageStart=1, [Int32]$pageMax=4, [Int32]$step=2)

# IF NECESSARY for non initialized prompts...
#$env:Path += ";C:\Users\...\miniconda3\Scripts"
#conda init powershell
#activate base

$storesIds = @("fast-shop", "marabraz-loja-online")

foreach ($store in $storesIds) {
	For ($i=$pageStart; $i -le $pageMax; $i = $i + $step) {
		python main.py --store_name=$store --page_start=$i --page_end=$pageMax scrapeReclameAqui
		Start-Sleep -s 120
	}
}
