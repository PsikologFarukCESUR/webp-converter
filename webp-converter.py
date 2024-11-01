import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import os
import pathlib
import subprocess
import platform

class WebPConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("WebP Dönüştürücü")
        self.root.geometry("800x600")
        
        # Değişkenler
        self.quality = tk.IntVar(value=80)
        self.delete_original = tk.BooleanVar(value=False)
        self.maintain_structure = tk.BooleanVar(value=True)
        self.source_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.base_filename = tk.StringVar(value="resim")
        self.rename_files = tk.BooleanVar(value=False)  # Dosya adı değiştirme seçeneği
        self.last_output_folder = None  # Son çıktı klasörünü takip etmek için
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Kaynak seçimi
        source_frame = ttk.LabelFrame(main_frame, text="Kaynak Seçimi", padding=10)
        source_frame.pack(fill="x", pady=5)
        
        ttk.Button(source_frame, text="Dosya Seç", command=self.select_file).pack(side="left", padx=5)
        ttk.Button(source_frame, text="Klasör Seç", command=self.select_folder).pack(side="left", padx=5)
        self.source_label = ttk.Label(source_frame, text="Henüz seçim yapılmadı")
        self.source_label.pack(side="left", padx=5)
        
        # Hedef klasör seçimi
        output_frame = ttk.LabelFrame(main_frame, text="Hedef Klasör", padding=10)
        output_frame.pack(fill="x", pady=5)
        
        ttk.Button(output_frame, text="Klasör Seç", command=self.select_output_folder).pack(side="left", padx=5)
        self.output_label = ttk.Label(output_frame, text="Kaynak klasör kullanılacak")
        self.output_label.pack(side="left", padx=5)
        
        # Ayarlar
        settings_frame = ttk.LabelFrame(main_frame, text="Ayarlar", padding=10)
        settings_frame.pack(fill="x", pady=5)
        
        # Kalite ayarı
        quality_frame = ttk.Frame(settings_frame)
        quality_frame.pack(fill="x", pady=5)
        ttk.Label(quality_frame, text="Kalite:").pack(side="left", padx=5)
        
        # Kalite değer etiketi
        self.quality_label = ttk.Label(quality_frame, text="80%")
        self.quality_label.pack(side="right", padx=5)
        
        # Kalite kaydırıcısı
        quality_scale = ttk.Scale(
            quality_frame, 
            from_=1, 
            to=100, 
            orient="horizontal", 
            variable=self.quality,
            command=self.update_quality_label
        )
        quality_scale.pack(side="left", fill="x", expand=True, padx=5)
        
        # İsimlendirme ayarları
        naming_frame = ttk.LabelFrame(settings_frame, text="Dosya İsimlendirme", padding=10)
        naming_frame.pack(fill="x", pady=5)
        
        # Dosya adı değiştirme seçeneği
        rename_frame = ttk.Frame(naming_frame)
        rename_frame.pack(fill="x", pady=2)
        ttk.Checkbutton(rename_frame, text="Dosya adlarını değiştir", 
                       variable=self.rename_files,
                       command=self.toggle_filename_entry).pack(side="left", padx=5)
        
        # Dosya adı giriş alanı
        self.filename_frame = ttk.Frame(naming_frame)
        self.filename_frame.pack(fill="x", pady=2)
        ttk.Label(self.filename_frame, text="Dosya adı:").pack(side="left", padx=5)
        self.filename_entry = ttk.Entry(self.filename_frame, textvariable=self.base_filename, width=30)
        self.filename_entry.pack(side="left", padx=5)
        ttk.Label(self.filename_frame, text="(Birden fazla dosya için otomatik numaralandırılacak)").pack(side="left", padx=5)
        
        # Başlangıçta dosya adı giriş alanını devre dışı bırak
        self.toggle_filename_entry()
        
        # Diğer ayarlar
        options_frame = ttk.Frame(settings_frame)
        options_frame.pack(fill="x", pady=5)
        ttk.Checkbutton(options_frame, text="Orijinal dosyaları sil", 
                       variable=self.delete_original).pack(side="left", padx=5)
        ttk.Checkbutton(options_frame, text="Klasör yapısını koru", 
                       variable=self.maintain_structure).pack(side="left", padx=5)
        
        # İlerleme çubuğu
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.pack(fill="x", pady=10)
        
        # Butonlar için frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=5)
        
        # Dönüştür ve Klasörü Aç butonları
        ttk.Button(button_frame, text="Dönüştür", command=self.convert).pack(side="left", padx=5)
        self.open_folder_button = ttk.Button(button_frame, text="Klasörü Aç", 
                                           command=self.open_output_folder, state="disabled")
        self.open_folder_button.pack(side="left", padx=5)
        
        # Sonuç listesi
        result_frame = ttk.LabelFrame(main_frame, text="Sonuçlar", padding=10)
        result_frame.pack(fill="both", expand=True, pady=5)
        
        self.result_text = tk.Text(result_frame, height=10)
        self.result_text.pack(fill="both", expand=True)

    def open_output_folder(self):
        """Çıktı klasörünü sistemin varsayılan dosya gezgininde aç"""
        if self.last_output_folder and os.path.exists(self.last_output_folder):
            if platform.system() == "Windows":
                os.startfile(self.last_output_folder)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", self.last_output_folder])
            else:  # Linux ve diğer sistemler
                subprocess.run(["xdg-open", self.last_output_folder])
    
    def convert(self):
        if not self.source_path.get():
            messagebox.showerror("Hata", "Lütfen kaynak dosya veya klasör seçin!")
            return
        
        if self.rename_files.get() and not self.base_filename.get().strip():
            messagebox.showerror("Hata", "Lütfen bir dosya adı girin!")
            return
            
        self.result_text.delete(1.0, 'end')
        self.progress['value'] = 0
        
        # Çıktı klasörünü belirle
        output_base = self.output_path.get()
        self.last_output_folder = os.path.join(output_base, self.get_output_folder_name())
        
        # Dosya listesini oluştur
        files_to_convert = []
        source_path = self.source_path.get()
        
        if os.path.isfile(source_path):
            files_to_convert.append(source_path)
        else:
            for ext in ('*.jpg', '*.jpeg', '*.png'):
                files_to_convert.extend(list(pathlib.Path(source_path).rglob(ext)))
        
        total_files = len(files_to_convert)
        if total_files == 0:
            messagebox.showinfo("Bilgi", "Dönüştürülecek dosya bulunamadı!")
            return
        
        # İlerleme çubuğunu ayarla
        self.progress['maximum'] = total_files
        
        # Dosyaları dönüştür
        for i, file_path in enumerate(files_to_convert, 1):
            index = (i if len(files_to_convert) > 1 else None) if self.rename_files.get() else None
            self.convert_single_file(str(file_path), output_base, index)
            self.progress['value'] = i
            self.root.update()
        
        # Dönüştürme tamamlandığında Klasörü Aç butonunu etkinleştir
        self.open_folder_button.config(state="normal")
        messagebox.showinfo("Bilgi", "Dönüştürme işlemi tamamlandı!")

    # Diğer metodlar aynı kalacak...
    def toggle_filename_entry(self):
        """Dosya adı giriş alanını etkinleştir/devre dışı bırak"""
        if self.rename_files.get():
            self.filename_entry.config(state="normal")
        else:
            self.filename_entry.config(state="disabled")
    
    def update_quality_label(self, *args):
        self.quality_label.config(text=f"{self.quality.get()}%")
    
    def get_output_folder_name(self):
        """Çıktı klasörünün adını belirle"""
        if self.rename_files.get() and self.base_filename.get().strip():
            return f"{self.base_filename.get()}-webp"
        return "webp"
    
    def convert_single_file(self, input_path, output_folder, index=None):
        try:
            # Yeni dosya adını oluştur
            if self.rename_files.get():
                if index is None:
                    new_filename = f"{self.base_filename.get()}.webp"
                else:
                    new_filename = f"{self.base_filename.get()}-{index}.webp"
            else:
                # Orjinal dosya adını kullan
                original_name = os.path.splitext(os.path.basename(input_path))[0]
                new_filename = f"{original_name}.webp"
            
            # Çıktı klasörünü belirle
            webp_folder = os.path.join(output_folder, self.get_output_folder_name())
            
            # Çıktı dosya yolunu oluştur
            if self.maintain_structure.get():
                rel_path = os.path.relpath(os.path.dirname(input_path), self.source_path.get())
                output_path = os.path.join(webp_folder, rel_path, new_filename)
            else:
                output_path = os.path.join(webp_folder, new_filename)
            
            # Hedef klasörü oluştur
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Dosyayı aç ve dönüştür
            with Image.open(input_path) as img:
                original_size = os.path.getsize(input_path)
                
                # WebP olarak kaydet
                img.save(output_path, 'WEBP', quality=self.quality.get())
                
                new_size = os.path.getsize(output_path)
                savings = (1 - new_size/original_size) * 100
                
                # Sonuçları kaydet
                result = f"Dönüştürüldü: {os.path.basename(input_path)} -> {new_filename}\n"
                result += f"Orijinal: {original_size/1024:.1f}KB\n"
                result += f"Yeni: {new_size/1024:.1f}KB\n"
                result += f"Kazanç: {savings:.1f}%\n"
                result += "-" * 40 + "\n"
                
                self.result_text.insert('end', result)
                self.result_text.see('end')
                self.root.update()
                
                # Orijinal dosyayı sil (eğer seçilmişse)
                if self.delete_original.get():
                    os.remove(input_path)
                
        except Exception as e:
            self.result_text.insert('end', f"Hata: {input_path} - {str(e)}\n")
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            self.source_path.set(file_path)
            self.source_label.config(text=os.path.basename(file_path))
            # Hedef klasörü otomatik ayarla
            self.output_path.set(os.path.dirname(file_path))
            self.output_label.config(text=os.path.dirname(file_path))
    
    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.source_path.set(folder_path)
            self.source_label.config(text=folder_path)
            # Hedef klasörü otomatik ayarla
            self.output_path.set(folder_path)
            self.output_label.config(text=folder_path)
    
    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_path.set(folder_path)
            self.output_label.config(text=folder_path)

def main():
    root = tk.Tk()
    app = WebPConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()