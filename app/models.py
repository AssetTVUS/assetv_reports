from app import db


class Video(db.Model):
    __tablename__ = "Video"
    V_ID = db.Column(db.Integer, primary_key=True)
    V_Title = db.Column(db.String(200))
    V_DateFilmed = db.Column(db.DateTime)
    V_DatePublished = db.Column(db.DateTime)
    V_Duration = db.Column(db.Float)
    V_VideoLink = db.Column(db.String(500))
    V_Type = db.Column(db.String(1))
    V_ImageURL = db.Column(db.String(500))
    #videos = db.relationship("TagList", backref="video")

    def __repr__(self):
        return '<Video (%r) - %r>' % (self.V_ID,self.V_Title.encode('utf-8'))

class Tag(db.Model):
    T_ID = db.Column(db.Integer, primary_key=True)
    T_TAG = db.Column(db.String(200))
    T_Type = db.Column(db.String(50))

    def __repr__(self):
        return '<Tag (%r) - %r>' % (self.T_ID,self.T_Tag)

class Company(db.Model):
    CID = db.Column(db.Integer, primary_key=True)
    CName = db.Column(db.String(100))
    CReportSinceMonth = db.Column(db.Integer)         #TODO
    CReportSinceYear  = db.Column(db.Integer)             #TODO
    CType = db.Column(db.Integer)                     #TODO

    def __repr__(self):
        return '<Company (%r) - %r>' % (self.CID, self.CName)

class Company_List(db.Model):
    __tablename__ = "VW_COMPANY_LIST"
    CID = db.Column(db.Integer, primary_key=True)
    CName = db.Column(db.String(100))
    month_name = db.Column(db.Integer)         #TODO
    CReportSinceYear  = db.Column(db.Integer)             #TODO
    company_type = db.Column(db.Integer)                     #TODO

    def __repr__(self):
        return '<Company (%r) - %r>' % (self.CID, self.CName)


'''
class TagList(db.Model):
    TL_ID = db.Column(db.Integer, primary_key=True)
    TL_VID =  db.Column(db.Integer,db.ForeignKey('Video.V_ID'))
    TL_TID = db.Column(db.Integer,db.ForeignKey('Tag.T_ID'))
    tags = db.relationship("TagList", backref="tag")

    def __repr__(self):
        return '<TagList Video Id:(%r) - Tag Id:(%r)>' % (self.TL_VID,self.TL_TID)
'''