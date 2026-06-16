from ast import pattern

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
            # Дата и время (всегда ЧЧ:ММ)
            r"(?P<date_time>\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2})\s+"
            # Дата учета (всегда ДД.ММ.ГГГГ)     
            r"(?P<date_accounting>\d{2}\.\d{2}\.\d{4})\s+"
            # Любые символы до начала суммы
            r"(?P<description_operation>.+?)\s+"
            # Сумма с пробелами в тысячах или без них + значок рубля
            r"(?P<sum_value>[+-]?\d+(?:\s\d+)*\.\d{2})\s*₽?\s+"
            r"(?P<remainder>\d+(?:\s\d+)*\.\d{2})" 
)
        return pattern
    
    def _process_text(self, text: str) -> list:
        """
        Обрабатываем сырой текст из файла, группируя по категориям
        информацию из выписки и превращая данные в словарь.
        """
        lines = text.split("\n")
        pattern = self.make_pattern()
        result = []
        for line in lines:
            match = re.match(pattern, line)
            if not match:
                continue # Если None - пропускаем строку
            transaction_dict = match.groupdict()
            result.append(transaction_dict)
                
        return result
            

parser = TBankParser("data/t_bank_test.pdf")
print(parser.parse())
