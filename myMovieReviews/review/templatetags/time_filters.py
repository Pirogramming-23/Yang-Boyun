from django import template

register = template.Library()

@register.filter
def hours_minutes(value):
    try:
        value = int(value)
        hours = value // 60
        minutes = value % 60
        if hours > 0:
            return f"{hours}시간 {minutes}분" if minutes else f"{hours}시간"
        else:
            return f"{minutes}분"
    except (ValueError, TypeError):
        return value 