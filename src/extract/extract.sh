!/bin/bash

# Ativar o ambiente virtual
source /home/bigdata/IGTI/pos_engenharia_dados/projeto_aplicado/.venv/bin/activate

# Remove todos os arquivos antes de realizar a carga.
rm /home/bigdata/IGTI/pos_engenharia_dados/projeto_aplicado/data/*

#scrapy crawl amazon_smartphone_apple -o ../../data/amazon_smartphone_apple.json  ;
#scrapy crawl amazon_smartphone_samsung -o ../../data/amazon_smartphone_samsung.json ;
#scrapy crawl casasbahia_smartphone_apple -o ../../data/casasbahia_smartphone_apple.json ;
#scrapy crawl casasbahia_smartphone_samsung -o ../../data/casasbahia_smartphone_samsung.json ;
scrapy crawl magazineluiza_smartphone_apple -o ../../data/magazineluiza_smartphone_apple.json ;
scrapy crawl magazineluiza_smartphone_samsung -o ../../data/magazineluiza_smartphone_samsung.json ;
scrapy crawl mercado_livre_smartphone_apple -o ../../data/mercadolivre_smartphone_apple.json ;
scrapy crawl mercado_livre_smartphone_samsung -o ../../data/mercadolivre_smartphone_samsung.json

deactivate