import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Numeric, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CustomBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, nullable=True, default=datetime.datetime.now())


class Camera(Base):
    __abstract__ = True

    number_cameras = Column(Integer, nullable=False)
    camera_quality = Column(String, nullable=False)
    video_format = Column(String, nullable=False)
    optical_stabilization = Column(Boolean, nullable=False, default=False)
    front_camera_quality = Column(String, nullable=False)


class User(CustomBase):
    __tablename__ = 'users'

    email = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String(12), nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False)

    def __str__(self):
        return f'Пользователь «{self.email}»'


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    id_order = Column(Integer, ForeignKey('orders.id'), nullable=False)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_product = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    is_deleted = Column(Boolean, nullable=False, default=False)

    order = relationship('Order')
    user = relationship('User')
    product = relationship('Product')

    def __str__(self):
        return f'Товар №{self.id_product}'


class Order(CustomBase):
    __tablename__ = 'orders'

    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default='created')
    is_deleted = Column(Boolean, nullable=False, default=False)

    user = relationship('User')
    order_item = relationship('OrderItem', back_populates='order')

    def __str__(self):
        return f'Заказ №{self.id}'


class Provider(CustomBase):
    __tablename__ = 'providers'

    label = Column(String, nullable=False)
    contact_info = Column(String, nullable=True)
    description = Column(String, nullable=True)
    location = Column(String, nullable=True)

    def __str__(self):
        return f'Поставщик «{self.label}»'


product_photo = Table(
    "product_photo",
    Base.metadata,
    Column("id_product", Integer, ForeignKey("products.id"), primary_key=True),
    Column("id_photo", Integer, ForeignKey("photos.id"), primary_key=True),
)


class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False, index=True)

    products = relationship("Product", secondary="product_photo", back_populates="photos")

    def __str__(self):
        return f'Фото №{self.id}'


class Product(CustomBase):
    __tablename__ = 'products'

    id_author = Column(Integer, ForeignKey('users.id'), nullable=True)
    id_editor_last = Column(Integer, ForeignKey('users.id'), nullable=True)
    id_provider = Column(Integer, ForeignKey('providers.id'), nullable=False)
    type = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    color_main = Column(String, nullable=False)
    material = Column(String, nullable=False)
    model = Column(String, nullable=False)
    height = Column(Numeric(precision=6, scale=2), nullable=False)
    width = Column(Numeric(precision=6, scale=2), nullable=False)
    weight = Column(Numeric(precision=6, scale=2), nullable=False)
    thickness = Column(Numeric(precision=6, scale=2), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    discount = Column(Integer, nullable=True, default=0)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    quantity = Column(Integer, nullable=True, default=1)
    equipment = Column(String, nullable=True)

    photos = relationship('Photo', secondary='product_photo', back_populates='products')
    author = relationship('User', foreign_keys=[id_author])
    editor_last = relationship('User', foreign_keys=[id_editor_last])
    provider = relationship('Provider', foreign_keys=[id_provider])

    __mapper_args__ = {
        'polymorphic_on': 'type'
    }

    def __str__(self):
        return f'Товар «{self.name}»'


class Technics(Product):
    __abstract__ = True

    screen_format = Column(String, nullable=False)
    operating_system = Column(String, nullable=False)
    memory_ram = Column(Integer, nullable=False)
    memory = Column(Integer, nullable=False)
    matrix_frequency = Column(Integer, nullable=False)
    matrix_type = Column(String, nullable=False)
    matrix_brightness = Column(String, nullable=False)
    matrix_contrast = Column(String, nullable=False)
    sound_technology = Column(String, nullable=True)
    headphone_output = Column(Boolean, nullable=False, default=False)
    date_release = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now()
    )
    screen_resolution = Column(String, nullable=False)
    screen_type = Column(String, nullable=False)
    screen_diagonal = Column(String, nullable=False)
    color_other = Column(String, nullable=True)


class Television(Technics):
    __tablename__ = 'televisions'

    id_product = Column(Integer, ForeignKey('products.id'), primary_key=True)
    consumption = Column(Integer, nullable=False)
    hdr_support = Column(Boolean, nullable=True)
    angle_view = Column(String, nullable=True)
    voice_assistant = Column(String, nullable=True)
    wifi_availability = Column(Boolean, nullable=False, default=False)
    wifi_standard = Column(String, nullable=True)
    sound_power = Column(String, nullable=True)
    subwoofer = Column(Boolean, nullable=False, default=False)
    sound_surround = Column(Boolean, nullable=False, default=False)
    codecs = Column(String, nullable=True)
    hdmi_ports = Column(Boolean, nullable=False, default=True)
    hdmi_version = Column(String, nullable=True)
    usb_ports = Column(String, nullable=True)
    smartphone_control = Column(Boolean, nullable=False, default=False)
    management_application = Column(String, nullable=True)
    bluetooth_control = Column(Boolean, nullable=False, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'television'
    }

    def __str__(self):
        return f'Телевизор «{self.name}»'


class Smartphone(Technics, Camera):
    __tablename__ = 'smartphones'

    id_product = Column(Integer, ForeignKey('products.id'), primary_key=True)
    support_lte = Column(Boolean, nullable=False, default=True)
    sim_card_format = Column(String, nullable=True)
    pixel_density = Column(Integer, nullable=False)
    degree_protection = Column(String, nullable=False)
    processor_model = Column(String, nullable=False)
    processor_frequency = Column(Integer, nullable=True)
    number_cores = Column(Integer, nullable=False)
    accumulator_type = Column(String, nullable=True)
    accumulator_capacity = Column(Integer, nullable=False)
    fast_charge = Column(Boolean, nullable=False, default=True)
    communication_standard = Column(String, nullable=True)
    sim_card_number = Column(String, nullable=True)
    sensors = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'smartphone'
    }

    def __str__(self):
        return f'Телефон «{self.name}»'


class Laptop(Technics):
    __tablename__ = 'laptops'

    id_product = Column(Integer, ForeignKey('products.id'), primary_key=True)
    consumption = Column(Integer, nullable=False)
    keyboard_layout = Column(String, nullable=False)
    keyboard_backlight = Column(String, nullable=False)
    touchpad = Column(String, nullable=False)
    fingerprint_scanner = Column(Boolean, nullable=False, default=False)
    hdr_support = Column(Boolean, nullable=True)
    type_graphics_accelerator = Column(String, nullable=False)
    video_card_model = Column(String, nullable=False)
    discrete_graphics = Column(String, nullable=True)
    video_chip = Column(String, nullable=False)
    video_memory_type = Column(String, nullable=True)
    video_memory = Column(Integer, nullable=False)
    clock_speed = Column(Integer, nullable=False)
    voice_assistant = Column(String, nullable=True)
    wifi_availability = Column(Boolean, nullable=False, default=True)
    wifi_standard = Column(String, nullable=True)
    sound_power = Column(String, nullable=True)
    hdmi_ports = Column(Boolean, nullable=False)
    usb_devices = Column(String, nullable=True)
    battery_life = Column(Numeric(precision=5, scale=3), nullable=False)
    microphone = Column(Boolean, nullable=False, default=True)

    __mapper_args__ = {
        'polymorphic_identity': 'laptop'
    }

    def __str__(self):
        return f'Ноутбук «{self.name}»'


class Smartwatch(Technics):
    __tablename__ = 'smartwatches'

    id_product = Column(Integer, ForeignKey('products.id'), primary_key=True)
    material_belt = Column(String, nullable=False)
    pixel_density = Column(Integer, nullable=False)
    degree_protection = Column(String, nullable=False)
    accumulator_type = Column(String, nullable=False)
    accumulator_capacity = Column(Integer, nullable=False)
    fast_charge = Column(Boolean, nullable=False, default=False)
    water_resistance = Column(Integer, nullable=True)
    measurements = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'smartwatch'
    }

    def __str__(self):
        return f'Часы «{self.name}»'


class Accessory(Product):
    __tablename__ = 'accessories'

    id_product = Column(Integer, ForeignKey('products.id'), primary_key=True)
    features = Column(String, nullable=True, default="нет")

    __mapper_args__ = {
        'polymorphic_identity': 'accessory'
    }

    def __str__(self):
        return f'Аксессуар «{self.name}»'


class Tablet(Technics, Camera):
    __tablename__ = 'tablets'

    id_product = Column(Integer, ForeignKey('products.id'), primary_key=True)
    pixel_density = Column(Integer, nullable=False)
    degree_protection = Column(String, nullable=False)
    processor_model = Column(String, nullable=False)
    processor_frequency = Column(Integer, nullable=False)
    number_cores = Column(Integer, nullable=False)
    support_lte = Column(Boolean, nullable=False, default=True)
    sim_card_format = Column(String, nullable=True)
    accumulator_type = Column(String, nullable=True)
    accumulator_capacity = Column(Integer, nullable=False)
    fast_charge = Column(Boolean, nullable=False, default=False)
    sensors = Column(String, nullable=True)
    communicate_module = Column(Boolean, nullable=False, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'tablet'
    }

    def __str__(self):
        return f'Планшет «{self.name}»'


class Review(CustomBase):
    __tablename__ = 'reviews'

    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_product = Column(Integer, ForeignKey('products.id'), nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.now())
    rating = Column(Integer, nullable=False)
    text = Column(String, nullable=True)

    user = relationship('User')
    product = relationship('Product')

    def __str__(self):
        return f'Отзыв №{self.id}'


class Favourite(Base):
    __tablename__ = 'favourites'

    id_user = Column(Integer, ForeignKey('users.id'), primary_key=True)
    id_product = Column(Integer, ForeignKey('products.id'), primary_key=True)
    is_deleted = Column(Boolean, nullable=False, default=False)

    user = relationship("User")
    product = relationship("Product")
