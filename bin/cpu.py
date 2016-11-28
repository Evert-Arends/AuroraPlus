from bin import jsondata

JsonAction = jsondata.JsonData


class CPUUsage:
    def __init__(self):
        return

    @staticmethod
    def get_usage(server_id):
        server_id = int(server_id)
        data = JsonAction.get_json_data()
        cpu_usage = (data["Server"]["ServerDetails"]["CPU_Usage"])
        if not cpu_usage:
            return
        else:
            return cpu_usage

    @staticmethod
    def cpu_chart(server_id):
        chart_data = CPUUsage.get_usage(server_id)
        chart_data = [12.3, 13.4, 15.2]

        return chart_data
