#!/bin/bash

MOALMANAC_DIR=$1
MOALMANAC_VENV=$2
INPUT_SOMATIC=$3
INPUT_COPY_NUMBER=$4
INPUT_FUSION=$5
WD=$PWD

cp annotate-variants.py annotate-copy-numbers.py annotate-fusions.py "$MOALMANAC_DIR"
cp "$INPUT_SOMATIC" "$MOALMANAC_DIR"/matchmaking-somatic-variants.txt
cp "$INPUT_COPY_NUMBER" "$MOALMANAC_DIR"/matchmaking-copy-number-alterations.txt
cp "$INPUT_FUSION" "$MOALMANAC_DIR"/matchmaking-fusions.txt
cd "$MOALMANAC_DIR" || exit

$MOALMANAC_VENV annotate-variants.py --input matchmaking-somatic-variants.txt --output samples.variants.annotated.txt --directory "$WD"
$MOALMANAC_VENV annotate-copy-numbers.py --input matchmaking-copy-number-alterations.txt --output samples.copy-number.annotated.txt --directory "$WD" --directory "$WD"
$MOALMANAC_VENV annotate-fusions.py --input matchmaking-fusions.txt --output samples.fusions.annotated.txt --directory "$WD" --directory "$WD"

rm annotate-variants.py annotate-copy-numbers.py annotate-fusions.py
