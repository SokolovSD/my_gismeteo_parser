import datetime
import peewee

base = peewee.SqliteDatabase("Weather.db")
cur = base.cursor()


class Weather(peewee.Model):
    day = peewee.DateField()
    rainfall = peewee.CharField()
    night_t = peewee.CharField()
    day_t = peewee.CharField()
    update_time = peewee.DateTimeField()

    class Meta:
        database = base


class InteractorWithDB:
    def __init__(self, dbname):
        self.db = dbname

    def save(self, data_to_save):
        # print('save')
        for day in data_to_save:
            day['update_time'] = datetime.datetime.now()
        # print(data)
        self.db.insert_many(data_to_save).execute()

    def get_from_db(self, start, finish, first):
        data_from_db_res = []
        a = start.split('-')
        b = finish.split('-')

        aa = datetime.date(int(a[0]), int(a[1]), int(a[2]))
        bb = datetime.date(int(b[0]), int(b[1]), int(b[2]))
        if first:
            delta = 6
        elif a == b:
            delta = 0
        else:
            delta = str(bb - aa)
            delta = int(delta.split()[0])

        for day in range(delta + 1):
            data_from_db = {}
            try:
                res = Weather.select().order_by(Weather.update_time.desc()).where(Weather.day == aa).get()

                data_from_db['day'] = res.day
                data_from_db['rainfall'] = res.rainfall
                data_from_db['night_t'] = res.night_t
                data_from_db['day_t'] = res.day_t
                data_from_db_res.append(data_from_db)
                if first:
                    aa += datetime.timedelta(days=-1)
                else:
                    aa += datetime.timedelta(days=1)
            except Weather.DoesNotExist:
                if first:
                    aa += datetime.timedelta(days=-1)
                else:
                    aa += datetime.timedelta(days=1)

        return data_from_db_res


Weather.create_table()
