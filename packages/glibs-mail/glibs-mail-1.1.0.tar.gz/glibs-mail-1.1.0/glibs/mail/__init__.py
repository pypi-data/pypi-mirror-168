import email.header as email_header


class Contact(object):
    def __init__(self, email, name=""):
        self.email = email
        self.name = name

    def formatted(self):
        """
        if the recipient has a name, will return something like
        `John Doe <johndoe@geekie.com.br>`.
        Otherwise, will return just the email of the recipient.
        """
        if self.name:
            formatted_name = email_header.Header(self.name, "UTF-8").encode()
            return "{0} <{1}>".format(formatted_name, self.email)
        else:
            return self.email

    def to_dict(self):
        """
        Returns a dict with email (always) and name (only if present) as strings for easy digestion.
        """
        return (
            dict(email=self.email, name=self.name)
            if self.name
            else dict(email=self.email)
        )

    @staticmethod
    def new_from_parameter(contact):
        """
        This allows the user to pass `recipient` as a `str` on method calls.
        It makes the API backwards-compatible and also makes it simpler.
        """
        if isinstance(contact, Contact):
            return contact
        else:
            return Contact(contact)


class File(object):
    def __init__(self, content, type, file_name):
        self.content = content
        self.type = type
        self.file_name = file_name

    @staticmethod
    def new_from_parameter(file):
        if isinstance(file, File):
            return file
        else:
            return File(file)
