#!/bin/sh

eval "$(conda shell.bash hook)"
conda activate {{ conda_env }}

echo "Changing to working directory: {{ project_dir }}"
cd {{ project_dir }}

echo "Running: {{ pipeline_run_command }}"
#continue on error so that aws instance can be stopped
{{ pipeline_run_command }} || true

echo "Stopping Instance {{ instance_id }}"
rlabs aws instance stop --instance-id {{ instance_id }} --credentials-file {{ credentials_file }}
