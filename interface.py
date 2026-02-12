import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import time
from medical_blockchain import medical_db 
from security import calculate_pdf_hash

# Modern Dashboard Renk Paleti
COLORS = {
    "bg_dark": "#0f111a", 
    "card_bg": "#1a1c2e", 
    "accent": "#5865f2",
    "success": "#2ecc71", 
    "danger": "#e74c3c", 
    "text_main": "#ffffff",
    "text_dim": "#949ba4", 
    "border": "#2f3136"
}

class ProfessionalMedicalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BLOCKCHAIN VERIFIER PRO")
        self.root.geometry("1150x800")
        self.root.configure(bg=COLORS["bg_dark"])
        
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("TNotebook", background=COLORS["bg_dark"], borderwidth=0)
        self.style.configure("TNotebook.Tab", font=("Segoe UI Semibold", 10), padding=[25, 12])
        self.style.map("TNotebook.Tab", background=[("selected", COLORS["accent"])])

        self.setup_ui()

    def setup_ui(self):
        # Üst Başlık
        header = tk.Frame(self.root, bg=COLORS["bg_dark"], pady=20)
        header.pack(fill="x")
        tk.Label(header, text="🛡️ MEDICAL REPORT CONTROL", font=("Segoe UI Black", 24), 
                 bg=COLORS["bg_dark"], fg=COLORS["accent"]).pack(side="left", padx=40)
        
        # Sekmeler
        self.tabs = ttk.Notebook(self.root)
        self.tab_reg = tk.Frame(self.tabs, bg=COLORS["bg_dark"], padx=30, pady=20)
        self.tab_verify = tk.Frame(self.tabs, bg=COLORS["bg_dark"], padx=30, pady=20)
        self.tab_explorer = tk.Frame(self.tabs, bg=COLORS["bg_dark"], padx=30, pady=20)

        self.tabs.add(self.tab_reg, text=" ✚ RAPOR MÜHÜRLER ")
        self.tabs.add(self.tab_verify, text=" 🔍 DOĞRULAMA MERKEZİ ")
        self.tabs.add(self.tab_explorer, text=" 🔗 ZİNCİR GEZGİNİ ")
        self.tabs.pack(expand=1, fill="both")

        self.build_reg_tab()
        self.build_verify_tab()
        self.build_explorer_tab()

    def build_reg_tab(self):
        # Kapsayıcı Frame (Sol Form + Sağ Log)
        self.reg_container = tk.Frame(self.tab_reg, bg=COLORS["bg_dark"])
        self.reg_container.pack(fill="both", expand=True)

        # Sol Panel (Giriş Alanı)
        form = tk.Frame(self.reg_container, bg=COLORS["card_bg"], padx=25, pady=25, 
                        highlightthickness=1, highlightbackground=COLORS["border"])
        form.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(form, text="HASTA KİMLİK NO", bg=COLORS["card_bg"], fg=COLORS["text_dim"], 
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_id = tk.Entry(form, font=("Segoe UI", 12), bg=COLORS["bg_dark"], 
                               fg="white", insertbackground="white", borderwidth=0)
        self.ent_id.pack(fill="x", pady=(5, 20), ipady=8)

        tk.Button(form, text="📁 DOSYALARI SEÇ", bg=COLORS["accent"], fg="white", 
                  font=("Segoe UI", 10, "bold"), command=self.select_files, cursor="hand2").pack(fill="x", pady=10)
        
        self.list_files = tk.Listbox(form, bg=COLORS["bg_dark"], fg=COLORS["success"], 
                                     font=("Consolas", 10), borderwidth=0, height=10)
        self.list_files.pack(fill="both", expand=True, pady=10)

        tk.Button(form, text="⛓️ ZİNCİRE İŞLE", bg=COLORS["success"], fg="white", 
                  font=("Segoe UI", 12, "bold"), command=self.seal_block, cursor="hand2").pack(fill="x", pady=10)

        # Sağ Panel (Terminal / Log Ekranı)
        self.log_reg = tk.Text(self.reg_container, width=45, bg="#000000", fg=COLORS["accent"], 
                               font=("Consolas", 9), padx=15, pady=15, borderwidth=0)
        self.log_reg.pack(side="right", fill="both")
        self.log_reg.insert("1.0", "> Sistem başlatıldı...\n> Veri girişi bekleniyor.")

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Dosyaları", "*.pdf")])
        for f in files:
            self.list_files.insert(tk.END, f)

    def seal_block(self):
        paths = self.list_files.get(0, tk.END)
        p_id = self.ent_id.get()
        if not paths or not p_id:
            messagebox.showwarning("Uyarı", "Hasta ID ve Dosya seçimi zorunludur!")
            return
        
        # Raporları hazırla ve mühürle
        reports = [{"patient_id": p_id, "file_name": p.split("/")[-1], "report_hash": calculate_pdf_hash(p)} for p in paths]
        new_block = medical_db.add_block(reports)
        
        # Log paneline yazdır
        self.log_reg.delete("1.0", tk.END)
        self.log_reg.insert("1.0", f"> İŞLEM BAŞARILI\n> Blok İndeksi: {new_block.index}\n> Hash: {new_block.hash[:32]}...\n> Zaman: {time.ctime(new_block.timestamp)}\n> Rapor Sayısı: {len(reports)}")
        
        self.list_files.delete(0, tk.END)
        self.update_explorer()

    def build_verify_tab(self):
        card = tk.Frame(self.tab_verify, bg=COLORS["card_bg"], padx=50, pady=50, 
                        highlightthickness=1, highlightbackground=COLORS["border"])
        card.pack(pady=40, fill="x")
        
        tk.Label(card, text="GÜVENLİ DOĞRULAMA SİSTEMİ", font=("Segoe UI", 14, "bold"), 
                 bg=COLORS["card_bg"], fg=COLORS["text_main"]).pack(pady=(0, 20))

        tk.Button(card, text="📂 DOSYA ANALİZİNİ BAŞLAT", bg=COLORS["accent"], fg="white", 
                  font=("Segoe UI", 12, "bold"), command=self.verify_report, pady=15).pack(fill="x")
        
        self.verify_res = tk.Label(self.tab_verify, text="SORGULAMA İÇİN HAZIR", 
                                   font=("Segoe UI", 18, "bold"), bg=COLORS["bg_dark"], 
                                   fg=COLORS["text_dim"], pady=50)
        self.verify_res.pack()

    def verify_report(self):
        path = filedialog.askopenfilename()
        if path:
            h = calculate_pdf_hash(path)
            valid, block, report = medical_db.verify_report_integrity(h)
            if valid:
                self.verify_res.config(text=f"✅ BELGE DOĞRULANDI\nHasta ID: {report['patient_id']}\nKayıt: {time.ctime(block.timestamp)}", fg=COLORS["success"])
            else:
                self.verify_res.config(text="❌ KRİTİK HATA\nBELGE KAYDI BULUNAMADI!", fg=COLORS["danger"])

    def build_explorer_tab(self):
        self.view = tk.Text(self.tab_explorer, bg=COLORS["card_bg"], fg="#cdd6f4", 
                             font=("Consolas", 10), borderwidth=0, padx=20, pady=20)
        self.view.pack(fill="both", expand=True)
        self.update_explorer()

    def update_explorer(self):
        self.view.delete("1.0", tk.END)
        for b in medical_db.chain:
            self.view.insert(tk.END, f"📦 BLOK #{b.index}\n")
            self.view.insert(tk.END, f"Hash: {b.hash}\n")
            self.view.insert(tk.END, f"Önceki Hash: {b.previous_hash}\n")
            self.view.insert(tk.END, f"Veriler: {json.dumps(b.reports, indent=2)}\n")
            self.view.insert(tk.END, "-"*80 + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalMedicalApp(root)
    root.mainloop()