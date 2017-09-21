#! /bin/bash
set -e
set -x

if [ ! -d data/ ]; then echo 'Error: data/ not found.'; exit 1; fi;

if [ ! -d data/cleaned_data/ ]; then mkdir -p data/cleaned_data/; fi;
if [ ! -d data/code_tables/ ]; then mkdir -p data/code_tables/; fi;

if [ ! -f "data/atusact_0315.zip" ]; then
    curl https://www.bls.gov/tus/special.requests/atusact_0315.zip > data/atusact_0315.zip
fi
if [ ! -f "data/atusrost_0315.zip" ]; then
    curl https://www.bls.gov/tus/special.requests/atusrost_0315.zip > data/atusrost_0315.zip
fi
if [ ! -f "data/atussum_0315.zip" ]; then
    curl https://www.bls.gov/tus/special.requests/atussum_0315.zip > data/atussum_0315.zip
fi
if [ ! -f "data/atuscps_0315.zip" ]; then
    curl https://www.bls.gov/tus/special.requests/atuscps_0315.zip > data/atuscps_0315.zip
fi
if [ ! -f "data/atuswho_0315.zip" ]; then
    curl https://www.bls.gov/tus/special.requests/atuswho_0315.zip > data/atuswho_0315.zip
fi
if [ ! -f "data/atusresp_0315.zip" ]; then
    curl https://www.bls.gov/tus/special.requests/atusresp_0315.zip > data/atusresp_0315.zip
fi

if [ ! -d "data/atusact_0315/" ]; then
    unzip data/atusact_0315.zip -d data/atusact_0315/
    mv data/atusact_0315/atusact_0315.dat data/atusact_0315/atusact_0315.csv
fi
if [ ! -d "data/atusrost_0315/" ]; then
    unzip data/atusrost_0315.zip -d data/atusrost_0315/
    mv data/atusrost_0315/atusrost_0315.dat data/atusrost_0315/atusrost_0315.csv
fi
if [ ! -d "data/atussum_0315/" ]; then
    unzip data/atussum_0315.zip -d data/atussum_0315/
    mv data/atussum_0315/atussum_0315.dat data/atussum_0315/atussum_0315.csv
fi
if [ ! -d "data/atuscps_0315/" ]; then
    unzip data/atuscps_0315.zip -d data/atuscps_0315/
    mv data/atuscps_0315/atuscps_0315.dat data/atuscps_0315/atuscps_0315.csv
fi
if [ ! -d "data/atuswho_0315/" ]; then
    unzip data/atuswho_0315.zip -d data/atuswho_0315/
    mv data/atuswho_0315/atuswho_0315.dat data/atuswho_0315/atuswho_0315.csv
fi
if [ ! -d "data/atusresp_0315/" ]; then
    unzip data/atusresp_0315.zip -d data/atusresp_0315/
    mv data/atusresp_0315/atusresp_0315.dat data/atusresp_0315/atusresp_0315.csv
fi
