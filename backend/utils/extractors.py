import io

import docx

import pdfplumber

 

class BaseTextExtractor:

    """

    Base class for text extraction.

    Child classes should override the `extract_text` method.

    """

    def extract_text(self, file_bytes: bytes) -> str:

        raise NotImplementedError("This method should be overridden by subclasses.")

 

class PDFTextExtractor(BaseTextExtractor):

    def extract_text(self, file_bytes: bytes) -> str:

        main_text = []

        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:

            for page in pdf.pages:

                bbox = (0, 50, page.width, page.height-50) # to exclude headers and footers

                cropped_page = page.within_bbox(bbox)

                text = cropped_page.extract_text()

                if text:

                    main_text.append(text.strip())

        return "\n".join(main_text)

 

    def extract_text2(self, file_bytes: bytes) -> str:

        main_text = []

        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:

            for page in pdf.pages:

                bbox = (0, 50, page.width, page.height-50)  # to exclude headers and footers

                cropped_page = page.within_bbox(bbox)

               

                # Extract words with detailed character information

                words = cropped_page.extract_words()

               

                # Initialize a variable to track the current line

                current_line = []

                previous_bottom = None

                is_bold = False

               

                for word in words:

                    # Determine if the font is bold

                    font_name = word.get('fontname', '').lower()

                    if 'bold' in font_name or 'black' in font_name:  # Common indicators of bold fonts

                        is_bold = True

                   

                    # Determine if we're on a new line

                    bottom = word['bottom']

                    if previous_bottom is None or abs(bottom - previous_bottom) > 2:  # New line detected

                        if current_line:

                            # Join the current line and add to main_text

                            line_text = " ".join(current_line)

                            if is_bold:

                                line_text = f"**{line_text}**"

                            main_text.append(line_text.strip())

                       

                        # Reset for the new line

                        current_line = []

                        is_bold = False

                   

                    # Add the current word to the line

                    current_line.append(word['text'])

                    previous_bottom = bottom

               

                # Add the last line if any

                if current_line:

                    line_text = " ".join(current_line)

                    if is_bold:

                        line_text = f"**{line_text}**"

                    main_text.append(line_text.strip())

 

        return "\n".join(main_text)

 

class DOCXTextExtractor(BaseTextExtractor):

    def extract_text(self, file_bytes: bytes) -> str:

        text = ""

        doc = docx.Document(io.BytesIO(file_bytes))

        for para in doc.paragraphs:

            text += para.text + "\n"

        return text

 

class TXTTextExtractor(BaseTextExtractor):

    def extract_text(self, file_bytes: bytes) -> str:

        return file_bytes.decode("utf-8")