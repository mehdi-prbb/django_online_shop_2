from bucket import bucket


def all_bucket_object_tasks():
    result = bucket.get_objects()
    return result