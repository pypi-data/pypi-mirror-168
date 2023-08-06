from starlette import datastructures


class RequestFile(bytes):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, datastructures.UploadFile):
            raise TypeError("Starlette data structures UploadFile required")
        return v

    def __repr__(self):
        return f"FilesType({super().__repr__()})"
