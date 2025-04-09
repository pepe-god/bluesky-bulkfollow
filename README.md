# Bluesky Takipçi Otomasyonu

Bu Python betiği, Bluesky sosyal ağında belirli bir hesabın takipçilerini çekerek otomatik takip işlemi yapar.

## 📋 Özellikler

- **Takipçi Listesi Çekme**: Hedef hesabın takipçilerini listeler
- **Profil Analizi**: Her profili aktiflik durumuna göre kontrol eder
- **Akıllı Takip Sistemi**: 
  - Zaten takip edilenleri atlar
  - Profil fotoğrafı/biyografisi olmayan hesapları filtreler
  - Hatalı hesapları otomatik atlar
- **Rate Limit Koruma**: İstekler arasında bekleme süreleri bulunur

## ⚙️ Kurulum

1. Gereksinimleri yükleyin:
```bash
pip install atproto python-dotenv
```

2. `.env` dosyasını düzenleyin:
```env
BSKY_HANDLE=kullaniciadi.bsky.social
BSKY_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

## 🚀 Kullanım

1. Betiği çalıştırmadan önce `TARGET_ACCOUNT` değişkenini güncelleyin
2. Terminalden çalıştırın:
```bash
python script_adi.py
```

## ⚠️ Dikkat Edilmesi Gerekenler

- **App Password kullanın** - Normal şifreniz değil!
- **Rate Limit** - Bluesky'nin [rate limit kurallarına](https://docs.bsky.app/docs/advanced-guides/rate-limits) uyun
- **Makul kullanım** - Aşırı takip işlemi hesabınızın askıya alınmasına neden olabilir
- **Güvenlik** - `.env` dosyanızı paylaşmayın/gitignore'a ekleyin

## 📊 Çıktı Örneği

```
🔑 Giriş başarılı!
🎯 Hedef hesap: example.bsky.social
🔄 example.bsky.social hesabının takipçileri çekiliyor (Limit: 1000)
✅ 100 yeni takipçi eklendi (Toplam: 100)
⏹️ Toplam 150 takipçi bulundu
🚀 150 kullanıcı için takip işlemi başlıyor...
⏭️ [1/150] Atlandı: user1.bsky.social - Sebep: zaten takip ediliyor
✅ [2/150] Takip edildi: user2.bsky.social
⏭️ [3/150] Atlandı: user3.bsky.social - Sebep: profil fotoğrafı yok, biyografi yok
```

Bluesky'nin [Hizmet Şartları](https://bsky.social/about/support/tos)'nı ihlal etmemeye özen gösterin.
