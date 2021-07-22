from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from app.Modbus_TCP import modbus_tcp


def tab(request):
    table = modbus_tcp()

    return render(request, "frontend.html", {
        "table": table
    })
