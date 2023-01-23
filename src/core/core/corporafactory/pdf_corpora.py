
from fpdf import FPDF, HTMLMixin
import random
from datetime import datetime
import os, sys
from pathlib import Path
from faker import Faker

import os, sys
import asyncio
from pathlib import Path

currentDir = os.path.dirname(Path(__file__))
sys.path.insert(0, currentDir)
core_core_dir = os.path.dirname(Path(__file__).parent)
sys.path.insert(0, core_core_dir)
models_dir = os.path.join(os.path.dirname(Path(__file__).parent), 'models')
sys.path.insert(0, models_dir)
import io

from eventstore import EventStore

class CustomFPDF(FPDF, HTMLMixin):
    pass

class PDFCorpora():
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PDFCorpora, cls).__new__(cls)
        return cls.instance
    
    
    def __init__(self) -> None:
        
        self.es = EventStore()
        
        self.data = []
        
        self.faker = Faker()
        
    def load_corpora(self, size=5000):
        if len(self.data) > 0:
            return
        
        for i in range(size):
            
            pdf = self.create_pdf()
            self.data.append(pdf)
        
        
    def next_corpora(self) -> bytearray:
        
        if len(self.data) == 0:
            return None
        
        randIdx = random.randint(0, len(self.data) - 1)
        
        return self.data[randIdx]
    
    # fpdf output doc
    # http://www.fpdf.org/en/doc/output.htm
    def create_pdf(self):
        
        
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>

                <!-- Declared Vars To Go Here -->

                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1">

                <!-- Metadata -->
                <meta name="description" content="">
                <meta name="author" content="">

                <link rel="icon" href="mysource_files/favicon.ico">

                <!-- Page Name and Site Name -->
                <title>Page Name - Squiz Matrix HTML Example</title>

                <!-- CSS -->
                <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
                <link href="mysource_files/style.css" rel="stylesheet">

            </head>

            <body>

                <div class="container">

                <header class="header clearfix" style="background-color: #ffffff">

                    <!-- Main Menu -->
                    <nav>
                    <ul class="nav nav-pills pull-right">
                        <li class="active"><a href="#">Home</a></li>
                        <li><a href="#">About</a></li>
                        <li><a href="#">Contact</a></li>
                    </ul>
                    </nav>

                    <!-- Site Name -->
                    <h1 class="h3 text-muted">Site Name</h1>

                    <!-- Breadcrumbs -->
                    <ol class="breadcrumb">
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Level 1</a></li>
                    <li class="active">Level 2</li>
                    </ol>

                </header>

                <div class="page-heading">

                    <!-- Page Heading -->
                    <h1>Page Heading</h1>

                </div>

                <div class="row">

                    <div class="col-sm-3">

                    <!-- Sub Navigation -->
                    <ul class="nav nav-pills nav-stacked">
                        <li><a href="#">Level 2</a></li>
                        <li class="active"><a href="#">Level 2</a>
                        <ul>
                            <li><a href="#">{self.faker.name()}</a></li>
                            <li><a href="#">{self.faker.job()}</a></li>
                            <li><a href="#">{self.faker.address()}</a></li>
                        </ul>
                        </li>
                        <li><a href="#">Level 2</a></li>
                    </ul>

                    </div>

                    <div class="col-sm-6">

                    <div class="page-contents">

                        <!-- Design Body -->
                        <h2>Info</h2>
                        <p>{self.faker.name()} {self.faker.address()} {self.faker.phone_number()}</p>
                        <h4>Info</h4>
                        <p>{self.faker.name()} {self.faker.address()} {self.faker.phone_number()}</p>
                        <h4>Info</h4>
                        <p>{self.faker.name()} {self.faker.address()} {self.faker.phone_number()}</p>

                    </div>

                    </div>

                    <div class="col-sm-3">

                    <!-- Login Section -->
                    <h2>Login</h2>

                    <!-- Search Section -->
                    <h2>Search</h2>

                    <!-- Nested Right Column Content -->

                    </div>

                </div>

                <footer class="footer">
                    <p class="pull-right">
                    <!-- Last Updated Design Area-->
                    Last Updated: Wednesday, January 6, 2016
                    </p>
                    <p>&copy; 2016 Company, Inc.</p>
                </footer>

                </div> <!-- /container -->

            </body>
            </html>
            '''
       
        pdf = CustomFPDF()
        pdf.add_page()
        pdf.author = 'Fuzzie'
        
        pdf.write_html(html)
        
        byteStr = pdf.output(dest='S').decode('latin-1')
       
        return byteStr
    
    def currDir(self):
        
        
        cDir = os.path.dirname(Path(__file__))
        return cDir
        
        
        
    