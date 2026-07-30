import flet as ft

def main(page: ft.Page):
    page.title = "Bakkal Otomasyon Sistemi"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # --- GEÇİCİ VERİLER ---
    stok_listesi = [
        {"barkod": "101", "ad": "Sütaş Süt 1L", "fiyat": 35.0, "adet": 50},
        {"barkod": "102", "ad": "Torku Şeker 1kg", "fiyat": 30.0, "adet": 40},
        {"barkod": "103", "ad": "Ekmek", "fiyat": 10.0, "adet": 100}
    ]
    
    cari_listesi = [
        {"ad": "Ahmet Yılmaz", "telefon": "5551112233", "bakiye": 250.0},
        {"ad": "Mehmet Demir", "telefon": "5554445566", "bakiye": 120.5}
    ]

    # --- 1. STOK VE ÜRÜN YÖNETİMİ ---
    barkod_input = ft.TextField(label="Barkod No", width=140)
    urun_ad_input = ft.TextField(label="Ürün Adı", width=180)
    fiyat_input = ft.TextField(label="Fiyat (TL)", width=100)
    adet_input = ft.TextField(label="Adet", width=90)
    
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
            # Her ürüne özel silme butonu
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
                    ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, icon_color="red", on_click=lambda e, bk=item["barkod"]: urun_sil(bk))),
                ])
            )
        page.update()

    def urun_ekle(e):
        if barkod_input.value and urun_ad_input.value and fiyat_input.value and adet_input.value:
            # Aynı barkod varsa güncelle, yoksa yeni ekle
            mevcut = next((x for x in stok_listesi if x["barkod"] == barkod_input.value), None)
            if mevcut:
                mevcut["ad"] = urun_ad_input.value
                mevcut["fiyat"] = float(fiyat_input.value)
                mevcut["adet"] = int(adet_input.value)
                mesaj = "Ürün güncellendi!"
            else:
                stok_listesi.append({
                    "barkod": barkod_input.value,
                    "ad": urun_ad_input.value,
                    "fiyat": float(fiyat_input.value),
                    "adet": int(adet_input.value)
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

    stok_ekle_btn = ft.ElevatedButton("Kaydet / Güncelle", on_click=urun_ekle)
    stoklari_guncelle()

    stok_view = ft.Column([
        ft.Text("Ürün & Stok Yönetimi (Ekle / Güncelle / Sil)", size=18, weight=ft.FontWeight.BOLD),
        ft.Row([barkod_input, urun_ad_input, fiyat_input, adet_input, stok_ekle_btn], wrap=True),
        ft.Divider(),
        stok_tablo
    ], scroll=ft.ScrollMode.AUTO)

    # --- 2. HIZLI SATIŞ ---
    satis_barkod = ft.TextField(label="Ürün Barkodu Okut", width=250)
    satis_sonuc = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
    
    def urun_sat(e):
        bulunan = next((item for item in stok_listesi if item["barkod"] == satis_barkod.value), None)
        if bulunan and bulunan["adet"] > 0:
            bulunan["adet"] -= 1
            satis_sonuc.value = f"Satış Yapıldı: {bulunan['ad']} - {bulunan['fiyat']} TL"
            stoklari_guncelle()
        else:
            satis_sonuc.value = "Ürün bulunamadı veya stokta kalmadı!"
        satis_barkod.value = ""
        page.update()

    satis_btn = ft.ElevatedButton("Satışı Tamamla", on_click=urun_sat)

    satis_view = ft.Column([
        ft.Text("Hızlı Satış Kasası", size=18, weight=ft.FontWeight.BOLD),
        ft.Row([satis_barkod, satis_btn]),
        satis_sonuc
    ], spacing=20)

    # --- 3. CARİ TAKİP & MÜŞTERİ EKLEME ---
    cari_ad_input = ft.TextField(label="Müşteri Ad Soyad", width=180)
    cari_tel_input = ft.TextField(label="Telefon", width=150)
    cari_bakiye_input = ft.TextField(label="Borç / Bakiye", width=100)

    cari_tablo = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Müşteri Adı")),
            ft.DataColumn(ft.Text("Telefon")),
            ft.DataColumn(ft.Text("Borç / Bakiye")),
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
                page.snack_bar = ft.SnackBar(ft.Text("Cari kayıt silindi!"))
                page.snack_bar.open = True
                page.update()

            cari_tablo.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(c["ad"])),
                    ft.DataCell(ft.Text(c["telefon"])),
                    ft.DataCell(ft.Text(f"{c['bakiye']} TL")),
                    ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, icon_color="red", on_click=lambda e, t=c["telefon"]: cari_sil(t))),
                ])
            )
        page.update()

    def cari_ekle(e):
        if cari_ad_input.value and cari_tel_input.value:
            cari_listesi.append({
                "ad": cari_ad_input.value,
                "telefon": cari_tel_input.value,
                "bakiye": float(cari_bakiye_input.value) if cari_bakiye_input.value else 0.0
            })
            cari_ad_input.value = ""
            cari_tel_input.value = ""
            cari_bakiye_input.value = ""
            carileri_guncelle()
            page.snack_bar = ft.SnackBar(ft.Text("Yeni cari eklendi!"))
            page.snack_bar.open = True
            page.update()

    cari_ekle_btn = ft.ElevatedButton("Cari Ekle", on_click=cari_ekle)
    carileri_guncelle()

    cari_view = ft.Column([
        ft.Text("Müşteri Cari ve Veresiye Yönetimi", size=18, weight=ft.FontWeight.BOLD),
        ft.Row([cari_ad_input, cari_tel_input, cari_bakiye_input, cari_ekle_btn], wrap=True),
        ft.Divider(),
        cari_tablo
    ], scroll=ft.ScrollMode.AUTO)

    # --- EKRAN YÖNETİMİ ---
    icerik_alani = ft.Container(content=satis_view, padding=20)

    def sayfa_sec(e, view):
        icerik_alani.content = view
        page.update()

    menu_bar = ft.Row([
        ft.OutlinedButton("Hızlı Satış", on_click=lambda e: sayfa_sec(e, satis_view)),
        ft.OutlinedButton("Stok İşlemleri", on_click=lambda e: sayfa_sec(e, stok_view)),
        ft.OutlinedButton("Cari Takip", on_click=lambda e: sayfa_sec(e, cari_view)),
    ], alignment=ft.MainAxisAlignment.CENTER)

    page.add(
        ft.Row([ft.Text("🛒 Bakkal Yönetim Paneli", size=22, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
        menu_bar,
        ft.Divider(),
        icerik_alani
    )

ft.app(target=main)
