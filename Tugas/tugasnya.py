import tkinter
from tkinter import*
import sqlite3
import tkinter.messagebox

window = tkinter.Tk()
window.title("Prediksi Prodi Berdasarkan Nilai Tertingi")

# koneksi ke database
connect = sqlite3.connect("prodi.db")
cursor = connect.cursor()

# fungsi tombol
def hasil_prediksi () :
    nama = nama_entry.get()
    if nama :
        matematika = int(entry_nilai_matematika.get())
        geografi = int(entry_nilai_geografi.get())
        inggris = int(entry_nilai_inggris.get())
        # Membandingkan Nilai 
        if matematika >= geografi and matematika >= inggris :
            hasil = "Kedokteran"
            frame_hasil.grid_configure(row=3,column=0,sticky="news",padx=20,pady=10)
            label_hasil.config(text=hasil)
            label_hasil.pack()
        elif geografi>=matematika and geografi>=inggris : 
            hasil = "Teknik"
            frame_hasil.grid_configure(row=3,column=0,sticky="news",padx=20,pady=10)
            label_hasil.config(text=hasil)
            label_hasil.pack()
        else :
            hasil = "Bahasa"
            frame_hasil.grid_configure(row=3,column=0,sticky="news",padx=20,pady=10)
            label_hasil.config(text=hasil)
            label_hasil.pack()

        # membuat table
        create_table_query = '''--sql
        create table if not EXISTS nilai_siswa(
        nama text,
        nilai_matematika int,
        nilai_geografi INT,
        nilai_inggris INT,
        hasil text
        )'''
        connect.execute(create_table_query)

        # insert data
        insert_data_query = '''--sql
        insert into nilai_siswa(
        nama,
        nilai_matematika,
        nilai_geografi,
        nilai_inggris,
        hasil)
        values(?,?,?,?,?)'''
        insert_data_tuple = (nama,
                             matematika,
                             geografi,
                             inggris,
                             hasil)
        cursor.execute(insert_data_query,insert_data_tuple)
        connect.commit()
        
    else : 
        tkinter.messagebox.showwarning(title="Warning !",message="Nama Harus Di isi")

def view() : 
    for widget in frame.winfo_children() :
        widget.destroy()
    cursor.execute("select * from nilai_siswa")
    data = cursor.fetchall()
    connect.commit()
    connect.close()
    for row in data :
        label_select = tkinter.Label(frame,text=str(row))
        label_select.pack(padx=20,pady=10)
        
frame = tkinter.Frame(window)
frame.pack()

# frame nama
frame_label_nama = tkinter.LabelFrame(frame,text="Nama")
frame_label_nama.grid(row=0,column=0,padx=20,pady=5,sticky="news")

# Label dan entry nama
nama_label = tkinter.Label(frame_label_nama,text="Masukkan Nama : ")
nama_entry = tkinter.Entry(frame_label_nama)
nama_label.grid(row=0,column=0,padx=20,pady=5)
nama_entry.grid(row=0,column=1,padx=50,pady=5)

# frame nilai
frame_nilai = tkinter.LabelFrame(frame,text="Nilai")
frame_nilai.grid(row=1,column=0,sticky="news",padx=20,pady=5)

# label dan entry nilai
label_nilai_matematika = tkinter.Label(frame_nilai,text="Masukkan Nilai matematika : ")
label_nilai_geografi = tkinter.Label(frame_nilai,text="Masukkan Nilai geografi : ")
label_nilai_inggris = tkinter.Label(frame_nilai,text="Masukkan Nilai inggris : ")
nilai_matematika = tkinter.IntVar()
nilai_geografi = tkinter.IntVar()
nilai_inggris = tkinter.IntVar()
label_nilai_matematika.grid(row=0,column=0)
label_nilai_geografi.grid(row=1,column=0)
label_nilai_inggris.grid(row=2,column=0)

entry_nilai_matematika = tkinter.Entry(frame_nilai,textvariable=nilai_matematika)
entry_nilai_geografi = tkinter.Entry(frame_nilai,textvariable=nilai_geografi)
entry_nilai_inggris = tkinter.Entry(frame_nilai,textvariable=nilai_inggris)

entry_nilai_matematika.grid(row=0,column=1)
entry_nilai_geografi.grid(row=1,column=1)
entry_nilai_inggris.grid(row=2,column=1)

# perulangan untuk mengatur padding widget dalam frame nilai
for widget in frame_nilai.winfo_children() : 
    widget.grid_configure(padx=20,pady=5)

# Tombol
button = tkinter.Button(frame,text="Predict IT !",command=hasil_prediksi)
button.grid(sticky="news",padx=20,pady=10)

# frame hasil prediksi
frame_hasil = tkinter.LabelFrame(frame,text="Hasil Prediksi")
frame_hasil.grid()
label_hasil = tkinter.Label(frame_hasil)

# select from 
frame_command_sql = tkinter.Button(frame,text="Command SQL",command=view)
frame_command_sql.grid(row=4,column=0,sticky="news" ,padx=20,pady=10)

window.mainloop()