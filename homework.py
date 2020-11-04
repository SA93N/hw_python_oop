import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        total_today = 0
        date_today = dt.datetime.now().date()
        for record in self.records:
            if record.date == date_today:
                total_today += record.amount
        return total_today

    def get_week_stats(self):
        total_week = 0
        date_today = dt.datetime.now().date()
        week_ago = date_today - dt.timedelta(days=7)
        for record in self.records:
            if week_ago <= record.date <= date_today:
                total_week += record.amount
        return total_week


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.comment = comment
        if date == '':
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        total_today = super().get_today_stats()
        remained_today = self.limit - total_today
        if remained_today > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remained_today} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    USD_RATE = 80.0
    EURO_RATE = 90.0

    def get_today_cash_remained(self, currency):
        exchange_rate = {
            'rub': [self.RUB_RATE, 'руб'],
            'usd': [self.USD_RATE, 'USD'],
            'eur': [self.EURO_RATE, 'Euro']
        }

        total_today = super().get_today_stats()
        remained_today = round(((self.limit - total_today) / exchange_rate[currency][0]), 2)
        # считаю что этот иф вообще не нужен, но подругому не смог пройти тесты, возможно я где-то затупил)
        if remained_today - int(remained_today) == 0 and currency == 'rub':
            remained_today = int(remained_today)
        currency_name = exchange_rate[currency][1]
        if remained_today > 0:
            return f'На сегодня осталось {remained_today} {currency_name}'
        elif remained_today < 0:
            remained_today = abs(remained_today)
            return f'Денег нет, держись: твой долг - {remained_today} {currency_name}'
        else:
            return 'Денег нет, держись'


cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment="кофе"))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))

print(cash_calculator.get_today_cash_remained("rub"))
