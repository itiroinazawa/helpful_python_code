def aggregate_data(data):
    return {"sum": sum(data), "average": sum(data) / len(data)}

# Example Usage
print(aggregate_data([1, 2, 3, 4]))
