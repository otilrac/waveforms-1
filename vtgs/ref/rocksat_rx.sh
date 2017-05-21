#!/bin/bash
DATETIME=`date -u +%Y%m%d_%H%M%S.%N_UTC`
IQ_FILENAME="./record/rocksat_iq_"$DATETIME"_500k.dat"
RFO_FILENAME="./record/rocksat_rfo_"$DATETIME"_0s1.meta"
SNR_FILENAME="./record/rocksat_snr_"$DATETIME"_0s1.meta"

echo "                   Raw IQ FILENAME:" $IQ_FILENAME
echo "Received Frequency Offset FILENAME:" $RFO_FILENAME
echo "    Signal To Noise Ratio FILENAME:" $SNR_FILENAME

echo "Starting Flowgraph..."
./rocksat_rx_5.py --iq-file=$IQ_FILENAME --rfo-file=$RFO_FILENAME --snr-file=$SNR_FILENAME --record-iq=1 --record-rfo=1 --record-snr=1
