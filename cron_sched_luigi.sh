#!/bin/bash

eval "$(pyenv init -)"

pyenv activate itam_dpa

cd ~/dpa-proj
export PGSERVICEFILE=${HOME}/.pg_service.conf
export PGSERVICE=jl_cfi
export PYTHONPATH=$PWD

PYTHONPATH="." luigi --module 'src.etl.task_almacenamiento' TaskStore --local-scheduler

echo $PYTHONPATH > time_test.txt 
pip freeze > crontest_pipfreeze.txt
