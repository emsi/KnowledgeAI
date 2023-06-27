"""
A generic chatbot class implementing common functionality.
"""
from config import settings


class Chat:
    """
    A generic chatbot class implementing common functionality.
    """

    @staticmethod
    def log(question, response, prompt):
        """
        Log a question and response to the log file.
        :param question: question asked
        :param response: response given
        :param prompt: full prompt as passed to the model
        """
        log_message = ""
        if settings.LOG_QUESTIONS:
            log_message += f"####\nQUESTION: {question}\n"
        if settings.LOG_ANSWERS:
            log_message += f"ANSWER: {response}\n"
        if settings.LOG_PROMPTS:
            log_message += f"PROMPT: {prompt}\n"
        if settings.LOG_ANSWERS or settings.LOG_QUESTIONS or settings.LOG_PROMPTS:
            logger.info(f"{log_message}####\n")


if settings.LOG_ANSWERS or settings.LOG_QUESTIONS or settings.LOG_PROMPTS:
    import logging
    from logging.handlers import RotatingFileHandler

    # logging.basicConfig(filename='example.log')
    # logging.debug('This message should go to the log file')

    logger = logging.getLogger('AppLogger')
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(settings.DATA / 'app.log')
    logger.addHandler(handler)