from flask_marshmallow import Marshmallow
from models import User, SavedPlaces

ma = Marshmallow()

class UserSchema(ma.ModelSchema):
        class Meta:
            model = User

class SavedPlacesSchema(ma.ModelSchema):
    class Meta:
        model = SavedPlaces

savedplace_schema = SavedPlacesSchema()
savedplaces_schema = SavedPlacesSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


