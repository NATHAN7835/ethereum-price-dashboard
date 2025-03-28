#!/bin/bash

while true; do
    echo "🕒 [$(date '+%Y-%m-%d %H:%M:%S')] Lancement d'une requête..." >> /home/ubuntu/eth-project/schedule.log

    price=$(/home/ubuntu/eth-project/scraper.sh)

    if [ -n "$price" ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S'),$price" >> /home/ubuntu/eth-project/prices.csv
        echo "✅ Prix enregistré : $price" >> /home/ubuntu/eth-project/schedule.log
    else
        echo "❌ Aucun prix récupéré." >> /home/ubuntu/eth-project/schedule.log
    fi

    sleep 300
done
