from random import randint

service_classes = {
    1: 'консультация',
    2: 'лечение',
    3: 'стационар',
    4: 'диагностика',
    5: 'лаборатория',
}


def get_service_class_and_name(service: str) -> dict:
    class_num = randint(1, 5)
    return {
        'service_class': class_num,
        'service_name': service_classes[class_num]
    }
