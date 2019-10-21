from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    team = db.Column(db.String(50), unique=False)

    def __init__(self, name, team):
        self.name = name
        self.team = team


class MemberSchema(ma.Schema):
    class Meta:
        fields = ('name', 'team')


member_schema = MemberSchema()
members_schema = MemberSchema(many=True)


@app.route("/member", methods=["POST"])
def add_member():
    name = request.json['name']
    team = request.json['team']

    new_member = Member(name, team)

    db.session.add(new_member)
    db.session.commit()

    member = Member.query.get(new_member.id)

    return member_schema.jsonify(member)


if __name__ == '__main__':
    app.run(debug=True)
