from datetime import datetime, date, time

class DateHelper:
    @staticmethod
    def to_str(obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        if isinstance(obj, time):
            return obj.strftime("%H:%M:%S")
        return obj

def format_model_to_dict(instance, fields=None):
    data = {}
    field_names = fields if fields else [f.name for f in instance._meta.fields]
    
    for field in field_names:
        value = getattr(instance, field, None)
        data[field] = DateHelper.to_str(value)
    return data