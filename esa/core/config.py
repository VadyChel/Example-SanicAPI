import re


class Config:
    MESSAGES = {
        "error_invalid_json": {
            "message": {
                "error": "Was provided an invalid data"
            }
        },
        "error_user_not_found": {
            "message": {
                "error": "There is no such user with such an ID"
            }
        },
        "error_invalid_password": {
            "message": {
                "error": "Was provided an invalid password"
            }
        },
        "error_email_already_used": {
            "message": {
                "error": "Specified mail already in use"
            }
        },
        "error_invalid_email": {
            "message": {
                "error": "There is a invalid email"
            }
        },
        "successfully_create_user": {
            "message": {
                'successfully': 'Creating user was successfully'
            }
        },
        "successfully_delete_user": {
            "message": {
                "successfully": "Deleting user was successfully"
            }
        },
        "successfully_edit_user": {
            "message": {
                "successfully": "Editing user was successfully"
            }
        }
    }
    EMAIL_REGEX = re.compile("(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)")
