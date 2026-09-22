import requests
def fetch_unique_columns(USER_PROMPT):
    SYSTEM_PROMPT= """You are a data-quality analyst specializing in database and tabular data semantics.
Your task is to identify ALL columns that are independently intended to contain a unique value for each record or entity represented by a row.
Analyze all of the following:
- filename
- table_type
- column_names
IMPORTANT:
A table can have MORE THAN ONE column that is required to be unique.
Do not stop after finding one unique column.
Evaluate EVERY column independently and return ALL columns whose uniqueness requirement is nearly certain from the table context.
For each column, ask:
"Does this column independently identify the entity represented by this row, such that two different records/entities normally should not have the same value?"
If YES with very high certainty, include the column.
If NO, do not include it.
If UNCERTAIN, do not include it.
Do not artificially limit the number of unique columns.
Distinguish between an identifier of the entity represented by the row and an identifier referring to another entity.
Example:
Orders table:
order_id
customer_id
product_id
order_date
Return order_id.
Do not return customer_id or product_id because many orders can belong to the same customer or contain the same product.
A table MAY have several independently unique identifiers.
Example:
User Account table:
user_id
username
email
first_name
last_name
If the context clearly indicates that user_id, username, and email are all independent account identifiers that must be unique, return:
{"unique_columns":["user_id","username","email"]}
Do not automatically assume username or email is unique.
Common identifiers that MAY be unique when supported by context include:
id, ID, entity_id, user_id, student_id, employee_id, patient_id, order_id, invoice_id, transaction_id, prescription_id, account_number, registration_number, roll_number, admission_number, membership_number, employee_number, invoice_number, order_number, transaction_number, serial_number, SKU, sku, username.
Do not return a column merely because its name looks like an identifier.
Do not automatically return foreign/reference identifiers.
Examples:
Customer Orders:
order_id
customer_id
product_id
salesperson_id
Return only order_id.
Bank Transactions:
transaction_id
account_id
customer_id
Return only transaction_id.
Student Records:
student_id
registration_number
student_name
age
department
If both student_id and registration_number independently identify the student, return both.
Product Catalog:
product_id
sku
product_name
category
price
If both product_id and SKU independently identify the product, return both.
Invoice Records:
invoice_id
invoice_number
customer_id
amount
If both invoice_id and invoice_number identify the invoice itself, return both.
Do not normally return ordinary descriptive or demographic columns such as:
name, first_name, last_name, gender, age, country, city, address, phone, date, salary, department, category, description, price, quantity, status, diagnosis.
Do not automatically assume email, username, or phone is unique. Include them only when the table context strongly indicates that they independently identify the entity.
Do not determine intended uniqueness merely from current values. A column is unique because of its intended role, not because current values happen to be different.
Do not return composite uniqueness. If uniqueness is achieved only by combining multiple columns, do not mark those individual columns as independently unique.
You MUST evaluate every column in column_names.
A table may have 0, 1, 2, 3, or more independently unique columns.
Precision is important, but do not skip a column merely because another column is a stronger identifier.
Use filename, table_type, and all column_names together.
If the meaning of a column is ambiguous, do not include it.
Return ONLY valid JSON.
The output must contain exactly one field:
{"unique_columns":[]}
The array must contain only exact column names from the input.
Do not modify column names.
Do not add explanations, reasons, confidence scores, or additional fields.
Do not return Markdown.
Do not use ```json.
Do not use ```.
Do not return any text before or after the JSON.
Example:
Input:
{"filename":"students.xlsx","table_type":"Student Records","column_names":["student_id","registration_number","student_name","age","department"]}
Output:
{"unique_columns":["student_id","registration_number"]}
Example:
Input:
{"filename":"orders.xlsx","table_type":"E-commerce Order Records","column_names":["order_id","customer_id","product_id","order_date","quantity"]}
Output:
{"unique_columns":["order_id"]}
Example:
Input:
{"filename":"products.xlsx","table_type":"Product Catalog","column_names":["product_id","sku","product_name","category","price"]}
Output:
{"unique_columns":["product_id","sku"]}
Example:
Input:
{"filename":"accounts.xlsx","table_type":"User Account Records","column_names":["user_id","username","email","first_name","last_name"]}
Output:
{"unique_columns":["user_id","username","email"]}
If no column is sufficiently certain to be independently unique:
{"unique_columns":[]}"""
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "gemma4:e4b",
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": str(USER_PROMPT)
                    }
                ],
                "stream": False,

            }
        )
        result = response.json()
        answer = result["message"]["content"]
        return answer

    except Exception:
        print("Error during calling of LLM for uniqueness")
        raise
