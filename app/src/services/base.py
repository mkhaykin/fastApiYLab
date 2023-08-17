from fastapi import HTTPException


class BaseService:
    @staticmethod
    def get_one(result, error_message=''):
        if len(result) == 0:
            raise HTTPException(404, error_message)
        elif len(result) > 1:
            # TODO write to log, more than one result
            raise HTTPException(500, error_message)
        return result[0]
