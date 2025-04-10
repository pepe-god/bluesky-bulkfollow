import os
import time
import threading
from dotenv import load_dotenv
from atproto import Client

load_dotenv()

class FollowerTracker:
    def __init__(self, client, actor):
        self.client = client
        self.actor = actor
        self.followers_count = 0
        self.following_count = 0
        self.lock = threading.Lock()

    def update_counts(self):
        while not getattr(self, 'stop_thread', False):
            with self.lock:
                current_counts = f"Following: {self.following_count} / Followers: {self.followers_count}"
                print(f"\r{current_counts.ljust(50)}", end='', flush=True)
            time.sleep(1)

    def get_relationships(self, list_type):
        items = []
        cursor = None

        try:
            while True:
                if list_type == 'followers':
                    response = self.client.get_followers(self.actor, limit=100, cursor=cursor)
                    new_items = [f.did for f in response.followers]
                else:
                    response = self.client.get_follows(self.actor, limit=100, cursor=cursor)
                    new_items = [f.did for f in response.follows]

                items.extend(new_items)

                with self.lock:
                    if list_type == 'followers':
                        self.followers_count = len(items)
                    else:
                        self.following_count = len(items)

                cursor = response.cursor
                if not cursor:
                    break

        except Exception as e:
            print(f"\n⚠️ {list_type} hatası: {str(e)}")

        return items

def main():
    client = Client()
    try:
        client.login(os.getenv('BSKY_HANDLE'), os.getenv('BSKY_PASSWORD'))
        print(f"🔑 Giriş başarılı: {client.me.handle}")

        tracker = FollowerTracker(client, client.me.did)

        counter_thread = threading.Thread(target=tracker.update_counts, daemon=True)
        counter_thread.start()

        followers_thread = threading.Thread(
            target=lambda: setattr(tracker, 'followers', tracker.get_relationships('followers'))
        )
        following_thread = threading.Thread(
            target=lambda: setattr(tracker, 'following', tracker.get_relationships('following'))
        )

        followers_thread.start()
        following_thread.start()

        followers_thread.join()
        following_thread.join()

        tracker.stop_thread = True
        counter_thread.join()

        print(f"\n\n🔍 Veri çekme tamamlandı - Following: {tracker.following_count} / Followers: {tracker.followers_count}")

        targets = list(set(tracker.followers) - set(tracker.following))
        print(f"🎯 Takip edilecek {len(targets)} kullanıcı bulundu\n")

        for did in targets:
            try:
                profile = client.get_profile(did)
                username = profile.handle
                client.follow(did)
                print(f"✅ Takip edildi: @{username}")
                time.sleep(5)
            except Exception as e:
                print(f"❌ Hata: {str(e)}")
                continue

        print("\n🎉 İşlem tamamlandı!")

    except Exception as e:
        print(f"\n💥 Kritik hata: {str(e)}")

if __name__ == "__main__":
    main()
