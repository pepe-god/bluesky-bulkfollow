import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from atproto import Client

load_dotenv()

def get_followers(client, target_account, limit=1000):
    followers = []
    cursor = None
    print(f"🔄 {target_account} hesabının takipçileri çekiliyor (Limit: {limit})")
    try:
        while len(followers) < limit:
            response = client.get_followers(target_account, limit=100, cursor=cursor)
            if not response.followers:
                print("❌ Daha fazla takipçi yok")
                break
            new_followers = [f.handle for f in response.followers]
            followers.extend(new_followers)
            cursor = response.cursor
            print(f"✅ {len(new_followers)} yeni takipçi eklendi (Toplam: {len(followers)})")
            if len(followers) >= limit or not cursor:
                break
            time.sleep(1)
        print(f"⏹️ Toplam {len(followers)} takipçi bulundu")
        return followers[:limit]
    except Exception as e:
        print(f"⚠️ Takipçi çekme hatası: {str(e)}")
        return followers

def is_inactive_profile(client, handle):
    try:
        profile = client.get_profile(handle)
        issues = []
        if profile.viewer and profile.viewer.following:
            return True, "zaten takip ediliyor", profile.did

        if not profile.avatar:
            issues.append("profil fotoğrafı yok")

        if not profile.description or not profile.description.strip():
            issues.append("biyografi yok")

        if issues:
            return True, ", ".join(issues), profile.did
        return False, "aktif profil", profile.did
    except Exception as e:
        return True, f"profil yüklenemedi: {str(e)}", handle

def bulk_follow(client, target_handles):
    total = len(target_handles)
    print(f"🚀 {total} kullanıcı için takip işlemi başlıyor...")
    for index, handle in enumerate(target_handles, 1):
        try:
            is_inactive, reason, did = is_inactive_profile(client, handle)
            if is_inactive:
                print(f"⏭️ [{index}/{total}] Atlandı: {handle} - Sebep: {reason}")
                continue
            client.follow(did)
            print(f"✅ [{index}/{total}] Takip edildi: {handle}")
            time.sleep(5)
        except Exception as e:
            print(f"❌ [{index}/{total}] Hata: {handle} - {str(e)}")
            continue
    print("🎉 Takip işlemi tamamlandı!")

if __name__ == "__main__":
    client = Client()
    try:
        client.login(os.getenv('BSKY_HANDLE'), os.getenv('BSKY_PASSWORD'))
        print("🔑 Giriş başarılı!")
        TARGET_ACCOUNT = "avmahmuttanal.bsky.social"
        print(f"🎯 Hedef hesap: {TARGET_ACCOUNT}")
        followers = get_followers(client, TARGET_ACCOUNT)
        bulk_follow(client, followers)
    except Exception as e:
        print(f"💥 Genel hata: {str(e)}")
