import peewee

base = peewee.SqliteDatabase("Weather.db")


class Weather(peewee.Model):
    day = peewee.DateField()
    rainfall = peewee.CharField()
    night_t = peewee.CharField()
    day_t = peewee.CharField()
    update_time = peewee.DateTimeField()
    
    class Meta:
        database = base


cur = base.cursor()