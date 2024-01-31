import os
from dotenv import load_dotenv
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential

def analyze_invoice(form_recognizer_client, file_path, invoice_total):
    with open(file_path, "rb") as f:
        form_data = f.read()
    # Need to determine which method to send the form to
    task = form_recognizer_client.begin_recognize_invoices(form_data)
    analyzed_result = task.result()
    for receipt in analyzed_result:
        for name, field in receipt.fields.items():
            if name == "VendorName":
                print("Vendor Name: '{}'".format(field.value))
            if name == "InvoiceTotal":
                if field.value is not None:
                    print("Invoice Total: '{}' with a confidence score of '{}'".format(
                        field.value, field.confidence))
                    if field.confidence >= ##: # replace ## with confidence lower limit for ex-------> 90% then 0.90
                        invoice_total+=field.value

    return invoice_total


def main():
    try:
        # Get configuration settings
        load_dotenv()
        form_endpoint = os.getenv('FORM_ENDPOINT')
        form_key = os.getenv('FORM_KEY')
        # Create client using endpoint and key
        form_recognizer_client = FormRecognizerClient(
            form_endpoint, AzureKeyCredential(form_key))
        # Analyze all files in the folder
        folder_path = r"...................." # replace ............. with test folder path
        invoice_total = 0
        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(folder_path, filename)
                print("Analyzing file: {}".format(file_path))
                invoice_total = analyze_invoice(form_recognizer_client, file_path, invoice_total)
        print("\nTotal Invoice Amount: {}".format(invoice_total))
    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    main()




#  Note >>>>>>>>>>> 
# .env folder is present in then assign it with end_point url and key value use string format only..
