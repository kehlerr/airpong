from immovable_object import ImmovableObject
from round_object import RoundObject


class Post(ImmovableObject, RoundObject):
    image_path = 'pic/post.png'
    size = (30, 30)
    radius = 15
