estimate_request_set = {'orig', 'plat', 'dir'}

def is_valid_estimate_req(req_dict):
    invalid_key_set = set()
    for key in req_dict:
        if key not in estimate_request_set:
            invalid_key_set.add(key)

        return invalid_key_set
