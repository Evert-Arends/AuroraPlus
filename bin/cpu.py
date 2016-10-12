from bin import jsondata
JsonAction = jsondata.JsonData


class CPUUsage:

    def __init__(self):
        return

    @staticmethod
    def get_usage(server_id):
        server_id = int(server_id)
        data = JsonAction.get_json_data()
        cpu_usage = (data["ServerList"]["Servers"][server_id]["ServerData"]["Cpu"])

        if not cpu_usage:
            return
        else:
            return cpu_usage

    @staticmethod
    def cpu_chart(server_id):
        chart_data = CPUUsage.get_usage(server_id)

        escaped = chart_data.replace(",", ".")
        final = escaped.split(',')

        item1 = float(final[0]) * 100
        data_array = item1

        return data_array
