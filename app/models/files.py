import os
from werkzeug.utils import secure_filename

from flask import current_app as application
from flask_login import current_user

from app import db

from app.models.base_mixin import BaseMixin

from app.handlers.files import FileHandler
from app.handlers.files import AWSFileHandler


class File(db.Model, BaseMixin):
    __tablename__ = "files"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    extension = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    hash = db.Column(db.String(255), nullable=False)

    created_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )

    user_id = db.Column(db.ForeignKey("users.id"))
    recipe_id = db.Column(db.ForeignKey("recipes.id"))

    created_by = db.Column(db.ForeignKey("users.id"), nullable=False, index=True)

    file_type = db.Column(db.String(40))

    author = db.relationship(
        "User", primaryjoin="File.created_by == User.id", backref="files",
    )

    __mapper_args__ = {"polymorphic_on": file_type, "polymorphic_identity": "file"}

    subfolder = ""

    def _get_hash_from_path(self):
        from hashlib import md5

        return md5(self.path.encode("utf-8")).hexdigest()

    def rename_to_id(self):
        self.path = os.path.join(self.subfolder, f"{self.id}.{self.extension}")
        super().edit()
        return self

    def save(self):
        # converts "some.picture.jpg" to "some.picture"
        self.name = secure_filename(".".join(self.data.filename.split(".")[:-1]))
        # converts "some.picture.jpg" to "jpg"
        self.extension = secure_filename(".".join(self.data.filename.split(".")[-1:]))
        self.path = os.path.join(self.subfolder, f"{self.name}.{self.extension}")

        if getattr(self, "created_by", None) is None:
            self.created_by = current_user.id

        # hash cannot be empty, but real will be created after path
        self.hash = ""

        super().save()

        # rename to match db id
        self.rename_to_id()

        self.hash = self._get_hash_from_path()
        super().edit()

        self.name = f"{self.id}.{self.extension}"
        # save file to filesystem
        if application.config["STORAGE_SYSTEM"] == "DEFAULT":
            FileHandler(subfolder=self.subfolder).save(self)
        elif application.config["STORAGE_SYSTEM"] == "AWS":
            AWSFileHandler().save(self)
        else:
            FileHandler(subfolder=self.subfolder).save(self)

        self.expire()

        return self

    def can_view(self, user) -> bool:
        """Check for permission

        To be overwritten in child classes

        Returns:
            bool -- True
        """
        return True

    @property
    def url(self):
        return AWSFileHandler().create_presigned_url(self)


class ImageFile(File):
    __mapper_args__ = {"polymorphic_identity": "image"}


class RecipeImageFile(ImageFile):
    __mapper_args__ = {"polymorphic_identity": "recipe_image"}

    recipe = db.relationship(
        "Recipe",
        primaryjoin="RecipeImageFile.recipe_id == Recipe.id",
        backref="images",
    )

    # def can_view(self, user):
    #     # private?
    #     return self.recipe in user.recipes or self.recipe.public or user.is_admin
