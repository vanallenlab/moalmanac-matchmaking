#!/bin/bash

MOALMANAC_DIR=$1
MOALMANAC_VENV=$2
INPUT_SOMATIC=$3
INPUT_COPY_NUMBER=$4
INPUT_FUSION=$5
OUTPUT_SOMATIC=${6-samples.variants.annotated.txt}
OUTPUT_COPY_NUMBER=${7-samples.copy_numbers.annotated.txt}
OUTPUT_FUSION=${8-samples.fusions.annotated.txt}
WD=$PWD

cp annotate-variants.py annotate-copy-numbers.py annotate-fusions.py "$MOALMANAC_DIR"
cp "$INPUT_SOMATIC" "$MOALMANAC_DIR"/matchmaking-somatic-variants.txt
cp "$INPUT_COPY_NUMBER" "$MOALMANAC_DIR"/matchmaking-copy-number-alterations.txt
cp "$INPUT_FUSION" "$MOALMANAC_DIR"/matchmaking-fusions.txt
cd "$MOALMANAC_DIR" || exit

$MOALMANAC_VENV annotate-variants.py --input matchmaking-somatic-variants.txt --output "$OUTPUT_SOMATIC" --directory "$WD"
$MOALMANAC_VENV annotate-copy-numbers.py --input matchmaking-copy-number-alterations.txt --output "$OUTPUT_COPY_NUMBER" --directory "$WD"
$MOALMANAC_VENV annotate-fusions.py --input matchmaking-fusions.txt --output "$OUTPUT_FUSION" --directory "$WD"

rm "$MOALMANAC_DIR"/annotate-variants.py "$MOALMANAC_DIR"/annotate-copy-numbers.py "$MOALMANAC_DIR"/annotate-fusions.py
rm "$MOALMANAC_DIR"/matchmaking-somatic-variants.txt "$MOALMANAC_DIR"/matchmaking-copy-number-alterations.txt "$MOALMANAC_DIR"/matchmaking-fusions.txt
