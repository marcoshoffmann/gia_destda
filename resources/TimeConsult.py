from datetime import datetime
from calendar import monthrange

class TimeConsult:
    def __init__(self) -> None:
        self.actual_month = f'{datetime.now().month - 1:02}' if not datetime.now().month.__eq__(1) else '12'
        self.updated_month = f'{datetime.now().month:02}'
        self.actual_year = f'{datetime.now().year}' if not datetime.now().month.__eq__(1) else f'{datetime.now().year - 1}'
        self.updated_year = f'{datetime.now().year}'
        self.competence_start = f'01/{self.actual_month}/{self.actual_year}'
        self.competence_end = f'{monthrange(year=int(self.actual_year), month=int(self.actual_month))}/{self.actual_month}/{self.actual_year}'
