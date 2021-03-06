from reserver_app.run import db
from passlib.hash import pbkdf2_sha256 as sha256

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    #TODO created, updated timestamps, role, etc.
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def return_all(cls):
        all_users = UserModel.query.all()
        def as_json(x):
            return {
                'username': x.username,
                'password': x.password
            }
        users_list = list(map(lambda user: as_json(user), all_users))
        return {'users': users_list}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} user(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Deleting all users operation failed'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
        
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    # Unique token identifier
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.comit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)