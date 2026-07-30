import flet as ft

def main(page: ft.Page):
    page.title = "Bulut Girişli Uygulama"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- ANA UYGULAMA EKRANI (Sayaç) ---
    def load_main_app():
        page.clean()  # Ekrandaki her şeyi temizle
        
        txt_number = ft.TextField(value="0", text_align=ft.TextAlign.CENTER, width=100)

        def minus_click(e):
            txt_number.value = str(int(txt_number.value) - 1)
            page.update()

        def plus_click(e):
            txt_number.value = str(int(txt_number.value) + 1)
            page.update()

        def logout_click(e):
            load_login_screen() # Çıkış yapıp giriş ekranına dön

        page.add(
            ft.Column(
                [
                    ft.Text("Hoş Geldiniz, Yönetici", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                            txt_number,
                            ft.IconButton(ft.Icons.ADD, on_click=plus_click),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.ElevatedButton("Çıkış Yap", on_click=logout_click, color=ft.Colors.RED)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )
        page.update()

    # --- GİRİŞ EKRANI (Login) ---
    def load_login_screen():
        page.clean()

        username_field = ft.TextField(label="Kullanıcı Adı", width=250)
        password_field = ft.TextField(label="Şifre", password=True, can_reveal_password=True, width=250)
        error_text = ft.Text("", color=ft.Colors.RED)

        def login_click(e):
            # Belirleyeceğiniz kullanıcı adı ve şifre
            if username_field.value == "admin" and password_field.value == "1234":
                load_main_app()  # Başarılı ise ana ekrana git
            else:
                error_text.value = "Hatalı kullanıcı adı veya şifre!"
                page.update()

        page.add(
            ft.Column(
                [
                    ft.Text("Sistem Girişi", size=24, weight=ft.FontWeight.BOLD),
                    username_field,
                    password_field,
                    ft.ElevatedButton("Giriş Yap", on_click=login_click, width=250),
                    error_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        )
        page.update()

    # İlk açılışta giriş ekranını göster
    load_login_screen()

ft.run(main)