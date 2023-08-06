from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Float, Boolean, sql
from sqlalchemy.dialects import mysql

if TYPE_CHECKING:
    from decimal import Decimal


class PrimitiveOfficeMixin(object):
    """
    Mixin providing fields shared by models: RawOffice, ExportableOffice, Office, OfficeAdminAdd.

    Don't forget to create a new migration for each of these models
    each time you add/change/remove a field here to keep all models
    in sync.
    """
    siret = Column(String(191))
    company_name = Column('raisonsociale', String(191), nullable=False)
    office_name = Column('enseigne', String(191), default='', nullable=False, server_default="")
    naf = Column('codenaf', String(8), nullable=False)
    street_number = Column('numerorue', String(191), default='', nullable=False, server_default="")
    street_name = Column('libellerue', String(191), default='', nullable=False, server_default="")
    city_code = Column('codecommune', String(191), nullable=False)
    zipcode = Column('codepostal', String(8), nullable=False)
    email = Column(String(191), default='', nullable=False, server_default="")
    tel = Column(String(191), default='', nullable=False, server_default="")
    departement = Column(String(8), nullable=False)
    headcount = Column('trancheeffectif', String(2))
    website = Column(String(191), default='', nullable=False, server_default="")
    flag_poe_afpr = Column(Boolean, default=False, nullable=False, server_default=sql.expression.false())
    flag_pmsmp = Column(Boolean, default=False, nullable=False, server_default=sql.expression.false())


class OfficeMixin(PrimitiveOfficeMixin):
    """
    Mixin providing fields shared by models: ExportableOffice, Office, OfficeAdminAdd.

    Don't forget to create a new migration for each of these models
    each time you add/change/remove a field here to keep all models
    in sync.
    """
    social_network = Column(mysql.TINYTEXT, nullable=True)

    email_alternance = Column('email_alternance', mysql.TINYTEXT, default='', nullable=True, server_default="")
    phone_alternance = Column('phone_alternance', mysql.TINYTEXT, nullable=True)
    website_alternance = Column('website_alternance', mysql.TINYTEXT, nullable=True)
    contact_mode = Column('contact_mode', mysql.TINYTEXT, nullable=True)

    flag_alternance = Column(Boolean, default=False, nullable=False, server_default=sql.expression.false())
    flag_junior = Column(Boolean, default=False, nullable=False, server_default=sql.expression.false())
    flag_senior = Column(Boolean, default=False, nullable=False, server_default=sql.expression.false())
    flag_handicap = Column(Boolean, default=False, nullable=False, server_default=sql.expression.false())
    score_alternance = Column(Integer, default=0, nullable=False, server_default='0')
    x = Column('coordinates_x', Float)  # Longitude.
    y = Column('coordinates_y', Float)  # Latitude.
    hiring = Column(Integer, default=0, nullable=False, server_default='0')

    @property
    def score(self) -> 'Decimal':
        raise NotImplementedError()

    @property
    def longitude(self) -> 'Decimal':
        return self.x

    @property
    def latitude(self) -> 'Decimal':
        return self.y


class FinalOfficeMixin(OfficeMixin):
    """
    Mixin providing fields shared by models: ExportableOffice, Office.

    Don't forget to create a new migration for each of these models
    each time you add/change/remove a field here to keep all models
    in sync.
    """
    # A flag that is True if the office also recruits beyond the boundaries of its primary geolocation.
    has_multi_geolocations = Column(Boolean, default=False, nullable=False, server_default=sql.expression.false())
