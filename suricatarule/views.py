# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import subprocess
from urllib.parse import unquote, urlparse
import json

def validate_rule(request):
    decoded_error=''
    decoded_output=''
    url_param = request.get_full_path().split('?')[1]
    content = unquote(url_param).replace('check_rule=', '')
    print(content)
    with open('/etc/suricata/rules/test.rules', 'w') as f:
        f.write(content)
    # Define the command to execute
    command = "/usr/bin/suricata -c /etc/suricata/suricata.yaml -T | egrep '<Error>'"

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    decoded_output = output.decode('utf-8')
    decoded_error = error.decode('utf-8')
    #print((decoded_error.split('\n')[0]).split('-')[5])
    error_msg = "Rule is OK"
    if decoded_error != '':
        error_msg="Issue in the rule. " + (decoded_error.split('\n')[0]).split('-')[5]
    return HttpResponse(json.dumps({"error": error_msg}))
