import pandas as pd
import re

# Function to remove emojis and special characters
def clean_comment(comment):
    # Remove emojis and unwanted special characters
    comment = re.sub(r'[^\w\sàáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]', '', comment)
    return comment.strip()

# Function to replace common Vietnamese slang/acronyms
def fix_vietnamese_typo(comment):
    slang_dict = {
        "ko": "không",
        "k": "không",
        "kg": "không",
        "khg": "không",
        "hok": "không",
        "ns": "nói",
        "j": "gì",
        "dc": "được",
        "nhg": "nhưng",
        "mik": "mình",
        "bt": "bình thường",
        "mn": "mọi người",
        "mng": "mọi người",
        "đc": "được",
        "sp": "sản phẩm",
        "ms": "mới",
        "vs": "và",
        "s": "sao",
        "v": "vậy",
        "nt": "nhắn tin"
    }
    for slang, full_word in slang_dict.items():
        comment = re.sub(rf'\b{slang}\b', full_word, comment, flags=re.IGNORECASE)
    return comment

# Load the scraped Excel file
file_path = "lazada_comments.xlsx"
data = pd.read_excel(file_path)

# Drop empty rows (if not already handled in Excel)
data = data.dropna(subset=["Comment"])

# Clean the 'Comment' column
data["Comment"] = data["Comment"].apply(clean_comment)
data["Comment"] = data["Comment"].apply(fix_vietnamese_typo)

# Save the cleaned data back to an Excel file
cleaned_file_path = "lazada_comments.xlsx"
data.to_excel(cleaned_file_path, index=False)

print(f"Cleaning completed! Cleaned file saved as '{cleaned_file_path}'.")
