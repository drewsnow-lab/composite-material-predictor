import sys
import json
import urllib.request
import urllib.error
from PyQt6.QtWidgets import (QApplication,
                             QDialog,
                             QDialogButtonBox, 
                             QFormLayout,
                             QLineEdit, 
                             QVBoxLayout, 
                             QGroupBox,
                             QLabel,
                             QMessageBox)

print("import success")

class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.x_for_predict = {}
        self.createFormGroupBox()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                     QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.get_predict)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle('Предсказатель прочности при растяжении материала')

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox('Заполните данные')
        self.layout = QFormLayout()

        button_list = ['Соотношение матрица-наполнитель',
                       'Плотность, кг/м3',
                       'Модуль упругости, ГПа',
                       'Количество отвердителя, м.%',
                       'Содержание эпоксидных групп,%',
                       'Температура вспышки',
                       'Поверхностная плотность, г/м2',
                       'Модуль упругости при растяжении, ГПа',
                       'Потребление смолы, г/м2',
                       'Угол нашивки, град',
                       'Шаг нашивки',
                       'Плотность нашивки_лог']

        for index, label in enumerate(button_list):
            x = QLineEdit()
            x.textChanged.connect(lambda text, idx=index+1: self.x_for_predict.update({idx: text}))
            self.layout.addRow(QLabel(label), x)
        self.formGroupBox.setLayout(self.layout)
    
    def get_predict(self):
        rslt = QMessageBox(self)
        rslt.setWindowTitle('Результат')
        
        try:
            # Собираем данные из всех полей
            x_list = []
            for i in range(1, 13):
                if i in self.x_for_predict:
                    try:
                        x_list.append(float(self.x_for_predict[i]))
                    except ValueError:
                        rslt.setText(f"Ошибка: значение '{self.x_for_predict[i]}' не является числом")
                        rslt.exec()
                        return
                else:
                    rslt.setText(f"Ошибка: поле {i} не заполнено")
                    rslt.exec()
                    return
            
            print(f"Отправляемые данные: {x_list}")
            
            # Создаем JSON данные
            json_data = json.dumps({'X_from_desktop': x_list})
            
            # Создаем запрос
            url = 'http://127.0.0.1:5000/api/v2/add_message/'
            req = urllib.request.Request(
                url,
                data=json_data.encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            try:
                # Отправляем запрос
                with urllib.request.urlopen(req, timeout=10) as response:
                    response_data = response.read().decode('utf-8')
                    
                    # Пытаемся распарсить JSON ответ
                    try:
                        result = json.loads(response_data)
                        rslt.setText(str(result))
                    except json.JSONDecodeError:
                        rslt.setText(f"Ответ сервера: {response_data}")
                        
            except urllib.error.HTTPError as e:
                rslt.setText(f"Ошибка HTTP {e.code}: {e.reason}")
            except urllib.error.URLError as e:
                rslt.setText(f"Ошибка соединения: {e.reason}\nУбедитесь, что сервер запущен на http://127.0.0.1:5000")
            except Exception as e:
                rslt.setText(f"Ошибка при отправке запроса: {str(e)}")
            
        except Exception as e:
            rslt.setText(f"Ошибка: {str(e)}")
        
        rslt.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec())