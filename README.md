# Bluesky Takipçi Otomasyonu

Bu Python betiği, Bluesky sosyal ağında belirli bir hesabın takipçilerini çekerek otomatik takip işlemi yapar.

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

## ⚠️ Dikkat Edilmesi Gerekenler

- **App Password kullanın** - Normal şifreniz değil!
- **Rate Limit** - Bluesky'nin [rate limit kurallarına](https://docs.bsky.app/docs/advanced-guides/rate-limits) uyun
- **Makul kullanım** - Aşırı takip işlemi hesabınızın askıya alınmasına neden olabilir
- **Güvenlik** - `.env` dosyanızı paylaşmayın!

Bluesky'nin [Hizmet Şartları](https://bsky.social/about/support/tos)'nı ihlal etmemeye özen gösterin.
