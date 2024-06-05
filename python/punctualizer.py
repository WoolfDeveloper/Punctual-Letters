import os
import shutil
import zipfile
import PyPDF2
from textblob import TextBlob

class PunctualLetterController:
    def __init__(self, to_route):
        self.export_folder = ''
        self.original_file = ''
        self.new_file = to_route
        self.bookname = ''
        self.delete_export_folder = True
        self.setTempPath()

    def processfile(self):
        self.exportEpub()
        file_puntualized = self.PunctualLetterizerFiles()
        if file_puntualized:
            return self.makeEpub()
        else:
            self.deleteExportFolder()
            return False

    def exportEpub(self):
        with zipfile.ZipFile(self.original_file, 'r') as zip_ref:
            zip_ref.extractall(self.export_folder)

    def makeEpub(self):
        with zipfile.ZipFile(self.new_file, 'w') as zip_ref:
            for root, _, files in os.walk(self.export_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.export_folder)
                    zip_ref.write(file_path, relative_path)
        self.deleteExportFolder()
        return True

    def addFolderToZip(self, folder, zip_ref, base_path=''):
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder)
                if os.path.isdir(file_path):
                    zip_ref.write(file_path, relative_path)
                    self.addFolderToZip(file_path, zip_ref, os.path.join(base_path, file))
                else:
                    zip_ref.write(file_path, os.path.join(base_path, file))

    def setTempPath(self):
        script_dir = os.path.dirname(__file__)
        self.export_folder = os.path.join(script_dir, '.temp')
        os.makedirs(self.export_folder, exist_ok=True)

    def setNewEpubPath(self, filepath):
        self.original_file = os.path.abspath(filepath)
        self.bookname = (os.path.basename(filepath)).replace('.epub', '')
        self.new_file = os.path.join(self.new_file, self.bookname + '_punctualized.epub')

    def PunctualLetterizerFiles(self):
        files = [os.path.join(root, file) for root, _, files in os.walk(self.export_folder) for file in files
                if file.endswith(('.html', '.xhtml', '.htm'))]

        if len(files) == 0:
            #TODO: Poner mensajes de error como err.processed o err.file_null
            return False

        cssfiles = [os.path.join(root, file) for root, _, files in os.walk(self.export_folder) for file in files
                if file.endswith('.css')]
        self.putBoldStyles(cssfiles)

        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if 'Punctualized by Punctual Letters' in lines[-1]:
                    return False
            with open(file, 'w', encoding='utf-8') as f:
                for line in lines:
                    if '<p' in line and '<img' not in line:
                        line_separated = self.separateTagsFromText(line)
                        new_line = []
                        idx = 0
                        for segment in line_separated:
                            if '|tag' in segment:
                                if ',' in line_separated[idx + 1][0] or '.' in line_separated[idx + 1][0]:
                                    new_line.append(segment.replace('|tag', ''))
                                else:
                                    new_line.append(segment.replace('|tag', ' '))
                            if '|supermegatext' in segment:
                                segment = segment.replace('|supermegatext', '')
                                new_line.append(self.punctualizeText(segment))
                            if '\n' in segment:
                                new_line.append(segment)
                            idx += 1
                        line = ''.join(new_line)

                    f.write(line)
                f.write('\n<!-- Punctualized by Punctual Letters -->\n')
        return True

    def punctualizeText(self, text):
        text_exploded = text.split()
        for idx, word in enumerate(text_exploded):
            if not '&' in word:
                if len(word) <= 3:
                    formatted_word = '<b>' + word[:1] + '</b>' + word[1:]
                elif len(word) <= 5:
                    formatted_word = '<b>' + word[:2] + '</b>' + word[2:]
                elif len(word) <= 7:
                    formatted_word = '<b>' + word[:3] + '</b>' + word[3:]
                elif len(word) <= 9:
                    formatted_word = '<b>' + word[:4] + '</b>' + word[4:]
                elif len(word) <= 11:
                    formatted_word = '<b>' + word[:5] + '</b>' + word[5:]
                elif len(word) <= 13:
                    formatted_word = '<b>' + word[:6] + '</b>' + word[6:]
                else:
                    formatted_word = '<b>' + word[:7] + '</b>' + word[7:]
                text_exploded[idx] = formatted_word
        text_joined = ' '.join(text_exploded)
        return text_joined

    def putBoldStyles(self, cssfiles):
        for cssfile in cssfiles:
            with open(cssfile, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            with open(cssfile, 'w', encoding='utf-8') as f:
                for line in lines:
                    f.write(line)
                f.write('\nb { font-weight: bold !important; }\n')

    def separateTagsFromText(self, line):
        if '<' in line:
            line_splitted = line.split('>')
            new_line_splitted = []
            for segment in line_splitted:
                segment = segment.lstrip()
                from_closing_tag = False
                if not '|tag' in segment and not '' == segment:
                    if '<' in segment[0] and not '\n' in segment:
                        segment = segment + '>|tag'
                    elif '</' in segment:
                        segment = segment + '|clossingtag'
                        segmentDivided = segment.split('</')
                        mini_idx = 0
                        for microsegment in segmentDivided:
                            if '|clossingtag' in microsegment:
                                microsegment = microsegment.replace('|clossingtag', '')
                                if not '>' in microsegment or not '|tag' in microsegment:
                                    microsegment = '</' + microsegment + '>|tag'
                                else:
                                    microsegment = '</' + microsegment
                                segment = microsegment
                                from_closing_tag = True
                            else:
                                if '<' in microsegment:
                                    text, tag = microsegment.split('<', 1)
                                    new_line_splitted.append(text + '|supermegatext')
                                    new_line_splitted.append('<' + tag + '>|tag')
                                if microsegment != '':
                                    segmentDivided[mini_idx] = microsegment + '|supermegatext'
                                new_line_splitted.append(segmentDivided[mini_idx])
                            mini_idx += 1
                    elif '<' in segment:
                        text, tag = segment.split('<', 1)
                        new_line_splitted.append(text + '|supermegatext')
                        new_line_splitted.append('<' + tag + '>|tag')
                if ('|tag' in segment and not '|tag' in new_line_splitted) or from_closing_tag:
                    new_line_splitted.append(segment)
            if '\n' in line_splitted[-1] and not '\n' in new_line_splitted[-1]:
                new_line_splitted.append('\n')
            line_splitted = new_line_splitted
        return line_splitted
    
    def deleteExportFolder(self):
        if os.path.exists(self.export_folder):
            shutil.rmtree(self.export_folder)
        return True

class PunctualLetterPDFController:
    def __init__(self, to_route):
        self.export_folder = ''
        self.original_file = 'test_pdf.pdf'
        self.new_file = to_route
        self.bookname = ''
        self.delete_export_folder = True

    def process_pdf(self):
        with open(self.original_file, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)
            new_text = ''
            
            for page_num in range(num_pages):
                current_page = pdf_reader.pages[page_num]
                text = current_page.extract_text()
                for line in text.splitlines():
                    text_blob = TextBlob(line)
                    modified_line = ''
                    for word in text_blob.words:
                        modified_word = f"**{word[:2]}**"
                        modified_line += modified_word + ' '
                    modified_line = modified_line[:-1]
                    new_text += modified_line + '\n'
                new_text += '\n'

        with open(self.new_file, 'wb') as f:
            pdf_writer = PyPDF2.PdfWriter()
            new_page = pdf_writer.add_blank_page()
            new_page.set_text(new_text)
            pdf_writer.write(f)

#controller = PunctualLetterPDFController('modified_pdf.pdf')
#controller.process_pdf()



