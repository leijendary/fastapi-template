#!/bin/sh
aerich upgrade
gunicorn main:app