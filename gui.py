import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QHeaderView
from scraper_engine import NewsScraper

class NewsGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplikasi Scraping Berita")
        self.setGeometry(200,200,950,650)

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25,25,25,25)

        # ===== TITLE =====
        title = QLabel("News Web Scraper")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
        font-size:26px;
        font-weight:bold;
        color:#333;
        """)
        layout.addWidget(title)

        #INI INPUT URL BERITA
        url_layout = QHBoxLayout()

        url_label = QLabel("URL Berita:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Masukkan URL halaman berita...")

        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)

        #INI INPUT LIMIT BERITA
        limit_layout = QHBoxLayout()

        limit_label = QLabel("Limit Berita:")
        self.limit_input = QSpinBox()
        self.limit_input.setRange(1,100)
        self.limit_input.setValue(10)

        limit_layout.addWidget(limit_label)
        limit_layout.addWidget(self.limit_input)

        #INI INPUT TANGGAL BERITA (DIFILTER BERDASARKAN TANGGAL)
        date_layout = QHBoxLayout()

        start_label = QLabel("Start Date:")
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate())

        end_label = QLabel("End Date:")
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())

        date_layout.addWidget(start_label)
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(end_label)
        date_layout.addWidget(self.end_date)

        #INI BUTTON START DAN EXPORT
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start Scraping")
        self.export_button = QPushButton("Export CSV")

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.export_button)

        #INI LIAT PROGRESSNYA
        self.progress = QProgressBar()
        self.progress.setValue(0)

        #INI TABEL HASIL SCRAPING
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "Judul",
            "Tanggal",
            "Isi Berita"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #SUSUN LAYOUT 
        layout.addLayout(url_layout)
        layout.addLayout(limit_layout)
        layout.addLayout(date_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.progress)
        layout.addWidget(self.table)

        self.setLayout(layout)

        #INI STYLE SHEET biar estetik aja
        self.setStyleSheet("""

        QWidget{
            background-color:#b0b8d7;
            font-size:14px;
        }

        QLineEdit, QSpinBox, QDateEdit{
            padding:6px;
            border:1px solid #ccc;
            border-radius:5px;
            background:white;
        }

        QPushButton{
            background-color:#7596cb;
            color:white;
            font-weight:bold;
            padding:8px;
            border-radius:6px;
        }

        QPushButton:hover{
            background-color:#5a7bb8;
        }

        QTableWidget{
            background:white;
            border:1px solid #ddd;
        }

        QHeaderView::section{
            background:#eaeaea;
            font-weight:bold;
            padding:6px;
        }

        QProgressBar{
            border:1px solid #ccc;
            border-radius:6px;
            text-align:center;
        }

        QProgressBar::chunk{
            background-color:#4CAF50;
        }

        """)

        # ===== CONNECT BUTTON =====
        self.start_button.clicked.connect(self.start_scraping)
        self.export_button.clicked.connect(self.export_data)


    # ===== FUNCTION START =====
    def start_scraping(self):
    
        url = self.url_input.text()
        limit = self.limit_input.value()

        print("Start scraping:", url)

        scraper = NewsScraper()

        links = scraper.get_article_links(url, max_links=limit)

        data = []

        for i, link in enumerate(links):

            article = scraper.extract_article_data(link)

            if article:
                data.append(article)

            progress = int((i+1)/len(links)*100)
            self.progress.setValue(progress)

        scraper.close()

        self.table.setRowCount(len(data))

        for row, item in enumerate(data):

                self.table.setItem(row,0,QTableWidgetItem(item["judul"]))
                self.table.setItem(row,1,QTableWidgetItem(item["tanggal"]))
                self.table.setItem(row,2,QTableWidgetItem(item["isi"]))

    # ===== EXPORT =====
    def export_data(self):
        print("Export CSV diklik")


app = QApplication(sys.argv)

window = NewsGUI()
window.show()

sys.exit(app.exec_())
