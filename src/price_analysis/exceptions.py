class AnalysisError(Exception):
    """Базовое исключение"""

class PriceLoadError(AnalysisError):
    """Ошибка при выгрузке данных"""
    def __init__(self, filename: str, reason: str, row: int | None = None):
        self.filename = filename
        self.reason = reason
        self.row = row
        error_place = f", строка {row-1}" if row else ""
        super().__init__(f"{filename}{error_place}: {reason}")

class MissingColumnError(PriceLoadError):
    """Ошибка отсутствия нужных колонок"""
    def __init__(self, filename: str, column: set[str]):
        self.column = column
        super().__init__(filename, f"отсутствуют колонки: {', '.join(sorted(column))}")