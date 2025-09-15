import pandas as pd
import json
from datetime import datetime
import os

class ReceiptDataProcessor:
    
    def __init__(self, json_file_path):
        
        self.json_file_path = json_file_path
        self.data = None
        self.receipts = []
        
    def load_data(self):
        try:
            with open(self.json_file_path, 'r') as f:
                self.data = json.load(f)
            
            if 'receipts' in self.data:
                self.receipts = self.data['receipts']
            else:
                print("No receipts found in the JSON data")
                return False
            return True
        except FileNotFoundError:
            print(f"File {self.json_file_path} not found")
            return False
        except json.JSONDecodeError:
            print(f"Invalid JSON in {self.json_file_path}")
            return False
    
    def extract_merchant_info(self):
        merchant_data = []
        
        for receipt in self.receipts:
            merchant_info = {
                'merchant_name': receipt.get('merchant_name', ''),
                'merchant_address': receipt.get('merchant_address', ''),
                'merchant_phone': receipt.get('merchant_phone', ''),
                'merchant_website': receipt.get('merchant_website', ''),
                'city': receipt.get('city', ''),
                'state': receipt.get('state', ''),
                'zip': receipt.get('zip', ''),
                'country': receipt.get('country', ''),
                'receipt_no': receipt.get('receipt_no', ''),
                'date': receipt.get('date', ''),
                'time': receipt.get('time', ''),
                'total': receipt.get('total', 0),
                'currency': receipt.get('currency', ''),
                'payment_method': receipt.get('payment_method', ''),
                'ocr_confidence': receipt.get('ocr_confidence', 0)
            }
            merchant_data.append(merchant_info)
        
        return pd.DataFrame(merchant_data)
    
    def extract_items(self):
        items_data = []
        
        for receipt in self.receipts:
            merchant_name = receipt.get('merchant_name', '')
            receipt_date = receipt.get('date', '')
            receipt_time = receipt.get('time', '')
            
            for item in receipt.get('items', []):
                item_info = {
                    'merchant_name': merchant_name,
                    'receipt_date': receipt_date,
                    'receipt_time': receipt_time,
                    'description': item.get('description', ''),
                    'amount': item.get('amount', 0),
                    'quantity': item.get('qty', ''),
                    'unit_price': item.get('unitPrice', ''),
                    'category': item.get('category', ''),
                    'flags': item.get('flags', ''),
                    'remarks': item.get('remarks', ''),
                    'tags': item.get('tags', '')
                }
                items_data.append(item_info)
        
        return pd.DataFrame(items_data)
    
    def create_summary_stats(self):
        if not self.receipts:
            return pd.DataFrame()
        
        total_receipts = len(self.receipts)
        total_amount = sum(receipt.get('total', 0) for receipt in self.receipts)
        avg_amount = total_amount / total_receipts if total_receipts > 0 else 0
        
        total_items = sum(len(receipt.get('items', [])) for receipt in self.receipts)
        
        dates = [receipt.get('date', '') for receipt in self.receipts if receipt.get('date')]
        min_date = min(dates) if dates else ''
        max_date = max(dates) if dates else ''
        
        merchants = set(receipt.get('merchant_name', '') for receipt in self.receipts)
        unique_merchants = len(merchants)
        
        summary_data = {
            'Metric': [
                'Total Receipts',
                'Total Amount',
                'Average Amount per Receipt',
                'Total Items',
                'Unique Merchants',
                'Date Range (From)',
                'Date Range (To)',
                'Processing Date'
            ],
            'Value': [
                total_receipts,
                f"${total_amount:.2f}",
                f"${avg_amount:.2f}",
                total_items,
                unique_merchants,
                min_date,
                max_date,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
        }
        
        return pd.DataFrame(summary_data)
    
    def export_to_excel(self, output_file='receipt_analysis.xlsx'):
        if not self.load_data():
            return False
        
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                summary_df = self.create_summary_stats()
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                merchant_df = self.extract_merchant_info()
                merchant_df.to_excel(writer, sheet_name='Merchants', index=False)
                
                items_df = self.extract_items()
                items_df.to_excel(writer, sheet_name='Items', index=False)
                
                ocr_texts = []
                for receipt in self.receipts:
                    ocr_texts.append({
                        'merchant_name': receipt.get('merchant_name', ''),
                        'receipt_date': receipt.get('date', ''),
                        'ocr_text': receipt.get('ocr_text', ''),
                        'confidence': receipt.get('ocr_confidence', 0)
                    })
                
                if ocr_texts:
                    ocr_df = pd.DataFrame(ocr_texts)
                    ocr_df.to_excel(writer, sheet_name='OCR_Text', index=False)
            
            print(f"Excel file exported successfully: {output_file}")
            return True
            
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return False
    
    def export_to_csv(self, output_dir='csv_exports'):
        if not self.load_data():
            return False
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            summary_df = self.create_summary_stats()
            summary_df.to_csv(f'{output_dir}/summary.csv', index=False)
            
            merchant_df = self.extract_merchant_info()
            merchant_df.to_csv(f'{output_dir}/merchants.csv', index=False)
            
            items_df = self.extract_items()
            items_df.to_csv(f'{output_dir}/items.csv', index=False)
            
            print(f"CSV files exported successfully to {output_dir}/")
            return True
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False

def main():
    processor = ReceiptDataProcessor('result1.json')
    
    print("Exporting to Excel...")
    processor.export_to_excel('receipt_analysis.xlsx')
    
    print("Exporting to CSV...")
    processor.export_to_csv('csv_exports')
    
    print("Data processing complete!")

if __name__ == "__main__":
    main()
