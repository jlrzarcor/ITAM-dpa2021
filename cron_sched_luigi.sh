#!/bin/bash

cd ~/rep-proj-dpa
pyenv activate itam_dpa
export PYTHONPATH=$PWD
PYTHONPATH="." luigi --module 'src.etl.task_almacenamiento' TaskStore --local-scheduler --bucket 
echo $PYTHONPATH > testcron_path.txt 
pip freeze > testcron_pipfreeze.txt
