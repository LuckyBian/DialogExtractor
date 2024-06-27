#!/bin/bash

# 设置模型和语言等固定参数
ASR_MODEL="Faster Whisper (多语种)"
ASR_MODEL_SIZE="large"
ASR_LANG="yue"

# 循环从 2002 到 2024 年
for YEAR in {2006..2024}
do
  echo "Running ASR for year: $YEAR"
  python asr.py \
    --asr_inp_dir "/home/weizhenbian/legco/$YEAR" \
    --asr_opt_dir "/home/weizhenbian/legco/txt/$YEAR" \
    --asr_model "$ASR_MODEL" \
    --asr_model_size "$ASR_MODEL_SIZE" \
    --asr_lang "$ASR_LANG"
done
