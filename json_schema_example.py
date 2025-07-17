from jsonschema import validate


schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"}
    },
    "required": ["name"]
}


data = {
    "name": "Alice",
    "age": 30
}

validate(instance=data, schema=schema)