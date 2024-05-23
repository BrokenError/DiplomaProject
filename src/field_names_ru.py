BaseFields = {
    "id": "Номер",
    "date_created": "Дата создания",

}

CameraFields = {
    "number_cameras": "Количество камер",
    "camera_quality": "Качество камер",
    "video_format": "Видео формат",
    "optical_stabilization": "Оптическая стабилизация",
    "front_camera_quality": "Качество фронтальной камеры",
}

UserFields = BaseFields | {
    "email": "Почта",
    "first_name": "Имя",
    "last_name": "Фамилия",
    "phone_number": "Телефон",
    "photo_url": "Фотография",
}


OrderItemFields = {
    "id": "Номер",
    "id_order": "№ Заказа",
    "id_user": "№ Пользователя",
    "id_product": "№ Товара",
    "product": "Товар",
    "order": "Заказ",
    "user": "Пользователь",
    "quantity": "Количество",
}

OrderFields = BaseFields | {
    "id_user": "№ Пользователя",
    "user": "Пользователь",
    "payment_method": "Способ оплаты",
    "status": "Статус",
    "is_deleted": "Удален",
    "is_paid": "Оплачен",
}

ProviderFields = BaseFields | {
    "label": "Лейбл",
    "contact_info": "Контактная информация",
    "description": "Описание",
    "location": "Местонахождение",
}

PhotoFields = {
    "id": "Номер",
    "url": "Ссылка",
    "products": "Товары",
}


ProductFields = BaseFields | {
    "id_author": "Номер автора",
    "id_editor_last": "Номер редактора",
    "id_provider": "Номер поставщика",
    "author": "Автор",
    "editor_last": "Редактор",
    "photos": "Фотографии",
    "provider": "Поставщик",
    "type": "Категория товара",
    "name": "Название",
    "color_main": "Основной цвет",
    "color_hex": "Hex цвет",
    "material": "Материал",
    "model": "Модель",
    "height": "Высота, мм",
    "width": "Ширина, мм",
    "weight": "Вес, кг",
    "thickness": "Толщина, мм",
    "description": "Описание",
    "price": "Цена, Руб",
    "discount": "Скидка, %",
    "is_active": "Активный",
    "is_deleted": "Удален",
    "quantity": "Количество, шт",
    "equipment": "Комплектация",
}

TechnicsFields = ProductFields | {
    "screen_format": "Формат экрана",
    "operating_system": "Операционная система",
    "memory_ram": "Оперативная память, Гб.",
    "memory": "Внутреняя память, Гб.",
    "matrix_frequency": "Частота матрицы, Гц.",
    "matrix_type": "Тип матрицы",
    "matrix_brightness": "Яркость матрицы, Кд/м²",
    "matrix_contrast": "Контрастность матрицы",
    "sound_technology": "Технология звука",
    "headphone_output": "Выход на наушники",
    "date_release": "Дата выхода",
    "screen_resolution": "Разрешение экрана",
    "screen_diagonal": "Диагональ экрана",
    "color_other": "Дополнительный цвет",
}

TelevisionFields = TechnicsFields | {
    "id_product": "Номер товара",
    "consumption": "Потребление, Вт",
    "hdr_support": "Поддержка HDR",
    "angle_view": "Угол обзора",
    "voice_assistant": "Голосовой ассистент",
    "wifi_availability": "Наличие Wi-Fi",
    "wifi_standard": "Wi-Fi стандарт",
    "sound_power": "Мощность звука, Вт",
    "subwoofer": "Сабвуфер",
    "sound_surround": "Объемный звук",
    "codecs": "Кодеки",
    "hdmi_ports": "HDMI выходы",
    "hdmi_version": "HDMI версии",
    "usb_ports": "USB порты",
    "smartphone_control": "Управление через телефон",
    "management_application": "Приложение",
    "bluetooth_control": "Bluetooth",
}

SmartphoneFields = TechnicsFields | CameraFields | {
    "id_product": "Номер товара",
    "support_lte": "Поддержка LTE",
    "sim_card_format": "Формат сим-карты",
    "pixel_density": "Плотность пикселей, ppi",
    "degree_protection": "Степень защиты IP",
    "processor_model": "Модель процессора",
    "processor_frequency": "Частота процессора, ГГц",
    "number_cores": "Количество ядер",
    "accumulator_type": "Тип аккумулятора",
    "accumulator_capacity": "Емкость аккумулятора, мА*ч",
    "fast_charge": "Быстрая зарядка",
    "communication_standard": "Стандарт связи",
    "sim_card_number": "Количество сим-карт",
    "sensors": "Сенсоры",
}

LaptopFields = TechnicsFields | {
    "id_product": "Номер товара",
    "consumption": "Потребление, Вт",
    "keyboard_layout": "Раскладка клавиатуры",
    "keyboard_backlight": "Подсветка клавиш",
    "touchpad": "Тачпад",
    "fingerprint_scanner": "Сканер отпечатка пальца",
    "hdr_support": "Поддержка HDR",
    "processor_model": "Модель процессора",
    "processor_frequency": "Частота процессора, ГГц",
    "number_cores": "Количество ядер",
    "nuber_threads": "Количество потоков",
    "type_graphics_accelerator": "Вид графического ускорителя",
    "video_card_model": "Модель встроенной видеокарты",
    "discrete_graphics": "Модель дискретной видеокарты",
    "video_chip": "Производитель видеочипа",
    "video_memory_type": "Тип видеопамяти",
    "video_memory": "Объем видеопамяти",
    "clock_speed": "Частота видеокарты",
    "voice_assistant": "Голосовй ассистент",
    "wifi_availability": "Наличие Wi-Fi",
    "wifi_standard": "Wi-Fi стандарт",
    "sound_power": "Мощность звука, Вт",
    "hdmi_ports": "HDMI выходы",
    "usb_ports": "Разъемы USB",
    "battery_life": "Время автономной работы",
    "microphone": "Наличие микрофона",
}


SmartwatchFields = TechnicsFields | {
    "id_product": "Номер товара",
    "material_belt": "Материал ремня",
    "pixel_density": "Плотность пикселей, ppi",
    "degree_protection": "Степень защиты IP",
    "accumulator_type": "Тип аккумулятора",
    "accumulator_capacity": "Емкость аккумулятора, мА*ч",
    "fast_charge": "Быстрая зарядка",
    "water_resistance": "Водонепроницаемость, Бар",
    "measurements": "Измерения",
}


AccessoryFields = TechnicsFields | {
    "id_product": "Номер товара",
    "features": "Особенности",
}

TabletFields = TechnicsFields | CameraFields | {
    "id_product": "Номер товара",
    "pixel_density": "Плотность пикселей, ppi",
    "degree_protection": "Степень защиты IP",
    "processor_model": "Модель процессора",
    "processor_frequency": "Частота процессора, ГГц",
    "number_cores": "Количество ядер",
    "support_lte": "Поддержка LTE",
    "sim_card_format": "Формат сим-карты",
    "accumulator_type": "Тип аккумулятора",
    "accumulator_capacity": "Емкость аккумулятора, мА*ч",
    "fast_charge": "Быстрая зарядка",
    "sensors": "Сенсоры",
    "communicate_module": "Модуль сотовой связи",
}


ReviewFields = BaseFields | {
    "id_user": "№ Пользователя",
    "id_product": "№ Товара",
    "user": "Пользователь",
    "product": "Товар",
    "date_created": "Дата создания",
    "rating": "Оценка",
    "text": "Текст",
}


FavouriteFields = {
    "id_user": "№ Пользователя",
    "id_product": "№ Товара",
    "user": "Пользователь",
    "product": "Товар",
    "is_deleted": "Удален",
}

NameFilters = {
    "color_main": "Цвет",
    "price": "Цена",
    "model": "Бренд",
    "material": "Материал",
    "memory": "Объем памяти",
    "memory_ram": "Объем оперативной памяти",
    "date_release": "Год релиза",
    "accumulator_capacity": "Емкость аккумулятора",
    "matrix_frequency": "Частота обновления экрана",
    "screen_diagonal": "Диагональ экрана",
    "number_cores": "Количество ядер",
    "degree_protection": "Степень защиты",
    "water_resistance": "Водонипроницаемость",
    "screen_resolution": "Разрешение экрана",
    "processor_model": "Модель процессора",
    "video_card_model": "Модель видеокарты",
    "matrix_type": "Тип матрицы",
}
