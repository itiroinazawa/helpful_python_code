FEATURE_FLAGS = {"new_feature": True}

def is_feature_enabled(feature_name):
    return FEATURE_FLAGS.get(feature_name, False)

# Example Usage
print(is_feature_enabled("new_feature"))
