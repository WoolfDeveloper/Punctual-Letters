import os
import shutil
import zipfile

class PunctualLetterController:
    def __init__(self, to_route):
        self.export_folder = ''
        self.original_file = ''
        self.new_file = to_route
        self.bookname = ''
        self.delete_export_folder = True
        self.HTML_TAGS_TO_FILTER = ['<p', '</p', '<div', '</div', '<span', '</span']
        self.HTML_TAGS_TO_EXCLUDE = ['<img']
        self.setTempPath()

    #region Process file and paths

    def processfile(self):
        self.exportEpub()
        file_puntualized = self.PunctualLetterizerFiles()
        if file_puntualized[0]:
            self.makeEpub()
            return file_puntualized
        else:
            self.deleteExportFolder()
            return file_puntualized

    def exportEpub(self):
        self.resetTempPath()
        with zipfile.ZipFile(self.original_file, 'r') as zip_ref:
            zip_ref.extractall(self.export_folder)

    def makeEpub(self):
        with zipfile.ZipFile(self.new_file, 'w') as zip_ref:
            for root, _, files in os.walk(self.export_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.export_folder)
                    zip_ref.write(file_path, relative_path)
        if self.delete_export_folder:
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

    def resetTempPath(self):
        if os.path.exists(self.export_folder):
            self.deleteExportFolder()
        os.makedirs(self.export_folder, exist_ok=True)

    def setNewEpubPath(self, filepath):
        self.original_file = os.path.abspath(filepath)
        self.bookname = (os.path.basename(filepath)).replace('.epub', '')
        self.new_file = os.path.join(self.new_file, self.bookname + '_punctualized.epub')

    def deleteExportFolder(self):
        if os.path.exists(self.export_folder):
            shutil.rmtree(self.export_folder)
        return True

    #endregion

    #region Punctualize all text

    def PunctualLetterizerFiles(self):
        files = [os.path.join(root, file) for root, _, files in os.walk(self.export_folder) for file in files
                if file.endswith(('.html', '.xhtml', '.htm'))]

        if len(files) == 0:
            return [False, 'err.file_empty']

        cssfiles = [os.path.join(root, file) for root, _, files in os.walk(self.export_folder) for file in files
                if file.endswith('.css')]
        self.putBoldStyles(cssfiles)

        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if 'Punctualized by Punctual Letters' in lines[-1]:
                    return [False, 'err.file_processed']
            with open(file, 'w', encoding='utf-8') as f:
                for line in lines:
                    if (self.filterByTags(line) and self.excludeByTags(line)) or '<' not in line:
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
        return [True, 'succ.epub_processed']

    def filterByTags(self, line):
        for tag in self.HTML_TAGS_TO_FILTER:
            if tag in line:
                return True
        return False

    def excludeByTags(self, line):
        for tag in self.HTML_TAGS_TO_EXCLUDE:
            if tag in line:
                return False
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

    #endregion

    #region Sort and tags

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
        else:
            if '\n' in line and not '\\' == line[0]:
                line_splitted = line.split('\n')
                new_line_splitted = []
                for segment in line_splitted:
                    if segment != '':
                        new_line_splitted.append(segment + '|supermegatext')
                    else:
                        new_line_splitted.append('\n')
                line_splitted = new_line_splitted
            else:
                line_splitted = line + '|supermegatext'
        return line_splitted

    #endregion

