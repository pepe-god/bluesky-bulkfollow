import os
import time
from dotenv import load_dotenv
from atproto import Client

load_dotenv()

def fetch_followers(client, target_account, max_followers=2500):
    print(f"⏳ {target_account} takipçileri çekiliyor (Maksimum: {max_followers})")
    followers = []
    cursor = None

    try:
        while len(followers) < max_followers:
            response = client.get_followers(target_account, limit=100, cursor=cursor)
            if not response.followers:
                print("❌ Daha fazla takipçi bulunamadı")
                break

            new_followers = [(f.did, f.handle) for f in response.followers]
            followers.extend(new_followers)
            cursor = response.cursor

            print(f"✅ {len(new_followers)} yeni takipçi eklendi (Toplam: {len(followers)})")
            if len(followers) >= max_followers or not cursor:
                break
            time.sleep(0.5)

        return followers[:max_followers]

    except Exception as e:
        print(f"⚠️ Takipçi çekme hatası: {str(e)}")
        return followers

def should_skip_profile(client, did, handle):
    try:
        profile = client.get_profile(did)

        if profile.viewer and profile.viewer.following:
            return True, f"@{handle} - Zaten takip ediliyor"

        if not profile.avatar:
            return True, f"@{handle} - Profil fotoğrafı yok"

        return False, f"@{handle} - Aktif profil"

    except Exception as e:
        return True, f"@{handle} - Profil kontrol hatası: {str(e)}"

def smart_follow(client, follower_list, max_follow=1600):
    success_count = 0
    total_processed = 0

    for did, handle in follower_list:
        if success_count >= max_follow:
            print(f"⏹️ Hedeflenen {max_follow} takip sayısına ulaşıldı")
            break

        total_processed += 1

        try:
            skip, reason = should_skip_profile(client, did, handle)
            if skip:
                print(f"⏭️ [{total_processed}] {reason}")
                continue

            client.follow(did)
            success_count += 1
            print(f"✅ [{success_count}/{max_follow}] @{handle} takip edildi")
            time.sleep(1.5)

        except Exception as e:
            print(f"❌ Hata: @{handle} - {str(e)}")

    print(f"\n🎉 Toplam {success_count} kullanıcı takip edildi")
    print(f"🔍 İşlenen: {total_processed} | Atlanan: {total_processed - success_count}")

if __name__ == "__main__":
    client = Client()

    try:
        client.login(
            os.getenv('BSKY_HANDLE'),
            os.getenv('BSKY_PASSWORD')
        )
        print("\n🔑 Bluesky'e giriş başarılı!\n")

        target = "ekremimamoglu.com"
        followers = fetch_followers(client, target, 2500)
        print(f"\n🔥 {len(followers)} takipçi başarıyla çekildi\n")

        smart_follow(client, followers, 1600)

    except Exception as e:
        print(f"\n💥 Kritik hata: {str(e)}")
