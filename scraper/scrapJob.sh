#!/bin/bash

#storesId=(marabraz-lojas-fisicas marabraz-loja-online openbox2 lojas-lebes-lojas-fisicas lider-interiores viggore-moveis fabrispuma lojas-guido)
storesId=(marabraz-loja-online marabraz-lojas-fisicas)

for u in "${storesId[@]}"
do
    echo "SCRAPING $u NOW..."

    for i in $(seq "$1" 20 "$2")
    do
        # shellcheck disable=SC2004
        endPage=$(( $i + 20 ))
        python main.py --store_name="$u" --page_start="$i" --page_end="$endPage" scrapeReclameAqui
        sleep 2m
    done

done
