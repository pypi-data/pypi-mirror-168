from solarbot_upload_image.controller.connection import Session
from solarbot_upload_image.model.upload import Upload


class UploadController:

    def __init__(self):
        pass

    @staticmethod
    def insert(upload):
        session = Session()
        session.add(upload)
        session.commit()
        session.close()

    @staticmethod
    def read():
        session = Session()
        result = session.query(Upload).all()
        session.close()

        return result

    @staticmethod
    def read_by_id(cd_upload):
        session = Session()
        result = session.query(Upload).filter(Upload.cd_upload == cd_upload).first()
        session.close()

        return result

    @staticmethod
    def read_by_type(cd_type):
        session = Session()
        result = session.query(Upload).filter(Upload.cd_tipo == cd_type).first()
        session.close()

        return result

    @staticmethod
    def read_by_send(flag):
        session = Session()
        result = session.query(Upload).filter(Upload.flag_enviado == flag).first()
        session.close()

        return result

    @staticmethod
    def update(update_upload):

        session = Session()
        upload = session.query(Upload).filter(Upload.cd_upload == update_upload.cd_upload).first()

        if upload is not None:
            upload.flag_enviado = update_upload.flag_enviado
            session.commit()
            session.refresh(upload)

        session.close()

    def delete(self, delete_upload):
        session = Session()
        upload = self.read_by_id(delete_upload.cd_upload)
        if upload is not None:
            session.delet(upload)
            session.commit()
        session.close()
