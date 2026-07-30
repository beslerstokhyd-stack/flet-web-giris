import flet as ft

def main(page: ft.Page):
    page.title = "Bakkal Otomasyon Sistemi"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- VERİLER (Geçici Hafıza Listeleri) ---
    stok_listesi = [
        {"barkod": "101", "ad": "Sütaş Süt 1L", "fiyat": 35.0, "adet": 50},
        {"barkod": "102", "ad": "Torku Şeker 1kg", "fiyat": 30.0, "adet": 40},
        {"barkod": "103", "ad": "Ekmek", "fiyat": 10.0, "adet": 100}
    ]
    
    cari_listesi = [
        {"ad": "Ahmet Yılmaz", "telefon": "5551112233", "bakiye": 250.0},
        {"ad": "Mehmet Demir", "telefon": "5554445566", "bakiye": 120.5}
    ]

    # --- 1. SAYFA: STOK / ÜRÜN YÖNETİMİ ---
    barkod_input = ft.TextField(label="Barkod No", width=150)
    urun_ad_input = ft.TextField(label="Ürün Adı", width=200)
    fiyat_input = ft.TextField(label="Satış Fiyatı (TL)", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    adet_input = ft.TextField(label="Stok Adedi", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    
    stok_tablo = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Barkod")),
            ft.DataColumn(ft.Text("Ürün Adı")),
            ft.DataColumn(ft.Text("Fiyat")),
            ft.DataColumn(ft.Text("Adet")),
        ],
        rows=[]
    )

    def stoklari_guncelle():
        stok_tablo.rows.clear()
        for item in stok_listesi:
            stok_tablo.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(item["barkod"])),
                    ft.DataCell(ft.Text(item["ad"])),
                    ft.DataCell(ft.Text(f"{item['fiyat']} TL")),
                    ft.DataCell(ft.Text(str(item["adet"]))),
                ])
            )
        page.update()

    def urun_ekle(e):
        if barkod_input.value and urun_ad_input.value and fiyat_input.value and adet_input.value:
            stok_listesi.append({
                "barkod": barkod_input.value,
                "ad": urun_ad_input.value,
                "fiyat": float(fiyat_input.value),
                "adet": int(adet_input.value)
            })
            barkod_input.value = ""
            urun_ad_input.value = ""
            fiyat_input.value = ""
            adet_input.value = ""
            stoklari_guncelle()
            page.snack_bar = ft.SnackBar(ft.Text("Ürün başarıyla eklendi!"), bgcolor="green")
            page.snack_bar.open = True
            page.update()

    stok_ekle_btn = ft.ElevatedButton("Ürün Ekle", on_click=urun_ekle, bgcolor="green", color="white")
    stoklari_guncelle()

    stok_view = ft.Column([
        ft.Text("Ürün ve Stok Yönetimi", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([barkod_input, urun_ad_input, fiyat_input, adet_input, stok_ekle_btn], wrap=True),
        ft.Divider(),
        stok_tablo
    ], scroll=ft.ScrollMode.AUTO)


    # --- 2. SAYFA: HIZLI SATIŞ VE KASA ---
    satis_barkod = ft.TextField(label="Ürün Barkodu Okut", width=250)
    satis_sonuc = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color="blue")
    
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

    satis_btn = ft.ElevatedButton("Satışı Tamamla", on_click=urun_sat, bgcolor="blue", color="white")

    satis_view = ft.Column([
        ft.Text("Hızlı Satış Kasası", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([satis_barkod, satis_btn]),
        satis_sonuc
    ], spacing=20)


    # --- 3. SAYFA: CARİ / VERESİYE TAKİBİ ---
    cari_tablo = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Müşteri Adı")),
            ft.DataColumn(ft.Text("Telefon")),
            ft.DataColumn(ft.Text("Borç / Bakiye")),
        ],
        rows=[]
    )

    def carileri_guncelle():
        cari_tablo.rows.clear()
        for c in cari_listesi:
            cari_tablo.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(c["ad"])),
                    ft.DataCell(ft.Text(c["telefon"])),
                    ft.DataCell(ft.Text(f"{c['bakiye']} TL", color="red" if c['bakiye'] > 0 else "green")),
                ])
            )
        page.update()
    
    carileri_guncelle()

    cari_view = ft.Column([
        ft.Text("Müşteri Cari ve Veresiye Listesi", size=20, weight=ft.FontWeight.BOLD),
        cari_tablo
    ], scroll=ft.ScrollMode.AUTO)


    # --- ANA SEKMELİ YAPI (TABS) ---
    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Hızlı Satış", content=ft.Container(content=satis_view, padding=20)),
            ft.Tab(text="Stok İşlemleri", content=ft.Container(content=stok_view, padding=20)),
            ft.Tab(text="Cari Takip", content=ft.Container(content=cari_view, padding=20)),
        ],
        expand=1
    )

    page.add(
        ft.Row([ft.Text("🛒 Bakkal Yönetim Paneli", size=22, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
        t
    )

ft.app(target=main)
