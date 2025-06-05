import sys, json, os, socket
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QFileDialog,
    QHeaderView, QInputDialog, QComboBox, QGridLayout, QDialog,
    QTabWidget, QTextEdit
)
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt, QDate
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

DATA_DIR = "data"
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")
SALES_FILE = os.path.join(DATA_DIR, "sales_log.json")
os.makedirs(DATA_DIR, exist_ok=True)

LOW_STOCK_THRESHOLD = 5

LANGUAGES = {
    "עברית": {
        "title": "מנהל קנאביס ברצלונה 🌿",
        "search": "🔍 חפש...",
        "sort": ["מיין לפי", "מחיר", "כמות", "הנחה"],
        "headers": ["מוצר", "כמות", "מחיר", "עלות", "הנחה (%)"],
        "add": "➕ הוסף מוצר",
        "delete": "🗑️ מחק",
        "save": "💾 שמור",
        "export": "⬆️ ייצא",
        "sell": "💰 בצע עסקה",
        "saved": "המלאי נשמר!",
        "exported": "הייצוא הצליח!",
        "new_product": "הוסף מוצר חדש",
        "product_name": "שם המוצר:",
        "product_type": "סוג:",
        "quantity": "כמות:",
        "price": "מחיר:",
        "cost": "עלות:",
        "discount": "הנחה (%):",
        "low_stock": "⚠️ מלאי נמוך: ",
        "sell_product": "בחר מוצר:",
        "sell_quantity": "כמות מכירה:",
        "sell_button": "מכור",
        "cancel": "ביטול",
        "ok": "אישור",
        "statistics": "📊 סטטיסטיקות",
        "daily_profit": "רווח יומי",
        "weekly_profit": "רווח שבועי",
        "monthly_profit": "רווח חודשי",
        "yearly_profit": "רווח שנתי",
        "inventory_value": "שווי מלאי",
        "sales_history": "היסטוריית מכירות",
        "language": "שפה",
        "general": "כללי",
        "product_info": "פרטי מוצר",
        "sale_info": "פרטי מכירה",
        "total_revenue": "סך הכנסות",
        "total_cost": "סך עלויות",
        "total_profit": "סך רווח",
    },
    "English": {
        "title": "Barcelona Cannabis Shop Manager 🌿",
        "search": "🔍 Search...",
        "sort": ["Sort by", "Price", "Quantity", "Discount"],
        "headers": ["Product", "Qty", "Price", "Cost", "Discount (%)"],
        "add": "➕ Add Product",
        "delete": "🗑️ Delete",
        "save": "💾 Save",
        "export": "⬆️ Export",
        "sell": "💰 Sell",
        "saved": "Inventory saved!",
        "exported": "Export successful!",
        "new_product": "Add New Product",
        "product_name": "Product Name:",
        "product_type": "Type:",
        "quantity": "Quantity:",
        "price": "Price:",
        "cost": "Cost:",
        "discount": "Discount (%):",
        "low_stock": "⚠️ Low stock: ",
        "sell_product": "Select Product:",
        "sell_quantity": "Sale Quantity:",
        "sell_button": "Sell",
        "cancel": "Cancel",
        "ok": "OK",
        "statistics": "📊 Statistics",
        "daily_profit": "Daily Profit",
        "weekly_profit": "Weekly Profit",
        "monthly_profit": "Monthly Profit",
        "yearly_profit": "Yearly Profit",
        "inventory_value": "Inventory Value",
        "sales_history": "Sales History",
        "language": "Language",
        "general": "General",
        "product_info": "Product Information",
        "sale_info": "Sale Information",
        "total_revenue": "Total Revenue",
        "total_cost": "Total Cost",
        "total_profit": "Total Profit",
    }
}

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {path}.  Returning default.")
            return default
    return default

def save_json(data, path):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving to {path}: {e}")
        QMessageBox.critical(None, "Error", f"Failed to save data to {path}.  Check permissions and disk space.")

class AddProductDialog(QDialog):
    def __init__(self, parent=None, tr=None):
        super().__init__(parent)
        self.tr = tr if tr else LANGUAGES["עברית"]
        self.setWindowTitle(self.tr["new_product"])
        self.layout = QGridLayout(self)

        self.name_label = QLabel(self.tr["product_name"])
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label, 0, 0)
        self.layout.addWidget(self.name_input, 0, 1)

        self.type_label = QLabel(self.tr["product_type"])
        self.type_combo = QComboBox()
        self.type_combo.addItems(["אינדיקה", "סאטיבה", "היבריד"])
        self.layout.addWidget(self.type_label, 1, 0)
        self.layout.addWidget(self.type_combo, 1, 1)

        self.quantity_label = QLabel(self.tr["quantity"])
        self.quantity_input = QLineEdit()
        self.quantity_input.setValidator(Qt.IntValidator())
        self.layout.addWidget(self.quantity_label, 2, 0)
        self.layout.addWidget(self.quantity_input, 2, 1)

        self.price_label = QLabel(self.tr["price"])
        self.price_input = QLineEdit()
        self.price_input.setValidator(Qt.DoubleValidator())
        self.layout.addWidget(self.price_label, 3, 0)
        self.layout.addWidget(self.price_input, 3, 1)

        self.cost_label = QLabel(self.tr["cost"])
        self.cost_input = QLineEdit()
        self.cost_input.setValidator(Qt.DoubleValidator())
        self.layout.addWidget(self.cost_label, 4, 0)
        self.layout.addWidget(self.cost_input, 4, 1)

        self.discount_label = QLabel(self.tr["discount"])
        self.discount_input = QLineEdit()
        self.discount_input.setValidator(Qt.IntValidator())
        self.layout.addWidget(self.discount_label, 5, 0)
        self.layout.addWidget(self.discount_input, 5, 1)

        self.buttons = QHBoxLayout()
        self.ok_button = QPushButton(self.tr["ok"])
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton(self.tr["cancel"])
        self.cancel_button.clicked.connect(self.reject)
        self.buttons.addWidget(self.ok_button)
        self.buttons.addWidget(self.cancel_button)
        self.layout.addLayout(self.buttons, 6, 0, 1, 2)

    def get_data(self):
        name = self.name_input.text()
        product_type = self.type_combo.currentText().lower()
        quantity_text = self.quantity_input.text()
        price_text = self.price_input.text()
        cost_text = self.cost_input.text()
        discount_text = self.discount_input.text()

        if not name:
            QMessageBox.warning(self, self.tr["error"], "Product name cannot be empty.")
            return None

        if not quantity_text or not price_text or not cost_text or not discount_text:
            QMessageBox.warning(self, self.tr["error"], "All fields must be filled.")
            return None
        try:
            quantity = int(quantity_text)
            price = float(price_text)
            cost = float(cost_text)
            discount = int(discount_text) / 100.0
            return {"name": name, "type": product_type, "quantity": quantity, "price": price, "cost": cost, "discount": discount}
        except ValueError:
            QMessageBox.warning(self, self.tr["error"], "Invalid number entered.")
            return None

class SellDialog(QDialog):
    def __init__(self, parent=None, inventory_items=None, tr=None):
        super().__init__(parent)
        self.tr = tr if tr else LANGUAGES["עברית"]
        self.setWindowTitle(self.tr["sell"])
        self.inventory_items = inventory_items if inventory_items else {}
        self.layout = QGridLayout(self)

        self.product_label = QLabel(self.tr["sell_product"])
        self.product_combo = QComboBox()
        self.product_combo.addItems(self.inventory_items.keys())
        self.layout.addWidget(self.product_label, 0, 0)
        self.layout.addWidget(self.product_combo, 0, 1)

        self.quantity_label = QLabel(self.tr["sell_quantity"])
        self.quantity_input = QLineEdit()
        self.quantity_input.setValidator(Qt.IntValidator())
        self.layout.addWidget(self.quantity_label, 1, 0)
        self.layout.addWidget(self.quantity_input, 1, 1)

        self.buttons = QHBoxLayout()
        self.sell_button = QPushButton(self.tr["sell_button"])
        self.sell_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton(self.tr["cancel"])
        self.cancel_button.clicked.connect(self.reject)
        self.buttons.addWidget(self.sell_button)
        self.buttons.addWidget(self.cancel_button)
        self.layout.addLayout(self.buttons, 2, 0, 1, 2)

    def get_sale_data(self):
        product_name = self.product_combo.currentText()
        quantity_text = self.quantity_input.text()
        if not quantity_text:
             QMessageBox.warning(self, self.tr["error"], "Quantity must be entered.")
             return None
        try:
            quantity = int(quantity_text)
            return {"product_name": product_name, "quantity": quantity}
        except ValueError:
            QMessageBox.warning(self, self.tr["error"], "Invalid number entered.")
            return None

class StatisticsDialog(QDialog):
    def __init__(self, parent=None, sales_data=None, inventory_data=None, tr=None):
        super().__init__(parent)
        self.tr = tr if tr else LANGUAGES["עברית"]
        self.setWindowTitle(self.tr["statistics"])
        self.sales_data = sales_data if sales_data else {"sales": []}
        self.inventory_data = inventory_data if inventory_data else {"items": {}}
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()

        self.general_tab = QWidget()
        self.general_layout = QVBoxLayout(self.general_tab)
        self.general_tab.setLayout(self.general_layout)
        self.tabs.addTab(self.general_tab, self.tr["general"])

        self.sales_tab = QWidget()
        self.sales_layout = QVBoxLayout(self.sales_tab)
        self.sales_history_text = QTextEdit()
        self.sales_layout.addWidget(QLabel(self.tr["sales_history"]))
        self.sales_layout.addWidget(self.sales_history_text)
        self.sales_tab.setLayout(self.sales_layout)
        self.tabs.addTab(self.sales_tab, self.tr["sales_history"])

        self.layout.addWidget(self.tabs)
        self.populate_statistics()

    def calculate_inventory_value(self):
        total_value = 0
        for item_name, item_data in self.inventory_data["items"].items():
            total_value += item_data["quantity"] * item_data["cost"]
        return total_value

    def calculate_profit(self, start_date=None, end_date=None):
        total_profit = 0
        total_revenue = 0
        total_cost = 0
        for sale in self.sales_data["sales"]:
            sale_date = datetime.fromisoformat(sale["date"])
            if (start_date is None or sale_date >= start_date) and \
               (end_date is None or sale_date <= end_date):
                total_profit += sale["profit"]
                total_revenue += sale["sale_price"] * sale["quantity"]
                total_cost += sale["cost_per_item"] * sale["quantity"]
        return total_profit, total_revenue, total_cost

    def populate_statistics(self):
        today = datetime.now()

        daily_profit, daily_revenue, daily_cost = self.calculate_profit(today, today + timedelta(days=1))
        weekly_profit, weekly_revenue, weekly_cost = self.calculate_profit(today - timedelta(days=7), today + timedelta(days=1))
        monthly_profit, monthly_revenue, monthly_cost = self.calculate_profit(today - relativedelta(months=1), today + timedelta(days=1))
        yearly_profit, yearly_revenue, yearly_cost = self.calculate_profit(today - relativedelta(years=1), today + timedelta(days=1))
        inventory_value = self.calculate_inventory_value()

        self.general_layout.addWidget(QLabel(f"{self.tr['daily_profit']}: {daily_profit:.2f}"))
        self.general_layout.addWidget(QLabel(f"{self.tr['weekly_profit']}: {weekly_profit:.2f}"))
        self.general_layout.addWidget(QLabel(f"{self.tr['monthly_profit']}: {monthly_profit:.2f}"))
        self.general_layout.addWidget(QLabel(f"{self.tr['yearly_profit']}: {yearly_profit:.2f}"))
        self.general_layout.addWidget(QLabel(f"{self.tr['inventory_value']}: {inventory_value:.2f}"))
        self.general_layout.addWidget(QLabel(f"{self.tr['total_revenue']}: {yearly_revenue:.2f}"))
        self.general_layout.addWidget(QLabel(f"{self.tr['total_cost']}: {yearly_cost:.2f}"))
        self.general_layout.addWidget(QLabel(f"{self.tr['total_profit']}: {yearly_profit:.2f}"))

        sales_text = ""
        for sale in self.sales_data["sales"]:
            sale_date = datetime.fromisoformat(sale["date"]).strftime("%Y-%m-%d %H:%M:%S")
            sales_text += f"{self.tr['product_name']}: {sale['product']}, {self.tr['quantity']}: {sale['quantity']}, {self.tr['sale_info']}: {sale_date}, Profit: {sale['profit']:.2f}\n"
        self.sales_history_text.setPlainText(sales_text)

class CoffeeShopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.language = "עברית"
        self.tr = LANGUAGES[self.language]
        self.setWindowTitle(self.tr["title"])
        self.setGeometry(100, 100, 1200, 800)
        self.apply_modern_style()
        self.inventory = load_json(INVENTORY_FILE, {"items": {}})
        self.sales = load_json(SALES_FILE, {"sales": []})
        self.current_filter = None

        self.layout = QVBoxLayout(self)

        self.language_switch = QComboBox()
        self.language_switch.addItems(LANGUAGES.keys())
        self.language_switch.setCurrentText(self.language)
        self.language_switch.currentIndexChanged.connect(self.change_language)
        self.layout.addWidget(self.language_switch)

        self.status_label = QLabel(f"🔗 {socket.gethostname()}")
        self.status_label.setStyleSheet("color: #555; font-style: italic")
        self.layout.addWidget(self.status_label)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText(self.tr["search"])
        self.search_bar.textChanged.connect(self.refresh_table)
        self.layout.addWidget(self.search_bar)

        self.filter_layout = QHBoxLayout()
        self.indica_filter_btn = QPushButton("אינדיקה")
        self.indica_filter_btn.clicked.connect(lambda: self.set_filter("indica"))
        self.sativa_filter_btn = QPushButton("סאטיבה")
        self.sativa_filter_btn.clicked.connect(lambda: self.set_filter("sativa"))
        self.hybrid_filter_btn = QPushButton("היבריד")
        self.hybrid_filter_btn.clicked.connect(lambda: self.set_filter("hybrid"))
        self.all_filter_btn = QPushButton("הכל")
        self.all_filter_btn.clicked.connect(lambda: self.set_filter(None))
        self.filter_layout.addWidget(self.indica_filter_btn)
        self.filter_layout.addWidget(self.sativa_filter_btn)
        self.filter_layout.addWidget(self.hybrid_filter_btn)
        self.filter_layout.addWidget(self.all_filter_btn)
        self.layout.addLayout(self.filter_layout)

        self.sort_box = QComboBox()
        self.sort_box.addItems(self.tr["sort"])
        self.sort_box.currentIndexChanged.connect(self.refresh_table)
        self.layout.addWidget(self.sort_box)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(self.tr["headers"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.itemDoubleClicked.connect(self.edit_item)
        self.layout.addWidget(self.table)

        btn_row = QHBoxLayout()
        actions = [
            (self.tr["add"], self.add_product),
            (self.tr["delete"], self.delete_selected),
            (self.tr["save"], self.save_data),
            (self.tr["export"], self.export_data),
            (self.tr["sell"], self.sell_product),
            (self.tr["statistics"], self.show_statistics) # added statistics
        ]
        for text, func in actions:
            btn = QPushButton(text)
            btn.clicked.connect(func)
            btn_row.addWidget(btn)
        self.layout.addLayout(btn_row)

        self.refresh_table()

    def apply_modern_style(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f0f8ea"))
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, QColor("#e0eee0"))
        palette.setColor(QPalette.AlternateBase, QColor("#c1cdc1"))
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor("#8fbc8f"))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Highlight, QColor("#556b2f"))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        self.setPalette(palette)

        self.setStyleSheet("""
            QWidget {
                font-family: 'Arial';
                font-size: 14px;
            }
            QPushButton {
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                border: 1px solid #a9a9a9;
                background-color: #d3d3d3;
                color: black;
            }
            QPushButton:hover {
                background-color: #bebebe;
            }
            QLineEdit, QComboBox {
                padding: 7px;
                border: 1px solid #a9a9a9;
                border-radius: 4px;
                background-color: #f5f5f5;
            }
            QTableWidget {
                border: 1px solid #808080;
                background-color: #f8f8f8;
            }
            QHeaderView::section {
                background-color: #a9a9a9;
                color: white;
                padding: 4px;
                border: 1px solid #808080;
            }
            QTableWidget::item:selected {
                background-color: #add8e6;
            }
            QTabWidget::pane {
                border: 1px solid #808080;
                background-color: #f8f8f8;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background: #a9a9a9;
                color: white;
                padding: 8px 20px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                border: 1px solid #808080;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background: #f8f8f8;
                color: black;
                border-bottom: 1px solid #f8f8f8;
            }
            QTabBar::tab:hover {
                background: #bebebe;
            }
            QTextEdit {
                border: 1px solid #a9a9a9;
                border-radius: 4px;
                background-color: #f5f5f5;
            }
        """)

    def change_language(self):
        self.language = self.language_switch.currentText()
        self.tr = LANGUAGES[self.language]
        self.setWindowTitle(self.tr["title"])
        self.search_bar.setPlaceholderText(self.tr["search"])
        self.sort_box.clear()
        self.sort_box.addItems(self.tr["sort"])
        self.table.setHorizontalHeaderLabels(self.tr["headers"])
        self.refresh_table()

    def set_filter(self, product_type):
        self.current_filter = product_type
        self.refresh_table()

    def refresh_table(self):
        items = self.inventory.get("items", {})
        search = self.search_bar.text().lower()
        sort_option = self.sort_box.currentText()

        filtered_items = items
        if self.current_filter:
            filtered_items = {
                name: data for name, data in filtered_items.items()
                if data.get('type', '').lower() == self.current_filter
            }

        sorted_items = list(filtered_items.items())
        if sort_option in ["Price", "מחיר"]:
            sorted_items.sort(key=lambda x: x[1]['price'])
        elif sort_option in ["Quantity", "כמות"]:
            sorted_items.sort(key=lambda x: x[1]['quantity'])
        elif sort_option in ["Discount", "הנחה"]:
            sorted_items.sort(key=lambda x: x[1].get('discount', 0), reverse=True)

        self.table.setRowCount(0)
        for name, data in sorted_items:
            if search and search not in name.lower():
                continue
            row = self.table.rowCount()
            self.table.insertRow(row)
            name_item = QTableWidgetItem(name)
            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, QTableWidgetItem(str(data['quantity'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(data['price'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(data['cost'])))
            self.table.setItem(row, 4, QTableWidgetItem(str(int(data.get('discount', 0) * 100))))
            for col in range(1, 5):
                item = self.table.item(row, col)
                if item:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
            if data['quantity'] <= LOW_STOCK_THRESHOLD:
                self.status_label.setText(f"{self.tr['low_stock']} {name} ({data['quantity']})")
            else:
                if all(item[1]['quantity'] > LOW_STOCK_THRESHOLD for item in items.items()):
                    self.status_label.setText(f"🔗 {socket.gethostname()}")

    def edit_item(self, item):
        if item.column() in [1, 2, 3, 4]:
            row = item.row()
            col = item.column()
            product_name = self.table.item(row, 0).text()
            old_value = item.text()
            new_value, ok = QInputDialog.getText(self, "ערוך ערך", f"הזן ערך חדש עבור {self.tr['headers'][col]}:", QLineEdit.Normal, old_value)
            if ok and new_value:
                try:
                    if col == 1:
                        self.inventory['items'][product_name]['quantity'] = int(new_value)
                    elif col == 2:
                        self.inventory['items'][product_name]['price'] = float(new_value)
                    elif col == 3:
                        self.inventory['items'][product_name]['cost'] = float(new_value)
                    elif col == 4:
                         self.inventory['items'][product_name]['discount'] = float(new_value) / 100
                    self.refresh_table()
                except ValueError:
                    QMessageBox.warning(self, "שגיאה", "אנא הזן ערך מספרי תקין.")

    def add_product(self):
        dialog = AddProductDialog(self, self.tr)
        if dialog.exec():
            data = dialog.get_data()
            if data:
                self.inventory['items'][data['name']] = {
                    "quantity": data['quantity'],
                    "price": data['price'],
                    "cost": data['cost'],
                    "discount": data['discount'],
                    "type": data['type']
                }
                self.refresh_table()

    def delete_selected(self):
        selected = self.table.currentRow()
        if selected >= 0:
            name_item = self.table.item(selected, 0)
            if name_item:
                name = name_item.text()
                if name in self.inventory['items']:
                    del self.inventory['items'][name]
                    self.refresh_table()

    def save_data(self):
        save_json(self.inventory, INVENTORY_FILE)
        save_json(self.sales, SALES_FILE) #save sales too
        QMessageBox.information(self, self.tr["save"], self.tr["saved"])

    def export_data(self):
        path, _ = QFileDialog.getSaveFileName(self, self.tr["export"], "inventory.csv", "CSV Files (*.csv)")
        if path:
            df = pd.DataFrame.from_dict(self.inventory['items'], orient='index')
            df.to_csv(path)
            QMessageBox.information(self, self.tr["export"], self.tr["exported"])

    def sell_product(self):
        sell_dialog = SellDialog(self, self.inventory['items'], self.tr)
        if sell_dialog.exec():
            sale_data = sell_dialog.get_sale_data()
            if sale_data:
                product_name = sale_data['product_name']
                quantity_to_sell = sale_data['quantity']
                if product_name in self.inventory['items']:
                    if self.inventory['items'][product_name]['quantity'] >= quantity_to_sell:
                        self.inventory['items'][product_name]['quantity'] -= quantity_to_sell
                        sale_price = self.inventory['items'][product_name]['price'] * (1 - self.inventory['items'][product_name].get('discount', 0))
                        sale_cost = self.inventory['items'][product_name]['cost']
                        profit = (sale_price - sale_cost) * quantity_to_sell
                        self.sales['sales'].append({
                            "product": product_name,
                            "quantity": quantity_to_sell,
                            "sale_price": sale_price,
                            "cost_per_item": sale_cost,
                            "profit": profit,
                            "date": datetime.now().isoformat()
                        })
                        save_json(self.sales, SALES_FILE)
                        self.refresh_table()
                        QMessageBox.information(self, "מכירה", f"בוצעה מכירה של {quantity_to_sell} {product_name}!")
                    else:
                        QMessageBox.warning(self, "מלאי לא מספיק", f"אין מספיק מלאי של {product_name}.")
                else:
                    QMessageBox.critical(self, "שגיאה", "המוצר לא נמצא במלאי.")

    def show_statistics(self):
        dialog = StatisticsDialog(self, self.sales, self.inventory, self.tr)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeShopApp()
    window.show()
    sys.exit(app.exec())
