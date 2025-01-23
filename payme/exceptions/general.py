import logging


class BaseError(Exception):
    """Base class for all errors in the payment system."""
    logger = logging.getLogger(__name__)

    def __init__(self, code, message, data=None):
        super().__init__(message["en"])  # Default to English
        self.code = code
        self.data = data
        self.message = message

        # pylint: disable=W1203
        self.logger.error(f"Error {code}: {message['en']}. Data: {data}")


class CardError(BaseError):
    """Base class for card-related errors."""


class TransportError(CardError):
    message = {
        "en": "Transport error.",
        "ru": "Ошибка транспорта.",
        "uz": "Transport xatosi."
    }

    def __init__(self, data=None):
        super().__init__(-32300, self.message, data)


class ParseError(CardError):
    message = {
        "en": "Parse error.",
        "ru": "Ошибка парсинга.",
        "uz": "Parse xatosi."
    }

    def __init__(self, data=None):
        super().__init__(-32700, self.message, data)


class InvalidRequestError(CardError):
    message = {
        "en": "Invalid Request.",
        "ru": "Неверный запрос.",
        "uz": "Noto'g'ri so'rov."
    }

    def __init__(self, data=None):
        super().__init__(-32600, self.message, data)


class MethodNotFoundError(CardError):
    message = {
        "en": "Method not found.",
        "ru": "Метод не найден.",
        "uz": "Metod topilmadi."
    }

    def __init__(self, data=None):
        super().__init__(-32601, self.message, data)


class InvalidParamsError(CardError):
    message = {
        "en": "Invalid Params.",
        "ru": "Неверные параметры.",
        "uz": "Noto'g'ri parametrlari."
    }

    def __init__(self, data=None):
        super().__init__(-32602, self.message, data)


class InvalidTokenFormat(CardError):
    """Invalid token format during card operation."""
    message = {
        "en": "Invalid token format.",
        "ru": "Неверный формат токена.",
        "uz": "Noto'g'ri token formati."
    }

    def __init__(self, data=None):
        super().__init__(-32500, self.message, data)


class AccessDeniedError(CardError):
    message = {
        "en": "Access denied.",
        "ru": "Доступ запрещен.",
        "uz": "Kirish taqiqlangan."
    }

    def __init__(self, data=None):
        super().__init__(-32504, self.message, data)


class CardNotFoundError(CardError):
    message = {
        "en": "Card not found.",
        "ru": "Карта не найдена.",
        "uz": "Karta topilmadi."
    }

    def __init__(self, data=None):
        super().__init__(-31400, self.message, data)


class SmsNotConnectedError(CardError):
    message = {
        "en": "SMS notification not connected.",
        "ru": "СМС-уведомление не подключено.",
        "uz": "SMS xabarnoma ulanmadi."
    }

    def __init__(self, data=None):
        super().__init__(-31301, self.message, data)


class BalanceError(CardError):
    message = {
        "en": "Unable to retrieve card balance. Please try again later.",
        "ru": "Не удалось получить баланс карты. Повторите попытку позже.",
        "uz": "Karta balansini olish imkoni yo'q. Keyinroq qayta urinib ko'ring."
    }

    def __init__(self, data=None):
        super().__init__(-31302, self.message, data)


class InsufficientFundsError(CardError):
    message = {
        "en": "Insufficient funds on the card.",
        "ru": "Недостаточно средств на карте.",
        "uz": "Kartada yetarli mablag' yo'q."
    }

    def __init__(self, data=None):
        super().__init__(-31303, self.message, data)


class InsufficientFundsErrorV2(CardError):
    message = {
        "en": "Insufficient funds on the card.",
        "ru": "Недостаточно средств на карте.",
        "uz": "Kartada yetarli mablag' yo'q."
    }

    def __init__(self, data=None):
        super().__init__(-31630, self.message, data)


class InvalidCardNumberError(CardError):
    message = {
        "en": "Invalid card number provided.",
        "ru": "Указан неверный номер карты.",
        "uz": "Noto'g'ri karta raqami ko'rsatilgan."
    }

    def __init__(self, data=None):
        super().__init__(-31300, self.message, data)


class ProcessingServerError(CardError):
    message = {
        "en": "Processing center server is unavailable. Please try again later.",
        "ru": "Сервер процессингового центра недоступен. Повторите попытку позже.",
        "uz": "Ishlov berish markazi serveriga ulanish imkoni yo'q. Keyinroq urining."
    }

    def __init__(self, data=None):
        super().__init__(-31002, self.message, data)


class OtpError(BaseError):
    """Base class for OTP-related errors."""


class OtpSendError(OtpError):
    message = {
        "en": "Error occurred while sending OTP. Please try again.",
        "ru": "Ошибка при отправке OTP. Повторите попытку.",
        "uz": "OTP yuborishda xatolik yuz berdi. Qayta urinib ko'ring."
    }

    def __init__(self, data=None):
        super().__init__(-31110, self.message, data)


class OtpExpiredError(OtpError):
    message = {
        "en": "OTP code has expired. Request a new code.",
        "ru": "Код OTP истек. Запросите новый код.",
        "uz": "OTP kodi eskirdi. Yangi kodni so'rang."
    }

    def __init__(self, data=None):
        super().__init__(-31101, self.message, data)


class OtpAttemptsExceededError(OtpError):
    message = {
        "en": "Number of attempts to enter the code has been exceeded.",
        "ru": "Превышено количество попыток ввода кода.",
        "uz": "Kodni kiritish urinishlari soni oshib ketdi."
    }

    def __init__(self, data=None):
        super().__init__(-31102, self.message, data)


class OtpInvalidCodeError(OtpError):
    message = {
        "en": "Invalid OTP code entered.",
        "ru": "Введен неверный код OTP.",
        "uz": "Noto'g'ri OTP kodi kiritildi."
    }

    def __init__(self, data=None):
        super().__init__(-31103, self.message, data)


class ReceiptsNotFoundError(BaseError):
    message = {
        "en": "No receipts found for the given transaction ID.",
        "ru": "Квитанции по данному ID транзакции не найдены.",
        "uz": "Berilgan tranzaksiya ID uchun kvitansiyalar topilmadi."
    }

    def __init__(self, data=None):
        super().__init__(-31602, self.message, data)


class UnknownPartnerError(BaseError):
    message = {
        "en": "The given partner ID is unknown.",
        "ru": "Указанный идентификатор партнера неизвестен.",
        "uz": "Ko'rsatilgan hamkor ID noma'lum."
    }

    def __init__(self, data=None):
        super().__init__(-31601, self.message, data)


errors_map = {
    -32300: TransportError,
    -32700: ParseError,
    -32600: InvalidRequestError,
    -32601: MethodNotFoundError,
    -32602: InvalidParamsError,
    -32504: AccessDeniedError,
    -31400: CardNotFoundError,
    -31301: SmsNotConnectedError,
    -31302: BalanceError,
    -31303: InsufficientFundsError,
    -31630: InsufficientFundsErrorV2,
    -31300: InvalidCardNumberError,
    -31002: ProcessingServerError,
    -31110: OtpSendError,
    -31101: OtpExpiredError,
    -31102: OtpAttemptsExceededError,
    -31103: OtpInvalidCodeError,
    -31602: ReceiptsNotFoundError,
    -32500: InvalidTokenFormat,
    -31601: UnknownPartnerError,
    -32400: SystemError
}
