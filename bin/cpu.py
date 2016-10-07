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

    @staticmethod
    def chart_color(server_id):
        chart_data = CPUUsage.cpu_chart(server_id)
        print chart_data

        if chart_data <= 50.0:
            fillcolor = "lightgreen"
            strokecolor = "#00D851"
            highlightfill = "#00D851"
            highlightstroke = "lightgreen"
        elif 50.0 < chart_data <= 75.0:
            fillcolor = "#FFA446"
            strokecolor = "orange"
            highlightfill = "orange"
            highlightstroke = "#FFA446"
        elif 75.0 < chart_data <= 100.0:
            fillcolor = "#FF6870"
            strokecolor = "#D85C4D"
            highlightfill = "#D85C4D"
            highlightstroke = "#FF6870"
        else:
            fillcolor = "#FF6870"
            strokecolor = "#D85C4D"
            highlightfill = "#D85C4D"
            highlightstroke = "#FF6870"

        chart_colors = [fillcolor, strokecolor, highlightfill, highlightstroke]
        return chart_colors
