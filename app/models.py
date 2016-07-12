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

class YTD_Results(db.Model):
    __tablename__ = "VW_YTD_Results_Detailed"
    CID = db.Column(db.Integer, primary_key=True)
    V_ID = db.Column(db.Integer, primary_key=True)
    V_Title = db.Column(db.String(200))
    V_DatePublished = db.Column(db.String(20))
    V_Duration = db.Column(db.Float)
    View_Stats =  db.Column(db.Integer)
    View_Completes = db.Column(db.Integer)
    Average_Completion_Rate = db.Column(db.Float)
    Average_Time = db.Column(db.Float)
    Total_Time = db.Column(db.Float)
    Bloomberg_Terminal_Views = db.Column(db.Integer)

class Single_Report_View(db.Model):
    __tablename__ = "VW_SINGLE_REPORT"
    month_id =  db.Column(db.Integer)
    V_ID  =  db.Column(db.Integer)
    SPeriod = db.Column(db.String(20))
    SYear = db.Column(db.Integer)
    V_Title = db.Column(db.String(200))
    V_ImageURL = db.Column(db.String(500))
    V_VideoLink = db.Column(db.String(500))
    V_DatePublished = db.Column(db.DateTime)
    VType  = db.Column(db.String(20))
    total_views = db.Column(db.Integer)
    Wirehouse_Advisors = db.Column(db.Float)
    Independent_BD = db.Column(db.Float)
    RIA  = db.Column(db.Float)
    Investment_Consultant =  db.Column(db.Float)
    Plan_Sponsor =  db.Column(db.Float)
    Asset_Manager =  db.Column(db.Float)
    Other  =  db.Column(db.Float)
    VS_ID = db.Column(db.Integer, primary_key=True)

class Current_Month_Stats(db.Model):
    __tablename__ = 'VW_Current_Month'
    month_number =  db.Column(db.Integer, primary_key=True)
    month_year =  db.Column(db.Integer)
    month_id =  db.Column(db.Integer)
    month_name  = db.Column(db.String(20))
    month_short_name  = db.Column(db.String(3))

class Video_Tag(db.Model):
    __tablename__ = 'VW_VIDEO_TAG_COMPANIES'
    TL_ID = db.Column(db.Integer,primary_key = True)
    video_id = db.Column(db.Integer)
    tag_name = db.Column(db.String(200))
    tag_type = db.Column(db.String(20))


'''
class TagList(db.Model):
    TL_ID = db.Column(db.Integer, primary_key=True)
    TL_VID =  db.Column(db.Integer,db.ForeignKey('Video.V_ID'))
    TL_TID = db.Column(db.Integer,db.ForeignKey('Tag.T_ID'))
    tags = db.relationship("TagList", backref="tag")

    def __repr__(self):
        return '<TagList Video Id:(%r) - Tag Id:(%r)>' % (self.TL_VID,self.TL_TID)
'''