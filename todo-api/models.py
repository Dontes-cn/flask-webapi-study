# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Batch11(db.Model):
    __tablename__ = 'batch11'

    posid = db.Column(db.Integer, primary_key=True, info='序号')
    province = db.Column(db.String(32), info='省')
    city = db.Column(db.String(32), info='市')
    county = db.Column(db.String(32), info='县')
    positon = db.Column(db.String(45), info='地址')
    contact = db.Column(db.String(16), info='联系人')
    phone = db.Column(db.String(32), info='电话')
    bank = db.Column(db.String(45))
    ppbcid = db.Column(db.String(18), info='人民银行代码')
    orgid = db.Column(db.String(18), info='征信机构代码')
    nedpos = db.Column(db.String(18), info='需发货数量')
    posd = db.Column(db.Integer, info='已发货数量')
    nopos = db.Column(db.String(18), info='不发货数量')
    reason = db.Column(db.String(45), info='不发货原因')
    lng = db.Column(db.String(45), info='经度')
    lat = db.Column(db.String(45), info='纬度')
    contract = db.Column(db.String(200), info='合同名称')
    address = db.Column(db.String(200), info='合同源地址')
    contractnum = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue(), info='合同编号')
