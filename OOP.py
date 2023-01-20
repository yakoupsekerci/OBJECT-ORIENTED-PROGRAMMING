"""
Created on Fri Jan 13 21:18:22 2023

@author: yakou
"""
import sqlite3
from datetime import datetime
import pandas as pd

def get_date():
    global date
    date = input("Lütfen satış tarihini girin (YYYY-MM-DD): ")
    date = datetime.strptime(date, "%Y-%m-%d")
    return date

def main_menu():
    print("Ana Menü")
    print("1. Müşteri İşlemleri ")
    print("2. Satış İşlemleri")

    print("0. Çıkış")
    choice = input("Seçiminiz: ")
    return choice

def satislar():
    print("Satış İşlemleri Menüsü")
    print("1. Günlük Satışlar")
    print("2. Cari Hesap Ekstresi Çıkar")
    print("9. Ana Menüye Dön")
    choice = input("Seçiminiz: ")
    return choice

def menu():
    print("Müşteri İşlemleri Menüsü")
    print("1. Müşteri Ekle")
    print("2. Müşteri Listele")
    print("3. Müşteri Sil")
    print("4. Müşteri Düzenle")
    print("5. Raporu Güncelle")
    print("6. Müşteri Raporu Al")
    print("7. Müşteri Ara")
    print("8. Tarih Değiştir")
    print("9. Ana Menüye Dön")
    choice = input("Seçiminiz: ")
    return choice

def create_connection():
    conn = sqlite3.connect('customers.db')
    return conn

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, price REAL, debt REAL,date date)''')
    conn.commit()
    conn.close()

create_table()

"""
C U S T O M E R     O P E R A T İ O N S
"""
def add_customer():
    conn = create_connection()
    c = conn.cursor()
    id = int(input("Müşteri ID: "))
    c.execute(f"SELECT * FROM customers WHERE id='{id}'")
    result = c.fetchone()
    if result:
        print("*******************************************************************")
        print("Bu ID'ye ait bir müşteri zaten var. Lütfen farklı bir ID girin.")
        print("*******************************************************************")
    else:
        name = input("Müşteri Unvanı: ")
        price = float(input("Alış Fiyatı: "))
        c.execute(f"INSERT INTO customers (id, name, price, debt, date) VALUES('{id}', '{name}', '{price}', '0', '{date}')")
        conn.commit()
        print("***************************************************************************************************************")
        print(f"Müşteri {name} başarıyla eklendi!. Raporu Güncellemeyi Unutmayın. Rapor Açıkken Raporu Güncelleyemezsin.")
        print("**************************************************************************************************************")
    conn.close()
    
def list_customers():
    conn = sqlite3.connect('customers.db')
    df = pd.read_sql_query("SELECT * FROM customers", conn)
    print(df)
    
def export_customers_to_excel():
    conn = sqlite3.connect('customers.db')
    query = "SELECT * FROM customers"
    df = pd.read_sql_query(query, conn)
    df.to_excel("customers.xlsx", index=False)
    writer = pd.ExcelWriter('customers.xlsx', engine='xlsxwriter')

    df.to_excel(writer, index=False)
    worksheet = writer.sheets['Sheet1']
    for i, col in enumerate(df.columns):
        series = df[col]
        max_len = max((
        series.astype(str).map(len).max(),
        len(str(series.name))
        )) + 1
        worksheet.set_column(i, i, max_len)

# Değişiklikleri kaydetme
    writer.save()
    print("********************************************************")
    print("Rapor kayıtları güncellendi.")
    print("********************************************************")
    conn.close()

def select_customer():
    conn = sqlite3.connect("customers.db")
    c = conn.cursor()
    
    c.execute("SELECT id, name FROM customers")
    customers = c.fetchall()
    for customer in customers:
        print(customer[0], customer[1])
    
    selected_id = int(input("Lütfen bilgilerinizi görmek istediğiniz müşterinin numarasını girin: "))
    c.execute(f"SELECT * FROM customers WHERE id={selected_id}")
    selected_customer = c.fetchone()
    if selected_customer:
        print("ID:", selected_customer[0])
        print("Unvan:", selected_customer[1])
        print("Alış Fiyatı:", selected_customer[2])
        print("Borç:", selected_customer[3])
        print("Tarih:",selected_customer[4])
    else:
        print("Seçilen numarada bir müşteri bulunamadı.")
        
    conn.close()
def delete_customer():
    conn = create_connection()
    c = conn.cursor()
    id = int(input("Silmek istediğiniz müşterinin ID'sini girin: "))
    c.execute(f"SELECT * FROM customers WHERE id='{id}'")
    result = c.fetchone()
    if result:
        confirm = input(f"{result[1]} müşterisini silmek istediğinize emin misiniz? (E/H)")
        if confirm.lower() == "e":
            c.execute(f"DELETE FROM customers WHERE id='{id}'")
            conn.commit()
            print(f"{result[1]} müşterisi başarıyla silindi!")
        else:
            print("Silme işlemi iptal edildi.")
    else:
        print("Bu ID'ye ait bir müşteri bulunamadı.")
    conn.close()
def update_customer():
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()

    id = int(input("Güncellenecek müşterinin ID'sini girin: "))
    c.execute(f"SELECT * FROM customers WHERE id='{id}'")
    result = c.fetchone()
    if result:
        name = input("Yeni müşteri unvanı: ")
        price = float(input("Yeni alış fiyatı: "))
        c.execute(f"UPDATE customers SET name='{name}', price='{price}', date='{date}' WHERE id='{id}'")
        conn.commit()
        print(f"Müşteri {name} başarıyla güncellendi!")
    else:
        print("Bu ID'ye ait bir müşteri yok.")
        
    conn.close()

"""
END    OF    C U S T O M E R     O P E R A T İ O N 
"""

"""
S A L E S    O P E R A T İ O N S 
"""
def sales():
    sale = "sale"
    print(sale)

def ekstre():
    ekstre = "ekstre"
    print(ekstre)
    
...


"""
E N D    O F    S A L E S   O P E R A T İ O N S
"""



if __name__ == "__main__":
    get_date()
    while True:
        choice = main_menu()
        if choice == "1":
            while True:
                choice = menu()
                if choice == "1":
                    add_customer()
                elif choice == "2":
                    list_customers()
                elif choice == "3":
                    delete_customer()
                elif choice == "4":
                    update_customer()
                elif choice == "5":
                    export_customers_to_excel()
                elif choice == "7":
                    select_customer()
                elif choice == "8":
                    get_date()
                elif choice == "9":
                    break

        elif choice == "2":
            while True:
                choice = satislar()
                if choice == "1":
                    sales()
                elif choice == "2":
                    ekstre()
                elif choice == "9":
                    break
        elif choice == "0":
            print("Programdan çıkılıyor...")
            break