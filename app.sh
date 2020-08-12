#!/bin/bash
export $(cat /proc/1/environ |tr '\0' '\n' | xargs)
uwsgi --http :5000 --ini uwsgi.ini