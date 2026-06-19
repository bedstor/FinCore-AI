import pdfplumber
import re

class BaseBankParser:
    """Стандартная модель банка"""

    def __init__(self, file_path: str):
        """Инициализируем атрибуты класса: путь к файлу"""
        self.file_path = file_path

    def _get_raw_text(self) -> str:
        """Получение и сохранение сырого текста со страниц файла"""
        text = ""
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text
    
    def parse(self):
        """Берём текст со страниц и вызываем метод для обработки его"""
        raw_text = self._get_raw_text()
        return self._process_text(raw_text)

    def _process_text(self, text):
        """Обрабатываем текст"""
        pass


class TBankParser(BaseBankParser):
    """Модель Т-банка"""

    def make_pattern(self):
        """Создание паттерна для нахождения данных"""
        pattern = (
            # Дата и время
            r"(?P<date_time>\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2})[\s\n]*"
            # Дата учета    
            r"(?P<date_accounting>\d{2}\.\d{2}\.\d{4})[\s\n]*"
            # Любые символы до начала суммы
            r"(?P<description_operation>.+?)[\s\n]*"
            # Сумма с пробелами в тысячах или без них + значок рубля
            r"(?P<sum_value>[+-]?\d+(?:\s\d+)*\.\d{2})\s*₽?[\s\n]*"
            r"(?P<remainder>\d+(?:\s\d+)*\.\d{2})" 
)
        return pattern
    
    def _process_text(self, text: str) -> list:
        """
        Находим нужные данные по паттерну, группируем
        и возвращаем их в виде пары "ключ - значение"
        """
        pattern = self.make_pattern()
        result = []
        for match in re.finditer(pattern, text):
            transaction_dict = match.groupdict()
            result.append(transaction_dict)
                
        return result


class SberParser(BaseBankParser):
    """Модель Сбер-банка"""

    def make_pattern(self):
        """Создание паттерна для нахождения данных"""
        pattern = (
            # Дата операции
            r"(?P<date_operation>\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2})[\s\n]*"
            # Дата обработки  
            r"(?P<date_processing>\d{2}\.\d{2}\.\d{4})[\s\n]*"
            # Любые символы до начала суммы
            r"(?P<description_operation>.+?)[\s\n]*"
            # Сумма с пробелами в тысячах или без них + значок рубля
            r"(?P<sum_value>[+-]?\d+(?:\s\d+)*\,\d{2})\s*₽?[\s\n]*"
            r"(?P<remainder>\d+(?:\s\d+)*\,\d{2})" 
)
        return pattern
    
    def _process_text(self, text: str) -> list:
        """
        Находим нужные данные по паттерну, группируем
        и возвращаем их в виде пары "ключ - значение"
        """
        pattern = self.make_pattern()
        result = []
        for match in re.finditer(pattern, text):
            transaction_dict = match.groupdict()
            result.append(transaction_dict)
        
        return result

sber = SberParser("data/sber_bank_test.pdf")
print(sber.parse())

