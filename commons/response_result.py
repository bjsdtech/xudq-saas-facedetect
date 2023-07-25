def respones_result(code, msg, result=""):
    return {


        "code": code,
        "msg": msg,
        "result": result
    }


def face_detech_return(trans_id, code, status, msg, response_id='', face_number=0, face_locations=None):
    if face_locations is None:
        face_locations = []

    return {
        "code": code,
        "msg": msg,
        "result": {
            "faceNumber": face_number,
            "faceLocations": face_locations,
            "requestId": trans_id,
            "responseId": response_id,
            "status": status
        }
    }
