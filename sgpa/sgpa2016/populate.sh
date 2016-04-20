#!/bin/bash

nombreTag=$2

git checkout $nombreTag

if [ "$1" -eq "1" ]; then
	python ../manage.py runserver
	deactivate

fi
