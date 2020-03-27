#!/bin/bash

storesId=(tokestok-loja-online tokestok madeiramadeira mobly etna-home-store-loja-online etna-home-store casas-bahia-loja-online casas-bahia-lojas-fisicas)
for u in "${storesId[@]}"
do
    echo "SCRAPING $u NOW..."
    python main.py --store_name="$u" --page_start=1 --page_end=5 scrapeReclameAqui
done
