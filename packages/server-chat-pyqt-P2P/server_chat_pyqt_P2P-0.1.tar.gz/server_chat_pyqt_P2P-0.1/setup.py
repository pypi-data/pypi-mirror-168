from setuptools import setup, find_packages

setup(name='server_chat_pyqt_P2P',
      version='0.1',
      description='Server_packet',
      packages=find_packages(),  # Будем искать пакеты тут(включаем авто поиск пакетов)
      author_email='maximichev@mail.ru',
      author='Anatoliy',
      install_requires=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      # зависимости которые нужно до установить
      )