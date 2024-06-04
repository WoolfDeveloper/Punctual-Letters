class MessageRepository:
    errors = {
        "err.not_processed": "The file could not be Punctualized.",
        "err.file_null": "The path you have entered is not a valid file."
    }
    successes = {
        "succ.epub_processed": "The epub has been successfully processed."
    }

    @staticmethod
    def get_success(success):
        return MessageRepository.successes.get(success, "Success.")

    @staticmethod
    def get_error(error):
        return MessageRepository.errors.get(error, "An error has occurred.")
