class MessageRepository:
    errors = {
        "err.not_processed": "The file could not be Punctualized.",
        "err.file_not_valid": "The path you have entered is not a valid file.",
        "err.file_processed": "The file has already been punctualized.",
        "err.file_empty": "The file is empty."
    }
    successes = {
        "succ.epub_processed": "The epub has been successfully punctualized."
    }

    @staticmethod
    def get_success(success):
        return MessageRepository.successes.get(success, "Success.")

    @staticmethod
    def get_error(error):
        return MessageRepository.errors.get(error, "An error has occurred.")
