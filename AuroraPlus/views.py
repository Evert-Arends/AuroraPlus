from django.shortcuts import render_to_response
from bin import cpu, jsondata

CPU = cpu.CPUUsage
JsonAction = jsondata.JsonData


def index(request):
    string_server = JsonAction.all_server_data()
    if not string_server:
        return "No data found"
    count_servers = JsonAction.count_servers()
    if not count_servers:
        return "-"
    return render_to_response('index.html', {'server_all': string_server, 'totalservers': count_servers})


def server_page(request, server_id):
    string_server = JsonAction.all_server_data()
    if not string_server:
        return "No data found"
    data_array = CPU.cpu_chart(server_id)
    if not data_array:
        return "0.00,0.00,0.00"
    chart_colors = CPU.chart_color(server_id)
    print chart_colors[0]
    return render_to_response('server.html', {'server_id': server_id, 'server_all': string_server,
                                              'chart_data': data_array, 'coloring': chart_colors})


def test(request):
    return render_to_response('test.html')

