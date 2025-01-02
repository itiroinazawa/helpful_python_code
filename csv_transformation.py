import csv
from flask import Response

def data_to_csv(data):
    output = []
    for item in data:
        output.append(",".join(str(value) for value in item.values()))
    return "\n".join(output)

@app.route("/api/export")
def export_data():
    data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    csv_data = data_to_csv(data)
    return Response(csv_data, mimetype="text/csv")
