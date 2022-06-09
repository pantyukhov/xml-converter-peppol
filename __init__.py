from flask import Flask, render_template, request, send_file
import xml.etree.ElementTree as ET
import src.convert as convert

# Create the application.
app = Flask(__name__)


# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    The home page for our application.
    """
    # Create a homepage with as centered title "Distribib" Underneath the title, display a centered text "Upload je
    # peppol xml file om het te converteren naar het juiste formaat." Underneath the text, display a centered file
    # upload input. Next to the input, display a button "Converteren"

    return render_template('home.html')


@app.route('/uploader', methods=['POST'])
def upload_file():
    """
    Get multipart file from the form
    :return: converted file
    """
    print(request.files)
    # Get the file as xml from the request
    file = request.files['file']
    # Convert file to elementtree
    xml = ET.fromstring(file.read())
    # Convert the xml to peppol xml
    converted_xml = convert.create_invoice_elementtree(xml, "0478693713")
    # Convert converted xml to file
    converted_file = ET.tostring(converted_xml)
    # Write converted_file to an xml file
    with open("converted.xml", "wb") as f:
        f.write(converted_file)
    # Return the converted xml
    return send_file('src/converted.xml', mimetype='text/xml', download_name='converted.xml', as_attachment=True)


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run()
