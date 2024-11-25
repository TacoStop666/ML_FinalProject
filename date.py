import pandas as pd
import csv

# 檔案名稱
input_file = "output.csv"  # 原始文件名稱
output_file = "cleaned_output.csv"  # 修復後的文件名稱
target_date = "2024-11-25"  # 設定目標日期

# 清理並修復文件
def clean_csv(input_file, output_file, expected_fields=9):
    """
    修復 CSV 文件中行數不匹配的問題，並儲存乾淨的輸出文件。
    """
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        header = next(reader)  # 讀取標題行
        if len(header) != expected_fields:
            print("標題行字段數與預期不符，請確認文件格式！")
            return
        
        writer.writerow(header)  # 寫入標題行
        
        for i, row in enumerate(reader, start=2):  # 從第二行開始檢查
            if len(row) == expected_fields:
                writer.writerow(row)
            else:
                print(f"跳過第 {i} 行：字段數不匹配 -> {row}")

    print(f"清理完成！修復後的文件已儲存到：{output_file}")

# 讀取並處理文件
def process_csv(output_file, target_date):
    """
    讀取修復後的 CSV 文件，計算每行與目標日期的天數差異。
    """
    # 將目標日期轉換為 datetime
    target_date = pd.to_datetime(target_date, format='%Y-%m-%d')
    
    # 讀取清理後的 CSV 文件
    df = pd.read_csv(output_file)
    
    # 確保 `upload time` 欄位為 datetime 格式
    df['upload time'] = pd.to_datetime(df['upload time'], format='%Y-%m-%dT%H:%M:%S.%fZ', errors='coerce')
    
    # 計算天數差距
    df['days_diff'] = (target_date - df['upload time']).dt.days
    
    # 將結果儲存回 CSV
    result_file = "processed_output.csv"
    df.to_csv(result_file, index=False)
    print(f"處理完成！結果已儲存到：{result_file}")

# 執行流程
if __name__ == "__main__":
    clean_csv(input_file, output_file)
    process_csv(output_file, target_date)
