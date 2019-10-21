from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://glrkpyhoaqlqxe:35a6c790243d67c23c30e03bda09d06dad3240236eb2e1089ee3198f20a647b2@ec2-184-73-209-230.compute-1.amazonaws.com:5432/dnj92fb18te98'
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


@app.route("/members", methods=["GET"])
def get_members():
    all_members = Member.query.all()
    result = members_schema.dump(all_members)
    return jsonify(result)


@app.route("/member/<id>", methods=['GET'])
def get_member(id):
    member = Member.query.get(id)
    return member_schema.jsonify(member)


@app.route('/member/<id>', methods=['PUT'])
def member_update(id):
    member = Member.query.get(id)
    name = request.json['name']
    team = request.json['team']

    member.name = name
    member.team = team

    db.session.commit()
    return member_schema.jsonify(member)


@app.route('/member/<id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    db.session.delete(member)
    db.session.commit()
    return "Member was successfully removed"


if __name__ == '__main__':
    app.run(debug=True)
