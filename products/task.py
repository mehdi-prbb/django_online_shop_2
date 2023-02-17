from bucket import bucket


# TODO: can be async?
def all_bucket_object_tasks():
    result = bucket.get_objects()
    return result