from sqlalchemy import Column, Integer, String, Boolean
from solarbot_upload_image.controller.connection import Base


class Upload(Base):
    __tablename__ = "tb_upload"
    cd_upload = Column("cd_upload", Integer, primary_key=True, autoincrement=True)
    cd_tipo = Column("cd_tipo", Integer)
    cd_missao = Column("cd_missao", Integer)
    output = Column("output", String)
    flag_enviado = Column("flag_enviado", Boolean)
    vl_rgb = Column("vl_rgb", String)
    vl_depth = Column("vl_depth", String)

    def __init__(self, cd_tipo, cd_missao, output, flag_enviado, vl_rgb, vl_depth):
        self.cd_tipo = cd_tipo
        self.cd_missao = cd_missao
        self.output = output
        self.flag_enviado = flag_enviado
        self.vl_rgb = vl_rgb
        self.vl_depth = vl_depth
