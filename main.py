import flet as ft

def main(page: ft.Page):
    page.title = "Bakkal Otomasyon Sistemi"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO

    # --- GEÇİCİ VERİLER ---
    stok_listesi = [
        {"barkod": "101", "ad": "Sütaş Süt 1L", "fiyat": 35.0, "adet": 50},
        {"barkod": "102", "ad": "Torku Şeker 1kg", "fiyat": 30.0, "adet": 40},
        {"barkod": "103", "ad": "Ekmek", "fiyat": 10.0, "adet": 100}
    ]
    
    cari_listesi = [
        {"ad": "Ahmet Yılmaz (Müşteri)", "telefon": "5551112233", "bakiye": 250.0, "tip": "Müşteri"},
        {"ad": "Sütaş Gıda A.Ş. (Tedarikçi)", "telefon": "2164445566", "bakiye": 1500.0, "tip": "Tedarikçi"},
        {"ad": "Mehmet Demir (Müşteri)", "telefon": "5554445566", "bakiye": 120.5, "tip": "Müşteri"}
    ]

    aktif_sepet = []
    secilen_cari = {"ad": "Seçilmedi", "telefon": ""}

    # --- 1. STOK VE ÜRÜN YÖNETİMİ ---
    barkod_input = ft.TextField(label="Barkod No", width=140)
    urun_ad_input = ft.TextField(label="Ürün Adı", width=160)
    fiyat_input = ft.TextField(label="Fiyat (TL)", width=90)
    adet_input = ft.TextField(label="Adet", width=80)
    
    stok_tablo = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Barkod")),
            ft.DataColumn(ft.Text("Ürün Adı")),
            ft.DataColumn(ft.Text("Fiyat")),
            ft.DataColumn(ft.Text("Adet")),
            ft.DataColumn(ft.Text("İşlem")),
        ],
        rows=[]
    )

    def stoklari_guncelle():
        stok_tablo.rows.clear()
        for item in stok_listesi:
            def urun_sec(e, b=item["barkod"], a=item["ad"], f=item["fiyat"], m=item["adet"]):
                barkod_input.value = b
                urun_ad_input.value = a
                fiyat_input.value = str(f)
                adet_input.value = str(m)
                page.update()

            def urun_sil(b_kodu=item["barkod"]):
                nonlocal stok_listesi
                stok_listesi = [x for x in stok_listesi if x["barkod"] != b_kodu]
                stoklari_guncelle()
                page.snack_bar = ft.SnackBar(ft.Text("Ürün silindi!"))
                page.snack_bar.open = True
                page.update()

            stok_tablo.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(item["barkod"])),
                    ft.DataCell(ft.Text(item["ad"])),
                    ft.DataCell(ft.Text(f"{item['fiyat']} TL")),
                    ft.DataCell(ft.Text(str(item["adet"]))),
                    ft.DataCell(ft.Row([
                        ft.IconButton(icon=ft.Icons.EDIT, icon_color="blue", tooltip="Düzenle", on_click=lambda e, b=item["barkod"], a=item["ad"], f=item["fiyat"], m=item["adet"]: urun_sec(e, b, a, f, m)),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color="red", tooltip="Sil", on_click=lambda e, bk=item["barkod"]: urun_sil(bk))
                    ], spacing=0))
                ])
            )
        page.update()

    def urun_ekle_guncelle(e):
        if barkod_input.value and urun_ad_input.value:
            mevcut = next((x for x in stok_listesi if x["barkod"] == barkod_input.value), None)
            if mevcut:
                mevcut["ad"] = urun_ad_input.value
                mevcut["fiyat"] = float(fiyat_input.value) if fiyat_input.value else mevcut["fiyat"]
                mevcut["adet"] = int(adet_input.value) if adet_input.value else mevcut["adet"]
                mesaj = "Ürün güncellendi!"
            else:
                stok_listesi.append({
                    "barkod": barkod_input.value,
                    "ad": urun_ad_input.value,
                    "fiyat": float(fiyat_input.value) if fiyat_input.value else 0.0,
                    "adet": int(adet_input.value) if adet_input.value else 0
                })
                mesaj = "Yeni ürün eklendi!"

            barkod_input.value = ""
            urun_ad_input.value = ""
            fiyat_input.value = ""
            adet_input.value = ""
            stoklari_guncelle()
            page.snack_bar = ft.SnackBar(ft.Text(mesaj))
            page.snack_bar.open = True
            page.update()

    stok_ekle_btn = ft.ElevatedButton("Kaydet / Güncelle", on_click=urun_ekle_guncelle)

    stok_view = ft.Column([
        ft.Text("Ürün & Stok Yönetimi", size=18, weight=ft.FontWeight.BOLD),
        ft.Row([barkod_input, urun_ad_input, fiyat_input, adet_input, stok_ekle_btn], wrap=True, spacing=10),
        ft.Divider(),
        ft.Row([stok_tablo], scroll=ft.ScrollMode.AUTO)
    ], scroll=ft.ScrollMode.AUTO)

    # --- 2. FATURA / TEDARİKÇİ MAL GİRİŞİ ---
    fatura_tedarikci_dropdown = ft.Dropdown(
        label="Tedarikçi (Satıcı) Firma Seç",
        width=280,
        options=[]
    )

    def tedarikci_listesini_guncelle():
        fatura_tedarikci_dropdown.options = [ft.dropdown.Option(c["ad"]) for c in cari_listesi if c.get("tip") == "Tedarikçi"]

    tedarikci_listesini_guncelle()

    fatura_barkod = ft.TextField(label="Ürün Barkodu", width=160)
    fatura_adet = ft.TextField(label="Fatura Adeti", width=110)
    fatura_sonuc = ft.Text("", size=15, weight=ft.FontWeight.BOLD)

    def fatura_stok_isle(e):
        if not fatura_tedarikci_dropdown.value:
            fatura_sonuc.value = "⚠️ Lütfen faturayı kesen Tedarikçi firmayı seçin!"
            page.update()
            return

        if fatura_barkod.value and fatura_adet.value:
            bulunan = next((item for item in stok_listesi if item["barkod"] == fatura_barkod.value), None)
            if bulunan:
                eklenen = int(fatura_adet.value)
                bulunan["adet"] += eklenen
                
                tutar = eklenen * bulunan["fiyat"]
                tedarikci = next((c for c in cari_listesi if c["ad"] == fatura_tedarikci_dropdown.value), None)
                if tedarikci:
                    tedarikci["bakiye"] += tutar

                fatura_sonuc.value = f"✅ {fatura_tedarikci_dropdown.value} firmasından {eklenen} adet {bulunan['ad']} eklendi, borç kaydedildi."
                stoklari_guncelle()
                carileri_guncelle()
            else:
                fatura_sonuc.value = "⚠️ Bu barkod bulunamadı! Önce Stok İşlemlerinden kaydedin."
            fatura_barkod.value = ""
            fatura_adet.value = ""
            page.update()

    fatura_btn = ft.ElevatedButton("Faturayı İşle ve Stoğa Ekle", on_click=fatura_stok_isle, color="white", bgcolor="blue")

    fatura_view = ft.Column([
        ft.Text("Fatura ve Tedarikçi Mal Girişi", size=18, weight=ft.FontWeight.BOLD),
        ft.Text("Tedarikçiden gelen faturaları işleyin ve borç/stok dengesini kurun:", size=13),
        fatura_tedarikci_dropdown,
        ft.Row([fatura_barkod, fatura_adet, fatura_btn], wrap=True, spacing=10),
        fatura_sonuc
    ], spacing=15, scroll=ft.ScrollMode.AUTO)

    # --- 3. PROFESYONEL HIZLI SATIŞ KASASI ---
    satis_barkod_input = ft.TextField(label="Barkod Okut / Gir", width=200)
    sepet_tablo = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Ürün Adı")),
            ft.DataColumn(ft.Text("Fiyat")),
            ft.DataColumn(ft.Text("Adet")),
            ft.DataColumn(ft.Text("Toplam")),
        ],
        rows=[]
    )
    toplam_tutar_text = ft.Text("Genel Toplam: 0.00 TL", size=18, weight=ft.FontWeight.BOLD, color="green")
    
    odeme_tipi_dropdown = ft.Dropdown(
        label="Ödeme Türü",
        width=140,
        options=[
            ft.dropdown.Option("Nakit"),
            ft.dropdown.Option("Kredi Kartı"),
        ],
        value="Nakit"
    )

    cari_secim_text = ft.Text("Seçilen Cari: Yok", size=14, weight=ft.FontWeight.BOLD, color="blue")
    cari_sec_btn = ft.ElevatedButton("🔍 Cari Seç", icon=ft.Icons.SEARCH, visible=False)

    # Cari Arama ve Seçim Penceresi (Dialog)
    arama_input = ft.TextField(label="Cari Adı veya Telefon ile Ara...", width=300)
    dialog_cari_tablo = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("Cari Adı")), ft.DataColumn(ft.Text("Telefon")), ft.DataColumn(ft.Text("İşlem"))],
        rows=[]
    )

    def cari_arama_filtrele(e=""):
        dialog_cari_tablo.rows.clear()
        arama_metni = arama_input.value.lower() if arama_input.value else ""
        for c in cari_listesi:
            if arama_metni in c["ad"].lower() or arama_metni in c["telefon"]:
                def sec(cari_obj=c):
                    nonlocal secilen_cari
                    secilen_cari = cari_obj
                    cari_secim_text.value = f"Seçilen Cari: {cari_obj['ad']}"
                    page.dialog.open = False
                    page.update()

                dialog_cari_tablo.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(c["ad"])),
                        ft.DataCell(ft.Text(c["telefon"])),
                        ft.DataCell(ft.ElevatedButton("Seç", on_click=lambda e, co=c: sec(co)))
                    ])
                )
        page.update()

    arama_input.on_change = cari_arama_filtrele

    cari_secim_dialog = ft.AlertDialog(
        title=ft.Text("Cari Müşteri Listesi ve Arama"),
        content=ft.Column([arama_input, ft.Row([dialog_cari_tablo], scroll=ft.ScrollMode.AUTO)], tight=True, scroll=ft.ScrollMode.AUTO),
        actions=[ft.TextButton("Kapat", on_click=lambda e: setattr(page.dialog, 'open', False) or page.update())]
    )

    def cari_secim_pencere_ac(e):
        arama_input.value = "" # Açıldığında arama kutusunu sıfırla ki hepsi listelensin
        cari_arama_filtrele()
        page.dialog = cari_secim_dialog
        cari_secim_dialog.open = True
        page.update()

    cari_sec_btn.on_click = cari_secim_pencere_ac

    satis_turu_dropdown = ft.Dropdown(
        label="Fiş / İşlem Türü",
        width=170,
        options=[
            ft.dropdown.Option("Normal Fiş"),
            ft.dropdown.Option("Cari Hesap (Veresiye)"),
        ],
        value="Normal Fiş"
    )

    def satis_turu_degisti(e):
        if satis_turu_dropdown.value == "Cari Hesap (Veresiye)":
            cari_sec_btn.visible = True
            cari_secim_text.visible = True
        else:
            cari_sec_btn.visible = False
            cari_secim_text.visible = False
            secilen_cari.clear()
            secilen_cari.update({"ad": "Seçilmedi", "telefon": ""})
            cari_secim_text.value = "Seçilen Cari: Yok"
        page.update()

    satis_turu_dropdown.on_change = satis_turu_degisti

    satis_mesaj = ft.Text("", size=15, weight=ft.FontWeight.BOLD)

    def sepeti_guncelle():
        sepet_tablo.rows.clear()
        genel_toplam = 0.0
        for item in aktif_sepet:
            tutar = item["fiyat"] * item["adet"]
            genel_toplam += tutar
            sepet_tablo.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(item["ad"])),
                    ft.DataCell(ft.Text(f"{item['fiyat']} TL")),
                    ft.DataCell(ft.Text(str(item["adet"]))),
                    ft.DataCell(ft.Text(f"{tutar:.2f} TL")),
                ])
            )
        toplam_tutar_text.value = f"Genel Toplam: {genel_toplam:.2f} TL"
        page.update()

    def sepete_urun_ekle(e):
        if satis_barkod_input.value:
            bulunan = next((item for item in stok_listesi if item["barkod"] == satis_barkod_input.value), None)
            if bulunan:
                if bulunan["adet"] > 0:
                    sepet_item = next((s for s in aktif_sepet if s["barkod"] == bulunan["barkod"]), None)
                    if sepet_item:
                        if sepet_item["adet"] < bulunan["adet"]:
                            sepet_item["adet"] += 1
                        else:
                            satis_mesaj.value = "Stokta yeterli ürün yok!"
                            satis_barkod_input.value = ""
                            page.update()
                            return
                    else:
                        aktif_sepet.append({
                            "barkod": bulunan["barkod"],
                            "ad": bulunan["ad"],
                            "fiyat": bulunan["fiyat"],
                            "adet": 1
                        })
                    satis_mesaj.value = f"Eklendi: {bulunan['ad']}"
                else:
                    satis_mesaj.value = "Ürün stokta tükenmiş!"
            else:
                satis_mesaj.value = "Ürün bulunamadı!"
            satis_barkod_input.value = ""
            sepeti_guncelle()

    satis_barkod_input.on_submit = sepete_urun_ekle

    def satisi_tamamla_click(e):
        nonlocal aktif_sepet, secilen_cari
        if not aktif_sepet:
            satis_mesaj.value = "Sepet boş! Satış yapılamaz."
            page.update()
            return

        genel_toplam = sum(item["fiyat"] * item["adet"] for item in aktif_sepet)
        
        for s_item in aktif_sepet:
            stok_urun = next((st for st in stok_listesi if st["barkod"] == s_item["barkod"]), None)
            if stok_urun:
                stok_urun["adet"] -= s_item["adet"]

        if satis_turu_dropdown.value == "Cari Hesap (Veresiye)":
            if secilen_cari["ad"] == "Seçilmedi":
                satis_mesaj.value = "Lütfen cari seçimi yapın!"
                page.update()
                return
            
            secilen_cari["bakiye"] += genel_toplam
            satis_mesaj.value = f"✅ Veresiye Satış Başarılı: {secilen_cari['ad']} - {genel_toplam:.2f} TL"
            secilen_cari = {"ad": "Seçilmedi", "telefon": ""}
            cari_secim_text.value = "Seçilen Cari: Yok"
        else:
            satis_mesaj.value = f"✅ Satış Tamamlandı ({odeme_tipi_dropdown.value}): {genel_toplam:.2f} TL"

        aktif_sepet = []
        sepeti_guncelle()
        stoklari_guncelle()
        carileri_guncelle()
        page.update()

    satis_tamamla_btn = ft.ElevatedButton("Satışı Tamamla", icon=ft.Icons.CHECK, on_click=satisi_tamamla_click, color="white", bgcolor="green")

    satis_view = ft.Column([
        ft.Text("Hızlı Satış ve Kasa Ekranı", size=18, weight=ft.FontWeight.BOLD),
        ft.Row([satis_barkod_input, ft.ElevatedButton("Sepete Ekle", on_click=sepete_urun_ekle)], wrap=True, spacing=10),
        ft.Row([sepet_tablo], scroll=ft.ScrollMode.AUTO),
        toplam_tutar_text,
        ft.Divider(),
        ft.Row([odeme_tipi_dropdown, satis_turu_dropdown, cari_sec_btn, cari_secim_text], wrap=True, spacing=10),
        satis_tamamla_btn,
        satis_mesaj
    ], spacing=12, scroll=ft.ScrollMode.AUTO)

    # --- 4. CARİ TAKİP ---
    cari_ad_input = ft.TextField(label="Cari Ad / Firma Adı", width=180)
    cari_tel_input = ft.TextField(label="Telefon", width=120)
    cari_bakiye_input = ft.TextField(label="Bakiye", width=80)
    cari_tip_dropdown = ft.Dropdown(
        label="Cari Türü",
        width=120,
        options=[ft.dropdown.Option("Müşteri"), ft.dropdown.Option("Tedarikçi")],
        value="Müşteri"
    )

    cari_tablo = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Cari Adı")),
            ft.DataColumn(ft.Text("Tür")),
            ft.DataColumn(ft.Text("Telefon")),
            ft.DataColumn(ft.Text("Bakiye")),
            ft.DataColumn(ft.Text("İşlem")),
        ],
        rows=[]
    )

    def carileri_guncelle():
        cari_tablo.rows.clear()
        for c in cari_listesi:
            def cari_sil(tel=c["telefon"]):
                nonlocal cari_listesi
                cari_listesi = [x for x in cari_listesi if x["telefon"] != tel]
                carileri_guncelle()
                tedarikci_listesini_guncelle()
                page.snack_bar = ft.SnackBar(ft.Text("Cari silindi!"))
                page.snack_bar.open = True
                page.update()

            cari_tablo.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(c["ad"])),
                    ft.DataCell(ft.Text(c.get("tip", "Müşteri"))),
                    ft.DataCell(ft.Text(c["telefon"])),
                    ft.DataCell(ft.Text(f"{c['bakiye']:.2f} TL")),
                    ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, icon_color="red", on_click=lambda e, t=c["telefon"]: cari_sil(t))),
                ])
            )
        page.update()

    def cari_ekle(e):
        if cari_ad_input.value and cari_tel_input.value:
            cari_listesi.append({
                "ad": cari_ad_input.value,
                "telefon": cari_tel_input.value,
                "bakiye": float(cari_bakiye_input.value) if cari_bakiye_input.value else 0.0,
                "tip": cari_tip_dropdown.value
            })
            cari_ad_input.value = ""
            cari_tel_input.value = ""
            cari_bakiye_input.value = ""
            carileri_guncelle()
            tedarikci_listesini_guncelle()
            page.snack_bar = ft.SnackBar(ft.Text("Yeni cari eklendi!"))
            page.snack_bar.open = True
            page.update()

    cari_ekle_btn = ft.ElevatedButton("Cari Ekle", on_click=cari_ekle)
    carileri_guncelle()

    cari_view = ft.Column([
        ft.Text("Cari / Müşteri ve Tedarikçi Yönetimi", size=18, weight=ft.FontWeight.BOLD),
        ft.Row([cari_ad_input, cari_tel_input, cari_bakiye_input, cari_tip_dropdown, cari_ekle_btn], wrap=True, spacing=10),
        ft.Divider(),
        ft.Row([cari_tablo], scroll=ft.ScrollMode.AUTO)
    ], scroll=ft.ScrollMode.AUTO)

    # --- EKRAN YÖNETİMİ ---
    icerik_alani = ft.Container(content=satis_view, padding=10)

    def sayfa_sec(e, view):
        icerik_alani.content = view
        page.update()

    menu_bar = ft.Row([
        ft.OutlinedButton("Hızlı Satış", on_click=lambda e: sayfa_sec(e, satis_view)),
        ft.OutlinedButton("Stok İşlemleri", on_click=lambda e: sayfa_sec(e, stok_view)),
        ft.OutlinedButton("Fatura Girişi", on_click=lambda e: sayfa_sec(e, fatura_view)),
        ft.OutlinedButton("Cari Takip", on_click=lambda e: sayfa_sec(e, cari_view)),
    ], alignment=ft.MainAxisAlignment.CENTER, wrap=True, spacing=5)

    page.add(
        ft.Row([ft.Text("🛒 Bakkal Yönetim Paneli", size=20, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
        menu_bar,
        ft.Divider(),
        icerik_alani
    )

ft.app(target=main)
