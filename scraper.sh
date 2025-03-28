#!/bin/bash

# URL de l'API CoinGecko pour Ethereum
url="https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

# Fichier de log
logfile="scraper.log"

# Récupérer la réponse JSON depuis l'API
json_content=$(curl -s "$url")

# Enregistrer la réponse dans le log
echo "$(date) - Réponse API : $json_content" >> "$logfile"

# Vérifier si la réponse JSON est vide ou mal formée
if [ -z "$json_content" ]; then
    echo "$(date) - Erreur : La réponse de l'API est vide ou inaccessible." >> "$logfile"
    exit 1
fi

# Extraire le prix de l'Ethereum en USD
price=$(echo "$json_content" | jq -r '.ethereum.usd')

# Vérifier si le prix est valide (non vide et non null)
if [[ "$price" == "null" || -z "$price" ]]; then
    echo "$(date) - Erreur : Impossible d'extraire le prix ou prix invalide." >> "$logfile"
    exit 1
fi

# Afficher le prix pour que schedule.sh puisse l'utiliser
echo "$price"
